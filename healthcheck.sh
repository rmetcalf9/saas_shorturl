#!/bin/bash

curl -f http://127.0.0.1:80/public/api/info/serverinfo?healthcheck=true || exit 1
RES=$?
if [ ${RES} -ne 0 ]; then
  echo "healthcheck.sh - failed python app"
  exit 1
fi

exit 0
