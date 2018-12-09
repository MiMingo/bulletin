#!/bin/bash

usage() {
  echo "Usage: $0 (start)"
}

init_start() {
  ./STAR-Vote/.cabal-sandbox/bin/bbserver -b :: -p 8000
}

if [ $# -ne 1 ]; then
  usage
  exit 1
fi

case $1 in
  "start")
    init_start
    ;;
#   "status")
#     init_status
#     ;;
#   "restart")
#     init_stop
#     init_start
#     ;;
#   "stop")
#     init_stop
#     ;;
  *)
    usage
    exit 1
    ;;
esac