ARG $registry=
FROM ${registry}archlinux-makepkg

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
