import glob
import io
import json
import os
import re
import requests
import subprocess
import time

from dcicutils import ff_utils
# get_env_real_url would rely on env_utils
# from dcicutils.env_utils import get_env_real_url
from dcicutils.command_utils import yes_or_no
from dcicutils.common import APP_CGAP, APP_FOURFRONT, OrchestratedApp
# We're not going to use full_cgap_env_name now, we'll just rely on the keys file to say what the name is.
# from dcicutils.env_utils import full_cgap_env_name
from dcicutils.exceptions import InvalidParameterError
from dcicutils.ff_utils import get_health_page
from dcicutils.lang_utils import n_of, conjoined_list, disjoined_list, there_are
from dcicutils.misc_utils import check_true, environ_bool, PRINT, url_path_join, ignorable, remove_prefix
from dcicutils.s3_utils import HealthPageKey
from typing import BinaryIO, Dict, Optional
from typing_extensions import Literal
from urllib.parse import urlparse
from .base import DEFAULT_ENV, DEFAULT_ENV_VAR, PRODUCTION_ENV, KEY_MANAGER
from .exceptions import CGAPPermissionError
from .utils import show, keyword_as_title


class SubmissionProtocol:
    S3 = 's3'
    UPLOAD = 'upload'


SUBMISSION_PROTOCOLS = [SubmissionProtocol.S3, SubmissionProtocol.UPLOAD]

DEFAULT_SUBMISSION_PROTOCOL = SubmissionProtocol.UPLOAD


# TODO: Will asks whether some of the errors in this file that are called "SyntaxError" really should be something else.
#  The thought was that they're syntax errors because they tend to reflect as a need for a change in the
#  command line argument syntax, but maybe I should raise other errors and just have them converted to syntax
#  errors in the command itself. Something to think about another day. -kmp 8-Sep-2020


SERVER_REGEXP = re.compile(
    # Note that this regular expression does NOT contain 4dnucleome.org for the same reason it requires
    # a fourfront-cgapXXX address. It is trying only to match cgap addresses, though of course it has to make an
    # exception for localhost debugging. You're on your own to make sure the right server is connected there.
    # -kmp 16-Aug-2020
    r"^(https?://localhost(:[0-9]+)?"
    r"|https?://(fourfront-cgap|cgap-)[a-z0-9.-]*"
    r"|https?://([a-z-]+[.])*cgap[.]hms[.]harvard[.]edu)/?$"
)


def resolve_server(server, env):
    """
    Given a server spec or a beanstalk environment (or neither, but not both), returns a server spec.

    :param server: a server spec or None
      A server is the first part of a url (containing the schema, host and, optionally, port).
      e.g., http://cgap.hms.harvard.edu or http://localhost:8000
    :param env: a cgap beanstalk environment
    :return: a server spec
    """

    check_true(not server or not env, "You may not specify both 'server' and 'env'.", error_class=SyntaxError)

    if not server and not env:
        if DEFAULT_ENV:
            show(f"Defaulting to environment {env!r} because {DEFAULT_ENV_VAR} is set.")
            env = DEFAULT_ENV
        else:
            # Production default needs no explanation.
            env = PRODUCTION_ENV

    if env:
        try:
            env = env  # was full_cgap_env_name(env), but we don't want to rely on env_utils for this tool
            server = KEY_MANAGER.get_keydict_for_env(env)['server']
        except Exception:
            raise SyntaxError(f"The specified env is not a known environment name: {env}")

    try:
        if server:
            # Called for effect. This will err if it's not there.
            KEY_MANAGER.get_keydict_for_server(server)
    except Exception:
        matched = SERVER_REGEXP.match(server)
        if not matched:
            raise ValueError("The server should be 'http://localhost:<port>' or 'https://<cgap-hostname>', not: %s"
                             % server)
        server = matched.group(1)

    return server


def get_user_record(server, auth):
    """
    Given a server and some auth info, gets the user record for the authorized user.

    This works by using the /me endpoint.

    :param server: a server spec
    :param auth: auth info to be used when contacting the server
    :return: the /me page in JSON format
    """

    user_url = server + "/me?format=json"
    user_record_response = requests.get(user_url, auth=auth)
    try:
        user_record = user_record_response.json()
    except Exception:
        user_record = {}
    try:
        if user_record_response.status_code in (401, 403) and user_record.get("Title") == "Not logged in.":
            show("Server did not recognize you with the given credentials.")
    except Exception:
        pass
    if user_record_response.status_code in (401, 403):
        raise CGAPPermissionError(server=server)
    user_record_response.raise_for_status()
    user_record = user_record_response.json()
    show("The server %s recognizes you as %s <%s>."
         % (server, user_record['title'], user_record['contact_email']))
    return user_record


