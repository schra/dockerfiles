FROM archlinux

RUN pacman -Sy --noconfirm --needed \
# > Packages in the AUR assume that the base-devel group is installed, i.e.
# > they do not list the group's members as build dependencies explicitly.
#
# https://wiki.archlinux.org/index.php/Arch_User_Repository
      base-devel \
# Some PKGBUILDs use Git repos as a source
      git \
 && rm -R /var/cache/pacman/pkg/* /var/lib/pacman/sync/*

# makepkg requires to be run with a non-root user. thus provide one
RUN useradd --create-home --shell /usr/bin/bash makepkg \
# makepkg must be executed without any interactive input in Dockerfiles, thus
# allow to execute sudo without a password
 && echo 'makepkg ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Install makepkg
RUN su makepkg -c 'gpg --keyserver keyserver.ubuntu.com --recv-keys 465022E743D71E39' \
 && cd /tmp \
 && su makepkg -c 'git clone https://aur.archlinux.org/aurman.git' \
 && cd /tmp/aurman \
 && pacman -Sy \
 && su aurman -c 'makepkg --noconfirm --rmdeps -si' \
 && rm -Rf /tmp/aurman \
 && rm -R /var/cache/pacman/pkg/* /var/lib/pacman/sync/*

COPY aurman_config /home/aurman/.config/aurman/aurman_config
