#!/usr/bin/env python3

# List all Docker images in this repo as a json array.

import pathlib
import json
import argparse

def list_docker_images(repo_path):
    return [x.name for x in repo_path.iterdir() if x.is_dir() and x.name != "_scripts" and not x.name.startswith(".")]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo_path', type=pathlib.Path, help="Path to the repo root.")
    args = parser.parse_args()
    print(json.dumps(list_docker_images(args.repo_path)))

if __name__ == '__main__':
    main()