def get_defaulted_institution(institution, user_record):
    """
    Returns the given institution or else if none is specified, it tries to infer an institution.

    :param institution: the @id of an institution, or None
    :param user_record: the user record for the authorized user
    :return: the @id of an institution to use
    """

    if not institution:
        institution = user_record.get('user_institution', {}).get('@id', None)
        if not institution:
            raise SyntaxError("Your user profile has no institution declared,"
                              " so you must specify --institution explicitly.")
        show("Using institution:", institution)
    return institution


def get_defaulted_project(project, user_record):
    """
    Returns the given project or else if none is specified, it tries to infer a project.

    :param project: the @id of a project, or None
    :param user_record: the user record for the authorized user
    :return: the @id of a project to use
    """

    if not project:
        # Ref: https://hms-dbmi.atlassian.net/browse/C4-371
        # The project_roles are expected to look like:
        #  [
        #    {"project": {"@id": "/projects/foo"}, "role": "developer"},
        #    {"project": {"@id": "/projects/bar"}, "role": "clinician"},
        #    {"project": {"@id": "/projects/baz"}, "role": "director"},
        #  ]
        project_roles = user_record.get('project_roles', [])
        if len(project_roles) == 0:
            raise SyntaxError("Your user profile declares no project roles.")
        elif len(project_roles) > 1:
            raise SyntaxError("You must use --project to specify which project you are submitting for"
                              " (probably one of: %s)." % ", ".join([x['project']['@id'] for x in project_roles]))
        else:
            [project_role] = project_roles
            project = project_role['project']['@id']
            show("Using project:", project)
    return project


def get_defaulted_award(award, user_record, error_if_none=False):
    """
    Returns the given award or else if none is specified, it tries to infer an award.

    :param award: the @id of an award, or None
    :param user_record: the user record for the authorized user
    :param error_if_none: boolean true if failure to infer an award should an raise error, and false otherwise.
    :return: the @id of an award to use
    """

    if not award:
        # The lab is expected to have awards looking like:
        #  [
        #    {"@id": "/awards/foo", ...},
        #    {"@id": "/awards/bar", ...},
        #    {"@id": "/awards/baz", ...},
        #  ]
        lab = user_record.get('lab', {})
        lab_awards = lab.get('awards', [])
        if len(lab_awards) == 0:
            if error_if_none:
                raise SyntaxError("Your user profile declares no lab with awards.")
        elif len(lab_awards) > 1:
            options = disjoined_list([award['@id'] for award in lab_awards])
            if error_if_none:
                raise SyntaxError(f"Your lab ({lab['@id']}) declares multiple awards."
                                  f" You must explicitly specify one of {options} with --award.")
        else:
            [lab_award] = lab_awards
            award = lab_award['@id']
        if not award:
            show("No award was inferred.")
        else:
            show("Using inferred award:", award)
    else:
        show("Using given award:", award)
    return award


def get_defaulted_lab(lab, user_record, error_if_none=False):
    """
    Returns the given lab or else if none is specified, it tries to infer a lab.

    :param lab: the @id of a lab, or None
    :param user_record: the user record for the authorized user
    :param error_if_none: boolean true if failure to infer a lab should an raise error, and false otherwise.
    :return: the @id of a lab to use
    """

    if not lab:
        lab = user_record.get('lab', {}).get('@id', None)
        if not lab:
            if error_if_none:
                raise SyntaxError("Your user profile has no lab declared,"
                                  " so you must specify --lab explicitly.")
        if not lab:
            show("No lab was inferred.")
        else:
            show("Using inferred lab:", lab)
    else:
        show("Using given lab:", lab)
    return lab


APP_ARG_DEFAULTERS = {
    'institution': get_defaulted_institution,
    'project': get_defaulted_project,
    'lab': get_defaulted_lab,
    'award': get_defaulted_award,
}


def do_app_arg_defaulting(app_args, user_record):
    for arg, val in app_args.items():
        defaulter = APP_ARG_DEFAULTERS.get(arg)
        if defaulter:
            app_args[arg] = defaulter(val, user_record)


PROGRESS_CHECK_INTERVAL = 15  # seconds
ATTEMPTS_BEFORE_TIMEOUT = 40


def get_section(res, section):
    """
    Given a description of an ingestion submission, returns a section name within that ingestion.

    :param res: the description of an ingestion submission as a python dictionary that represents JSON data
    :param section: the name of a section to find either in the toplevel or in additional_data.
    :return: the section's content
    """

    return res.get(section) or res.get('additional_data', {}).get(section)


