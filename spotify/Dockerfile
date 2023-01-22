# This file is originally by Jessie Frazelle and is licensed under the MIT
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
# See https://www.spotify.com/us/download/linux/ for the installation instructions
 && curl -sS https://download.spotify.com/debian/pubkey_7A3A762FAFD4A51F.gpg | gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/spotify.gpg \
 && echo "deb http://repository.spotify.com stable non-free" | tee /etc/apt/sources.list.d/spotify.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    alsa-utils \
    libgl1-mesa-dri \
    libgl1-mesa-glx \
    libpulse0 \
    libsm6 \
    spotify-client \
    xdg-utils \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
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
