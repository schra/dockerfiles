#!/usr/bin/env bash

# Build and optionally push a Docker image.

set -Eeuo pipefail

args=$(getopt -o 'i:p:' --long 'image:,image-name:,push:' -- "$@")
eval "set -- $args"

while true; do
  case $1 in
  -p | --push)
    registry=$2
    shift 2
    ;;
  -i | --image | --image-name)
    image_path=$2
    shift 2
    ;;
  --)
    shift
    break
    ;;
  *)
    exit 1
    ;;
  esac
done

trap 'echo >&2 $0: line $LINENO: $BASH_COMMAND: Failed with status $?' ERR

image_name=$(basename "$(realpath "$image_path")")

# TODO: The tag file is just a quick hack.
if [ -f "$image_path/tags" ]; then
  mapfile -t tags < "$image_path"/tags
else
  tags=(latest)
fi

for tag in "${tags[@]}"; do

  if [[ -v registry ]]; then
    # e.g. in spotify/ we need --no-cache because the Spotify app might
    # update without the parent image updating
    docker build "$image_path" --pull --tag "$registry/$image_name:$tag" --no-cache --build-arg registry="$registry/" --build-arg "tag=$tag"
    docker push "$registry/$image_name:$tag"
  else
    docker build "$image_path" --pull --tag "$image_name" --build-arg registry= --build-arg "tag=$tag"
  fi

done
