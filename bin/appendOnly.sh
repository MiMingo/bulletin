#!/bin/bash

usage() {
  echo "Usage: $0 (start)"
}

init_start() {
  ./STAR-Vote/.cabal-sandbox/bin/bbserver -b :: -p 8000
}

# init_status() {
#   if lsof -i :8000 &>/dev/null; then
#     echo "search server running"
#   fi
# }

# init_stop() {
#   echo "stopping search server ..."
#   pid=$(lsof -ti:8000)
#   echo "+ kill -9 ${pid}"
#   kill -9 ${pid}
# }


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