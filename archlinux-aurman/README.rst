archlinux-aurman
================

This image provides the AUR helper `aurman <https://github.com/polygamma/aurman>`_.

Usage::

  # Download the package database, otherwise aurman yields weird errors.
  pacman -Sy

  su makepkg -c 'aurman -S [package-to-install]'
