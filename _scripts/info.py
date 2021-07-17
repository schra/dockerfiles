#!/usr/bin/env python3

# List all Docker images in this repo as a JSON array with additional info.

import pathlib
import json
import argparse

def get_image_dependency(dir):
    for line in (dir / "Dockerfile").read_text().splitlines():
        if "FROM" in line:
            if "${registry}" in line:
                return line.split("}")[1]
            else:
                return None

def docker_images_info(repo_path):
    info = []
    for dir in (x for x in repo_path.iterdir() if x.is_dir() and x.name != "_scripts" and not x.name.startswith(".")):
        info.append({
            "name": dir.name,
            "dependency": get_image_dependency(dir)
        })
    return info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo_path', type=pathlib.Path, help="Path to the repo root.")
    args = parser.parse_args()
    print(json.dumps(docker_images_info(args.repo_path)))

if __name__ == '__main__':
    main()