def show_section(res, section, caveat_outcome=None):
    """
    Shows a given named section from a description of an ingestion submission.

    The caveat is used when there has been an error and should be a phrase that describes the fact that output
    shown is only up to the point of the caveat situation. Instead of a "My Heading" header the output will be
    "My Heading (prior to <caveat>)."

    :param res: the description of an ingestion submission as a python dictionary that represents JSON data
    :param section: the name of a section to find either in the toplevel or in additional_data.
    :param caveat_outcome: a phrase describing some caveat on the output
    """

    section_data = get_section(res, section)
    if caveat_outcome and not section_data:
        # In the case of non-success, be brief unless there's data to show.
        return
    if caveat_outcome:
        caveat = " (prior to %s)" % caveat_outcome
    else:
        caveat = ""
    show("----- %s%s -----" % (keyword_as_title(section), caveat))
    if not section_data:
        show("Nothing to show.")
    elif isinstance(section_data, dict):
        show(json.dumps(section_data, indent=2))
    elif isinstance(section_data, list):
        for line in section_data:
            show(line)
    else:  # We don't expect this, but such should be shown as-is, mostly to see what it is.
        show(section_data)


def ingestion_submission_item_url(server, uuid):
    return url_path_join(server, "ingestion-submissions", uuid) + "?format=json"


DEBUG_PROTOCOL = environ_bool("DEBUG_PROTOCOL", default=False)

TRY_OLD_PROTOCOL = True


def _post_files_data(submission_protocol, ingestion_filename) -> Dict[Literal['datafile'], Optional[BinaryIO]]:
    """
    This composes a dictionary of the form {'datafile': <maybe-stream>}.

    If the submission protocol is SubmissionProtocol.UPLOAD (i.e., 'upload'), the given ingestion filename is opened
    and used as the datafile value in the dictionary. If it is something else, no file is opened and None is used.

    :param submission_protocol:
    :param ingestion_filename:
    :return: a dictionary with key 'datafile' whose value is either an open binary input stream or None
    """

    if submission_protocol == SubmissionProtocol.UPLOAD:
        return {"datafile": io.open(ingestion_filename, 'rb')}
    else:
        return {"datafile": None}


def _post_submission(server, keypair, ingestion_filename, creation_post_data, submission_post_data,
                     submission_protocol=DEFAULT_SUBMISSION_PROTOCOL):
    """ This takes care of managing the compatibility step of using either the old or new ingestion protocol.

    OLD PROTOCOL: Post directly to /submit_for_ingestion

    NEW PROTOCOL: Create an IngestionSubmission and then use /ingestion-submissions/<guid>/submit_for_ingestion

    :param server: the name of the server as a URL
    :param keypair: a tuple which is a keypair (key_id, secret_key)
    :param ingestion_filename: the bundle filename to be submitted
    :param creation_post_data: data to become part of the post data for the creation
    :param submission_post_data: data to become part of the post data for the ingestion
    :return: the results of the ingestion call (whether by the one-step or two-step process)
    """

    if submission_protocol == SubmissionProtocol.UPLOAD and TRY_OLD_PROTOCOL:

        old_style_submission_url = url_path_join(server, "submit_for_ingestion")
        old_style_post_data = dict(creation_post_data, **submission_post_data)

        response = requests.post(old_style_submission_url,
                                 auth=keypair,
                                 data=old_style_post_data,
                                 headers={'Content-type': 'application/json'},
                                 files=_post_files_data(submission_protocol=submission_protocol,
                                                        ingestion_filename=ingestion_filename))

        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT("old_style_submission_url=", old_style_submission_url)
            PRINT("old_style_post_data=", json.dumps(old_style_post_data, indent=2))
            PRINT("keypair=", keypair)
            PRINT("response=", response)

        if response.status_code != 404:

            if DEBUG_PROTOCOL:  # pragma: no cover
                PRINT("Old style protocol worked.")

            return response

        else:  # on 404, try new protocol ...

            if DEBUG_PROTOCOL:  # pragma: no cover
                PRINT("Retrying with new protocol.")

    creation_post_headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }
    creation_post_url = url_path_join(server, "IngestionSubmission")
    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT("creation_post_data=", json.dumps(creation_post_data, indent=2))
        PRINT("creation_post_url=", creation_post_url)
    creation_response = requests.post(creation_post_url, auth=keypair,
                                      headers=creation_post_headers,
                                      json=creation_post_data
                                      # data=json.dumps(creation_post_data)
                                      )
    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT("headers:", creation_response.request.headers)
    creation_response.raise_for_status()
    [submission] = creation_response.json()['@graph']
    submission_id = submission['@id']

    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT("server=", server, "submission_id=", submission_id)
    new_style_submission_url = url_path_join(server, submission_id, "submit_for_ingestion")
    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT("submitting new_style_submission_url=", new_style_submission_url)
        PRINT(f"data=submission_post_data={json.dumps(submission_post_data, indent=2)}")
    response = requests.post(new_style_submission_url, auth=keypair, data=submission_post_data,
                             files=_post_files_data(submission_protocol=submission_protocol,
                                                    ingestion_filename=ingestion_filename))
    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT("response received for submission post:", response)
        PRINT("response.content:", response.content)

    return response


DEFAULT_INGESTION_TYPE = 'metadata_bundle'

