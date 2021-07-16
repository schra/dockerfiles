# This file is originally by Jessie Frazelle and licensed under the MIT
# license.
#
# https://github.com/jessfraz/dockerfiles/blob/8ff991327fd1c68369c2fb576215d0eabffca0e1/spotify/Dockerfile

FROM debian:sid-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    dirmngr \
    gnupg \
 && curl -sS https://download.spotify.com/debian/pubkey_0D811D58.gpg | apt-key add -  \
 && echo "deb http://repository.spotify.com stable non-free" >> /etc/apt/sources.list.d/spotify.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    alsa-utils \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libpulse0 \
    libsm6 \
    spotify-client \
    xdg-utils \
 && rm -rf /var/lib/apt/lists/*

ENV HOME /home/spotify
RUN useradd --create-home --home-dir $HOME spotify \
 && gpasswd -a spotify audio \
 && chown -R spotify:spotify $HOME

WORKDIR $HOME
USER spotify

# make search bar text better
RUN echo "QLineEdit { color: #000 }" > /home/spotify/spotify-override.css

ENTRYPOINT [ "spotify" ]
CMD [ "-stylesheet=/home/spotify/spotify-override.css" ]
