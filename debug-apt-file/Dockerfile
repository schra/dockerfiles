ARG tag
FROM ubuntu:$tag

RUN apt-get update \
 && apt-get install --yes --no-install-recommends apt-file \
 && apt-file update

ENTRYPOINT [ "apt-file" ]