DEFAULT_APP = APP_CGAP

GENERIC_SCHEMA_TYPE = 'FileOther'


def _resolve_app_args(institution, project, lab, award, app):

    app_args = {}
    if app == APP_CGAP:
        required_args = {'institution': institution, 'project': project}
        unwanted_args = {'lab': lab, 'award': award}
    elif app == APP_FOURFRONT:
        required_args = {'lab': lab, 'award': award}
        unwanted_args = {'institution': institution, 'project': project}
    else:
        raise ValueError(f"Unknown application: {app}")

    for argname, argvalue in required_args.items():
        app_args[argname] = argvalue

    extra_keys = []
    for argname, argvalue in unwanted_args.items():
        if argvalue:
            extra_keys.append(f"--{argname}")

    if extra_keys:
        raise ValueError(there_are(extra_keys, kind="inappropriate argument", joiner=conjoined_list, punctuate=True))

    return app_args


def submit_any_ingestion(ingestion_filename, *, ingestion_type, server, env, validate_only,
                         institution=None, project=None, lab=None, award=None, app: OrchestratedApp = None,
                         upload_folder=None, no_query=False, subfolders=False,
                         submission_protocol=DEFAULT_SUBMISSION_PROTOCOL):
    """
    Does the core action of submitting a metadata bundle.

    :param ingestion_filename: the name of the main data file to be ingested
    :param ingestion_type: the type of ingestion to be performed (an ingestion_type in the IngestionSubmission schema)
    :param server: the server to upload to
    :param env: the beanstalk environment to upload to
    :param validate_only: whether to do stop after validation instead of proceeding to post metadata
    :param app: either 'cgap' (the default) or 'fourfront'
    :param institution: the @id of the institution for which the submission is being done (when app='cgap' or None)
    :param project: the @id of the project for which the submission is being done (when app='cgap' or None)
    :param lab: the @id of the lab for which the submission is being done (when app='fourfront')
    :param award: the @id of the award for which the submission is being done (when app='fourfront')
    :param upload_folder: folder in which to find files to upload (default: same as bundle_filename)
    :param no_query: bool to suppress requests for user input
    :param subfolders: bool to search subdirectories within upload_folder for files
    :param submission_protocol: which submission protocol to use (default: 's3')
    """

    if app is None:  # For legacy reasons, SubmitCGAP was the first so didn't expect this arg was needed
        app = DEFAULT_APP

    if KEY_MANAGER.selected_app != app:
        with KEY_MANAGER.locally_selected_app(app):
            return submit_any_ingestion(ingestion_filename=ingestion_filename, ingestion_type=ingestion_type,
                                        server=server, env=env, validate_only=validate_only,
                                        institution=institution, project=project, lab=lab, award=award, app=app,
                                        upload_folder=upload_folder, no_query=no_query, subfolders=subfolders,
                                        submission_protocol=submission_protocol)

    app_args = _resolve_app_args(institution=institution, project=project, lab=lab, award=award, app=app)

    server = resolve_server(server=server, env=env)

    validation_qualifier = " (for validation only)" if validate_only else ""

    maybe_ingestion_type = ''
    if ingestion_type != DEFAULT_INGESTION_TYPE:
        maybe_ingestion_type = " (%s)" % ingestion_type

    if not no_query:
        if not yes_or_no("Submit %s%s to %s%s?"
                         % (ingestion_filename, maybe_ingestion_type, server, validation_qualifier)):
            show("Aborting submission.")
            exit(1)

    keydict = KEY_MANAGER.get_keydict_for_server(server)
    keypair = KEY_MANAGER.keydict_to_keypair(keydict)

    user_record = get_user_record(server, auth=keypair)

    do_app_arg_defaulting(app_args, user_record)

    if not os.path.exists(ingestion_filename):
        raise ValueError("The file '%s' does not exist." % ingestion_filename)

    creation_post_data = {
        'ingestion_type': ingestion_type,
        "processing_status": {
            "state": "submitted"
        },
        **app_args,  # institution & project or lab & award
    }

    if submission_protocol == SubmissionProtocol.S3:

        upload_result = upload_file_to_new_uuid(filename=ingestion_filename, schema_name=GENERIC_SCHEMA_TYPE,
                                                auth=keydict, **app_args)

        submission_post_data = compute_s3_submission_post_data(ingestion_filename=ingestion_filename,
                                                               ingestion_post_result=upload_result,
                                                               # The rest of this is other_args to pass through...
                                                               validate_only=validate_only, **app_args)

    elif submission_protocol == SubmissionProtocol.UPLOAD:

        submission_post_data = {
            'validate_only': validate_only,
        }

    else:

        raise InvalidParameterError(parameter='submission_protocol', value=submission_protocol,
                                    options=SUBMISSION_PROTOCOLS)

    response = _post_submission(server=server, keypair=keypair,
                                ingestion_filename=ingestion_filename,
                                creation_post_data=creation_post_data,
                                submission_post_data=submission_post_data,
                                submission_protocol=submission_protocol)

    try:
        # This can fail if the body doesn't contain JSON
        res = response.json()
    except Exception:  # pragma: no cover
        # This clause is not ordinarily entered. It handles a pathological case that we only hypothesize.
        # It does not require careful unit test coverage. -kmp 23-Feb-2022
        res = None

    try:
        response.raise_for_status()
    except Exception:
        if res is not None:
            # For example, if you call this on an old version of cgap-portal that does not support this request,
            # the error will be a 415 error, because the tween code defaultly insists on applicatoin/json:
            # {
            #     "@type": ["HTTPUnsupportedMediaType", "Error"],
            #     "status": "error",
            #     "code": 415,
            #     "title": "Unsupported Media Type",
            #     "description": "",
            #     "detail": "Request content type multipart/form-data is not 'application/json'"
            # }
            title = res.get('title')
            message = title
            detail = res.get('detail')
            if detail:
                message += ": " + detail
            show(message)
            if title == "Unsupported Media Type":
                show("NOTE: This error is known to occur if the server"
                     " does not support metadata bundle submission.")
        raise

    if res is None:  # pragma: no cover
        # This clause is not ordinarily entered. It handles a pathological case that we only hypothesize.
        # It does not require careful unit test coverage. -kmp 23-Feb-2022
        raise Exception("Bad JSON body in %s submission result." % response.status_code)

    uuid = res['submission_id']

    show("Bundle uploaded, assigned uuid %s for tracking. Awaiting processing..." % uuid, with_time=True)

    tracking_url = ingestion_submission_item_url(server=server, uuid=uuid)

    outcome = None
    tries_left = ATTEMPTS_BEFORE_TIMEOUT
    done = False
    while tries_left > 0:
        # Pointless to hit the queue immediately, so we avoid some
        # server stress by sleeping even before the first try.
        time.sleep(PROGRESS_CHECK_INTERVAL)
        res = requests.get(tracking_url, auth=keypair).json()
        processing_status = res['processing_status']
        done = processing_status['state'] == 'done'
        if done:
            outcome = processing_status['outcome']
            break
        else:
            progress = processing_status['progress']
            show("Progress is %s. Continuing to wait..." % progress, with_time=True)
        tries_left -= 1

    if not done:
        show("Timed out after %d tries." % ATTEMPTS_BEFORE_TIMEOUT, with_time=True)
        exit(1)

    show("Final status: %s" % outcome, with_time=True)

    if outcome == 'error' and res.get('errors'):
        show_section(res, 'errors')

    caveat_outcome = None if outcome == 'success' else outcome

    show_section(res, 'validation_output', caveat_outcome=caveat_outcome)

    if validate_only:
        exit(0)

    show_section(res, 'post_output', caveat_outcome=caveat_outcome)

    if outcome == 'success':
        show_section(res, 'upload_info')
        do_any_uploads(res, keydict=keydict, ingestion_filename=ingestion_filename,
                       upload_folder=upload_folder, no_query=no_query,
                       subfolders=subfolders)

    exit(0)


