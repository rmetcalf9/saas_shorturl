#!/bin/bash

#Not used by codefresh as I am using build container instead

#working directory is always saas_shorturl root
GITROOT=$(pwd)
DOCKER_USERNAME=metcarob
DOCKER_IMAGENAME=saas_shorturl
VERSIONNUM=$(cat ./VERSION)
QUASARBUILDIMAGE="metcarob/docker-build-quasar-app:0.0.12"

#could be spa or pwa
QUASARBUILDMODE=pwa

docker image inspect ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}_localbuild > /dev/null
RES=$?
if [ ${RES} -eq 0 ]; then
  docker rmi ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}_localbuild
  RES2=$?
  if [ ${RES2} -ne 0 ]; then
    echo "Image exists and delete failed"
    exit 1
  fi
fi

echo "There is no frontend for this service"

echo "Build docker container (VERSIONNUM=${VERSIONNUM})"
#This file does no version bumping
cd ${GITROOT}
eval docker build . -t ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}_localbuild
RES=$?
if [ ${RES} -ne 0 ]; then
  echo ""
  echo "Docker build failed"
  exit 1
fi

exit 0
