#!/bin/bash

echo "saas_shorturl"

INITAL_DIR=$(pwd)

cd ..
source ./_repo_vars.sh
cd ${INITAL_DIR}

SAAS_APIAPP_MASTERPASSWORDFORPASSHASH=wefgFvGFt5433e

# 8099 is hard coded in the saas_user_management container (Shared functions)
#  compiled into the webapp in the part where it identifies backend api
#  in this project in saasLinkvisCallapi.js
EXTPORT80FORSECURITY=8099

PYTHON_CMD=python
# We are using venv - see source command velow
#if [ E${EXTPYTHONCMD} != "E" ]; then
#  PYTHON_CMD=${EXTPYTHONCMD}
#fi

#pyCharm will run in project root directory. Check if we are here and if so then change int oservices directory
if [ -d "./services" ]; then
  echo "Changing into services directory"
  cd ./services
fi

PYTHONVERSIONCHECKSCRIPT="import sys\nprint(\"Python version \" + str(sys.version_info))\nif sys.version_info[0] < 3:\n  exit(1)\nif sys.version_info[0] == 3:\n  if sys.version_info[1] < 6:\n    exit(1)\nexit(0)\n"
printf "${PYTHONVERSIONCHECKSCRIPT}" | ${PYTHON_CMD}
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Wrong python version - this version won't have all the required libraries"
  echo "Using command ${PYTHON_CMD}"
  echo "you can set enviroment variable EXTPYTHONCMD to make this script use a different python command"
  echo ""
  exit 1
fi

if [ E${EXTURL} = "E" ]; then
  echo "EXTURL not set"
  exit 1
fi
if [ E${EXTPORT} = "E" ]; then
  echo "EXTPORT not set"
  exit 1
fi
if [ E${EXTPORT80} = "E" ]; then
  echo "EXTPORT80 not set"
  exit 1
fi

APP_DIR=.

export APIAPP_MODE=DEVELOPER
export APIAPP_JWTSECRET="gldskajld435sFFkfjlkfdsj"
export APIAPP_JWTSKIPSIGNATURECHECK=N
export APIAPP_FRONTEND=_
export APIAPP_APIURL=${EXTURL}:${EXTPORT}/api
export APIAPP_APIDOCSURL=${EXTURL}:${EXTPORT}/apidocs
export APIAPP_FRONTENDURL=${EXTURL}:${EXTPORT}/frontend
export APIAPP_APIACCESSSECURITY=[]
export APIAPP_PORT=8096
##export APIAPP_OBJECTSTORECONFIG="{\"Type\":\"Memory\"}"
export APIAPP_OBJECTSTORECONFIG="{\"Type\": \"SimpleFileStore\",\"BaseLocation\": \"./objectstoredata\"}"
export APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN="http://localhost:8080"

# Shorturl specific params
export APIAPP_REDIRECTPREFIX="http://rjmd.uk"
export APIAPP_URLEXPIREDAYS="366"
export APIAPP_DESTWHITELIST="{\"challengeappDEV\":[\"http://localhost\"],\"challengeapp\":[\"https://challengewsipe.com/#/challengeapp/\"],\"challengeappstage\":[\"https://challengewsipe.com/#/challengeappstage/\"]}"

export APIAPP_VERSION=
if [ -f ${APP_DIR}/VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/VERSION)
fi
if [ -f ${APP_DIR}/../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../VERSION)
fi
if [ -f ${APP_DIR}/../../VERSION ]; then
  APIAPP_VERSION=${0}-$(cat ${APP_DIR}/../../VERSION)
fi
if [ E${APIAPP_VERSION} = 'E' ]; then
  echo 'Can not find version file in standard locations'
  exit 1
fi

SETUP_JSON_DIR=${INITAL_DIR}
SETUP_JSON_FILENAME="_start_local_saas_user_management_service_config.json"
EXPECTED_TENANT="challengeappDEV"
EXTERNAL_VOLUME=""
APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN_FOR_USER_MANAGEMENT="http://localhost"


# Start security service (if not already running)
start_local_saas_user_management_service \
   ${RJM_USERMANAGEMENT_CONTAINER} \
   ${APIAPP_JWTSECRET} \
   ${EXTURL} \
   ${EXTPORT} \
   ${EXTPORT80FORSECURITY} \
   ${SAAS_APIAPP_MASTERPASSWORDFORPASSHASH} \
   "${APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN_FOR_USER_MANAGEMENT}" \
   ${SETUP_JSON_DIR} \
   ${SETUP_JSON_FILENAME} \
   ${EXPECTED_TENANT} \
   "${EXTERNAL_VOLUME}"
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "Error starting security microservice"
  echo ""
  exit 1
fi

#Python app reads parameters from environment variables
${PYTHON_CMD} ./src/app.py
RES=$?

if [ $RES -ne 0 ]; then
  echo "Process Errored"
  read -p "Press enter to continue"
fi