def compute_s3_submission_post_data(ingestion_filename, ingestion_post_result, **other_args):
    uuid = ingestion_post_result['uuid']
    at_id = ingestion_post_result['@id']
    accession = ingestion_post_result.get('accession')  # maybe not always there?
    upload_credentials = ingestion_post_result['upload_credentials']
    upload_urlstring = upload_credentials['upload_url']
    upload_url = urlparse(upload_urlstring)
    upload_key = upload_credentials['key']
    upload_bucket = upload_url.netloc
    # Possible sanity check, probably not needed...
    # check_true(upload_key == remove_prefix('/', upload_url.path, required=True),
    #            message=f"The upload_key, {upload_key!r}, did not match path of {upload_url}.")
    submission_post_data = {
        'datafile_uuid': uuid,
        'datafile_accession': accession,
        'datafile_@id': at_id,
        'datafile_url': upload_urlstring,
        'datafile_bucket': upload_bucket,
        'datafile_key': upload_key,
        'datafile_source_filename': os.path.basename(ingestion_filename),
        **other_args  # validate_only, and any of institution, project, lab, or award that caller gave us
    }
    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT(f"submission_post_data={json.dumps(submission_post_data, indent=2)}")
    return submission_post_data


def show_upload_info(uuid, server=None, env=None, keydict=None):
    """
    Uploads the files associated with a given ingestion submission. This is useful if you answered "no" to the query
    about uploading your data and then later are ready to do that upload.

    :param uuid: a string guid that identifies the ingestion submission
    :param server: the server to upload to
    :param env: the beanstalk environment to upload to
    :param keydict: keydict-style auth, a dictionary of 'key', 'secret', and 'server'
    """

    server = resolve_server(server=server, env=env)
    keydict = keydict or KEY_MANAGER.get_keydict_for_server(server)
    url = ingestion_submission_item_url(server, uuid)
    response = requests.get(url, auth=KEY_MANAGER.keydict_to_keypair(keydict))
    response.raise_for_status()
    res = response.json()
    if get_section(res, 'upload_info'):
        show_section(res, 'upload_info')
    else:
        show("No uploads.")


