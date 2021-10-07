from gevent import monkey
# Calling monkey patch to handle incoming requests concurrently
# This method is called before all imports which use ssl to avoid ssl errors
monkey.patch_all()

from flask import Flask, request
import subprocess
import logging
import os
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
import app_config


# Folders config
if not os.path.exists(app_config.CERTS_FOLDER):
    os.mkdir(app_config.CERTS_FOLDER)

if not os.path.exists(app_config.LOG_FOLDER):
    os.mkdir(app_config.LOG_FOLDER)

# logging config
logging.basicConfig(
    level=logging.DEBUG,
    filename=app_config.LOG_FILE,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    filemode="a",
)
logger = logging.getLogger(__name__)

# App Config
app = Flask(__name__)
app.config.from_object(app_config)


@app.before_request
def before_request():
    if not request.json:
        message = "Invalid Request. No request headers were given."
        logger.error(message)
        return {"output": message}, app_config.POST_REQUEST_STATUS_CODE

    if not (request.json.get("user") and request.json.get("group") and request.json.get("time") and request.json.get("key")):
        message = "Invalid Request. Missing request headers."
        logger.error(message)
        return {"output": message}, app_config.POST_REQUEST_STATUS_CODE
    
    if request.json.get("key") != app_config.SHAN_SERVER_SECRET_KEY:
        message = "You are not authorized to perform this operation."
        logger.error(message)
        return {"output": message}, app_config.POST_REQUEST_STATUS_CODE


@app.route("/", methods=["POST"])
def index():
    """POST method for "/" route for Server2 flask application.

    POST: Runs the elevation script for a given AD user, AD group and
    elevation time passed in the request body and returns dictionary/json
    showing the result of the the elevation script.
    """
    output = "Unknown error occurred. Please contact your Administrator."

    user_name = request.json.get("user")
    group_name = request.json.get("group")
    elevation_time = request.json.get("time")

    if not user_name or not group_name or not elevation_time:
        message = "Invalid Request. Request headers are empty"
        logger.error(message)
        return {"output": message}, app_config.POST_REQUEST_STATUS_CODE

    command = (
        "powershell -executionPolicy bypass -file "
        + "\""
        + app_config.POWERSHELL_SCRIPT_FILE
        + "\" \""
        + app_config.ELIGIBILITY_GROUPS_FILE
        + "\" "
        + user_name
        + " "
        + group_name
        + " "
        + elevation_time
    )

    resp = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    out = resp.stdout.read().decode("utf-8")
    if len(out) > len("ShanPowershell1") + 2:
        logger.error(out)
    else:
        logger.debug(out)

    if "ShanPowershell1" in out:
        output = "You are not authorized to perform this operation as you are not part of the Eligibility Group."
    elif "ShanPowershell2" in out:
        output = "AD is not reachable."
    elif "ShanPowershell3" in out:
        output = user_name + " is already a member of " + group_name + " group."
    elif "ShanPowershell4" in out:
        output = "You have been elevated to " + group_name + " group successfully."
    elif "ShanPowershell5" in out:
        output = "You have insufficient access rights to perform the operation."
    elif "ShanPowershell6" in out:
        output = "Please contact your administrator as there are issues with group configuration(s)."

    logger.debug(output)

    return {"output": output}, app_config.POST_REQUEST_STATUS_CODE


if __name__ == "__main__":

    if not os.path.exists(app_config.APP_FOLDER_PATH):
        logger.error("The repo shan-api-server is not cloned inside C:\\Program Files folder.")
    else:
        # If shan-api-server repo is configured in correct location

        logger.info("The repo shan-api-server is configured in correct location")

        for file in os.listdir(app_config.CERTS_FOLDER):
            if file.endswith("-chain.pem"):
                app_config.CERTS_CHAIN_FILE = app_config.CERTS_FOLDER + file
            elif file.endswith("-key.pem"):
                app_config.KEY_FILE = app_config.CERTS_FOLDER + file

        if not app_config.CERTS_CHAIN_FILE:
            logger.error(
                "Certificate chain file not found. Please refer ReadME for certificate configuration."
            )
        elif not app_config.KEY_FILE:
            logger.error(
                "Certificate key file not found. Please refer ReadME for certificate configuration."
            )
        else:
            logger.info("Starting WSGI server...")
            spawn = Pool(app_config.MAX_NUMBER_OF_REQUESTS)
            https_server = WSGIServer(
                (app_config.HTTPS_SERVER, app_config.HTTPS_PORT),
                app,
                keyfile=app_config.KEY_FILE,
                certfile=app_config.CERTS_CHAIN_FILE,
                spawn=spawn
            )
            https_server.serve_forever()

            logger.info("WSGI server is running...")