def do_any_uploads(res, keydict, upload_folder=None, ingestion_filename=None,
                   no_query=False, subfolders=False):
    upload_info = get_section(res, 'upload_info')
    folder = upload_folder or (os.path.dirname(ingestion_filename) if ingestion_filename else None)
    if upload_info:
        if no_query:
            do_uploads(upload_info, auth=keydict, no_query=no_query, folder=folder,
                       subfolders=subfolders)
        else:
            if yes_or_no("Upload %s?" % n_of(len(upload_info), "file")):
                do_uploads(upload_info, auth=keydict, no_query=no_query, folder=folder,
                           subfolders=subfolders)
            else:
                show("No uploads attempted.")


def resume_uploads(uuid, server=None, env=None, bundle_filename=None, keydict=None,
                   upload_folder=None, no_query=False, subfolders=False):
    """
    Uploads the files associated with a given ingestion submission. This is useful if you answered "no" to the query
    about uploading your data and then later are ready to do that upload.

    :param uuid: a string guid that identifies the ingestion submission
    :param server: the server to upload to
    :param env: the beanstalk environment to upload to
    :param bundle_filename: the bundle file to be uploaded
    :param keydict: keydict-style auth, a dictionary of 'key', 'secret', and 'server'
    :param upload_folder: folder in which to find files to upload (default: same as ingestion_filename)
    :param no_query: bool to suppress requests for user input
    :param subfolders: bool to search subdirectories within upload_folder for files
    """

    server = resolve_server(server=server, env=env)
    keydict = keydict or KEY_MANAGER.get_keydict_for_server(server)
    url = ingestion_submission_item_url(server, uuid)
    keypair = KEY_MANAGER.keydict_to_keypair(keydict)
    response = requests.get(url, auth=keypair)
    response.raise_for_status()
    do_any_uploads(response.json(),
                   keydict=keydict,
                   ingestion_filename=bundle_filename,
                   upload_folder=upload_folder,
                   no_query=no_query,
                   subfolders=subfolders)


def get_s3_encrypt_key_id_from_health_page(auth):
    try:
        health = get_health_page(key=auth)
        return health.get(HealthPageKey.S3_ENCRYPT_KEY_ID)
    except Exception:  # pragma: no cover
        # We don't actually unit test this section because get_health_page realistically always returns
        # a dictionary, and so health.get(...) always succeeds, possibly returning None, which should
        # already be tested. Returning None here amounts to the same and needs no extra unit testing.
        # The presence of this error clause is largely pro forma and probably not really needed.
        return None


def get_s3_encrypt_key_id(*, upload_credentials, auth):
    if 's3_encrypt_key_id' in upload_credentials:
        s3_encrypt_key_id = upload_credentials.get('s3_encrypt_key_id')
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"Extracted s3_encrypt_key_id from upload_credentials: {s3_encrypt_key_id}")
    else:
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"No s3_encrypt_key_id entry found in upload_credentials.")
            PRINT(f"Fetching s3_encrypt_key_id from health page.")
        s3_encrypt_key_id = get_s3_encrypt_key_id_from_health_page(auth)
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f" =id=> {s3_encrypt_key_id!r}")
    return s3_encrypt_key_id


def execute_prearranged_upload(path, upload_credentials, auth=None):
    """
    This performs a file upload using special credentials received from ff_utils.patch_metadata.

    :param path: the name of a local file to upload
    :param upload_credentials: a dictionary of credentials to be used for the upload,
        containing the keys 'AccessKeyId', 'SecretAccessKey', 'SessionToken', and 'upload_url'.
    :param auth: auth info in the form of a dictionary containing 'key', 'secret', and 'server',
        and possibly other useful information such as an encryption key id.
    """

    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT(f"Upload credentials contain {conjoined_list(list(upload_credentials.keys()))}.")
    try:
        s3_encrypt_key_id = get_s3_encrypt_key_id(upload_credentials=upload_credentials, auth=auth)
        extra_env = dict(AWS_ACCESS_KEY_ID=upload_credentials['AccessKeyId'],
                         AWS_SECRET_ACCESS_KEY=upload_credentials['SecretAccessKey'],
                         AWS_SECURITY_TOKEN=upload_credentials['SessionToken'])
        env = dict(os.environ, **extra_env)
    except Exception as e:
        raise ValueError("Upload specification is not in good form. %s: %s" % (e.__class__.__name__, e))

    start = time.time()
    try:
        source = path
        target = upload_credentials['upload_url']
        show("Going to upload %s to %s." % (source, target))
        command = ['aws', 's3', 'cp']
        if s3_encrypt_key_id:
            command = command + ['--sse', 'aws:kms', '--sse-kms-key-id', s3_encrypt_key_id]
        command = command + ['--only-show-errors', source, target]
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"Executing: {command}")
            PRINT(f" ==> {' '.join(command)}")
            PRINT(f"Environment variables include {conjoined_list(list(extra_env.keys()))}.")
        options = {}
        if running_on_windows_native():
            options = {"shell": True}
        subprocess.check_call(command, env=env, **options)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Upload failed with exit code %d" % e.returncode)
    else:
        end = time.time()
        duration = end - start
        show("Uploaded in %.2f seconds" % duration)


def running_on_windows_native():
    return os.name == 'nt'


def compute_file_post_data(filename, context_attributes):
    file_basename = os.path.basename(filename)
    _, ext = os.path.splitext(file_basename)  # could probably get a nicer error message if file in bad format
    file_format = remove_prefix('.', ext, required=True)
    return {
        'filename': file_basename,
        'file_format': file_format,
        **{attr: val for attr, val in context_attributes.items() if val}
    }


def upload_file_to_new_uuid(filename, schema_name, auth, **context_attributes):
    """
    Upload file to a target environment.

    :param filename: the name of a file to upload.
    :param schema_name: the schema_name to use when creating a new file item whose content is to be uploaded.
    :param auth: auth info in the form of a dictionary containing 'key', 'secret', and 'server'.
    :returns: item metadata dict or None
    """

    post_item = compute_file_post_data(filename=filename, context_attributes=context_attributes)

    response = ff_utils.post_metadata(post_item=post_item, schema_name=schema_name, key=auth)

    metadata, upload_credentials = extract_metadata_and_upload_credentials(response,
                                                                           method='POST', schema_name=schema_name,
                                                                           filename=filename, payload_data=post_item)

    execute_prearranged_upload(filename, upload_credentials=upload_credentials, auth=auth)

    return metadata


def upload_file_to_uuid(filename, uuid, auth):
    """
    Upload file to a target environment.

    :param filename: the name of a file to upload.
    :param uuid: the item into which the filename is to be uploaded.
    :param auth: auth info in the form of a dictionary containing 'key', 'secret', and 'server'.
    :returns: item metadata dict or None
    """
    metadata = None
    ignorable(metadata)  # PyCharm might need this if it worries it isn't set below

    # filename here should not include path
    patch_data = {'filename': os.path.basename(filename)}

    response = ff_utils.patch_metadata(patch_data, uuid, key=auth)

    metadata, upload_credentials = extract_metadata_and_upload_credentials(response,
                                                                           method='PATCH', uuid=uuid,
                                                                           filename=filename, payload_data=patch_data)

    execute_prearranged_upload(filename, upload_credentials=upload_credentials, auth=auth)

    return metadata


def extract_metadata_and_upload_credentials(response, filename, method, payload_data, uuid=None, schema_name=None):
    try:
        [metadata] = response['@graph']
        upload_credentials = metadata['upload_credentials']
    except Exception as e:
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"Problem trying to {method} to get upload credentials.")
            PRINT(f" payload_data={payload_data}")
            if uuid:
                PRINT(f" uuid={uuid}")
            if schema_name:
                PRINT(f" schema_name={schema_name}")
            PRINT(f" response={response}")
            PRINT(f"Got error {type(e)}: {e}")
        raise RuntimeError(f"Unable to obtain upload credentials for file {filename}.")
    return metadata, upload_credentials


# This can be set to True in unusual situations, but normally will be False to avoid unnecessary querying.
CGAP_SELECTIVE_UPLOADS = environ_bool("CGAP_SELECTIVE_UPLOADS")


def do_uploads(upload_spec_list, auth, folder=None, no_query=False, subfolders=False):
    """
    Uploads the files mentioned in the give upload_spec_list.

    If any files have associated extra files, upload those as well.

    :param upload_spec_list: a list of upload_spec dictionaries, each of the form {'filename': ..., 'uuid': ...},
        representing uploads to be formed.
    :param auth: a dictionary-form auth spec, of the form {'key': ..., 'secret': ..., 'server': ...}
        representing destination and credentials.
    :param folder: a string naming a folder in which to find the filenames to be uploaded.
    :param no_query: bool to suppress requests for user input
    :param subfolders: bool to search subdirectories within upload_folder for files
    :return: None
    """
    folder = folder or os.path.curdir
    if subfolders:
        folder = os.path.join(folder, '**')
    for upload_spec in upload_spec_list:
        file_name = upload_spec["filename"]
        file_path, error_msg = search_for_file(folder, file_name, recursive=subfolders)
        if error_msg:
            show(error_msg)
            continue
        uuid = upload_spec['uuid']
        uploader_wrapper = UploadMessageWrapper(uuid, no_query=no_query)
        wrapped_upload_file_to_uuid = uploader_wrapper.wrap_upload_function(
            upload_file_to_uuid, file_path
        )
        file_metadata = wrapped_upload_file_to_uuid(
            filename=file_path, uuid=uuid, auth=auth
        )
        if file_metadata:
            extra_files_credentials = file_metadata.get("extra_files_creds", [])
            if extra_files_credentials:
                upload_extra_files(
                    extra_files_credentials,
                    uploader_wrapper,
                    folder,
                    auth,
                    recursive=subfolders,
                )


def search_for_file(directory, file_name, recursive=False):
    """Search for file within directory.

    :param directory: Directory path
    :param file_name: Name of file to find
    :param recursive: Whether to search sub-directories of given
        directory
    :returns: (Path to file or None, Error message or None)
    """
    file_path_found = None
    msg = None
    file_path = os.path.join(directory, file_name)
    file_search = glob.glob(file_path, recursive=recursive)
    if len(file_search) == 1:
        [file_path_found] = file_search
    elif len(file_search) > 1:
        msg = (
            "No upload attempted for file %s because multiple copies were found"
            " in folder %s: %s."
            % (file_name, directory, ", ".join(file_search))
        )
    else:
        file_path_found = file_path
    return file_path_found, msg


class UploadMessageWrapper:
    """Class to provide consistent queries/messages to user when
    uploading file(s) to given File UUID.
    """

    def __init__(self, uuid, no_query=False):
        """Initialize instance for given UUID

        :param uuid: UUID of File item for uploads
        :param no_query: Whether to suppress asking for user
            confirmation prior to upload
        """
        self.uuid = uuid
        self.no_query = no_query

    def wrap_upload_function(self, function, file_name):
        """Wrap upload given function with messages conerning upload.

        :param function: Upload function to wrap
        :param file_name: File to upload
        :returns: Wrapped function
        """
        def wrapper(*args, **kwargs):
            result = None
            perform_upload = True
            if not self.no_query:
                if (
                    CGAP_SELECTIVE_UPLOADS
                    and not yes_or_no(f"Upload {file_name}?")
                ):
                    show("OK, not uploading it.")
                    perform_upload = False
            if perform_upload:
                try:
                    show("Uploading %s to item %s ..." % (file_name, self.uuid))
                    result = function(*args, **kwargs)
                    show(
                        "Upload of %s to item %s was successful."
                        % (file_name, self.uuid)
                    )
                except Exception as e:
                    show("%s: %s" % (e.__class__.__name__, e))
            return result
        return wrapper


def upload_extra_files(
    credentials, uploader_wrapper, folder, auth, recursive=False
):
    """Attempt upload of all extra files.

    Similar to "do_uploads", search for each file and then call a
    wrapped upload function. Here, since extra files do not correspond
    to Items on the portal, no need to PATCH an Item to retrieve AWS
    credentials; they are directly passed in from the parent File's
    metadata.

    :param credentials: AWS credentials dictionary
    :param uploader_wrapper: UploadMessageWrapper instance
    :param folder: Directory to search for files
    :param auth: CGAP authorization tuple
    :param recursive: Whether to search sub-directories for file
    """
    for extra_file_item in credentials:
        extra_file_name = extra_file_item.get("filename")
        extra_file_credentials = extra_file_item.get("upload_credentials")
        if not extra_file_name or not extra_file_credentials:
            continue
        extra_file_path, error_msg = search_for_file(
            folder, extra_file_name, recursive=recursive
        )
        if error_msg:
            show(error_msg)
            continue
        wrapped_execute_prearranged_upload = uploader_wrapper.wrap_upload_function(
            execute_prearranged_upload, extra_file_path
        )
        wrapped_execute_prearranged_upload(
            extra_file_path, extra_file_credentials, auth=auth
        )


def upload_item_data(item_filename, uuid, server, env, no_query=False):
    """
    Given a part_filename, uploads that filename to the Item specified by uuid on the given server.

    Only one of server or env may be specified.

    :param item_filename: the name of a file to be uploaded
    :param uuid: the UUID of the Item with which the uploaded data is to be associated
    :param server: the server to upload to (where the Item is defined)
    :param env: the beanstalk environment to upload to (where the Item is defined)
    :param no_query: bool to suppress requests for user input
    :return:
    """

    server = resolve_server(server=server, env=env)

    keydict = KEY_MANAGER.get_keydict_for_server(server)

    # print("keydict=", json.dumps(keydict, indent=2))

    if not no_query:
        if not yes_or_no("Upload %s to %s?" % (item_filename, server)):
            show("Aborting submission.")
            exit(1)

    upload_file_to_uuid(filename=item_filename, uuid=uuid, auth=keydict)
