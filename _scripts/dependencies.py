#!/usr/bin/env python3

# Generate dependency information of the Docker images in this repo. This is
# needed in the CI.
#
# The CI for the official Docker images
# (https://github.com/docker-library/bashbrew) doesn't fit my usage scenario.

import pathlib
import json
import argparse
import graphlib


def dockerfile_dependencies(dockerfile_path):
    deps = set()
    for line in dockerfile_path.read_text().splitlines():
        if line.startswith("FROM ${registry}"):
            deps.add(line.split("}")[-1])
    return deps


def dockerfiles_dependency_graph(repo_path):
    dependency_graph = {}
    for dir in (x for x in repo_path.iterdir() if x.is_dir() and x.name != "_scripts" and not x.name.startswith(".")):
        dependency_graph[dir.name] = dockerfile_dependencies(
            dir / "Dockerfile")
    return dependency_graph


def dfs(graph, node_to_visit, visited_nodes=None):
    if visited_nodes is None:
        visited_nodes = set()
    visited_nodes.add(node_to_visit)
    for node in graph[node_to_visit]:
        if node not in visited_nodes:
            dfs(graph, node, visited_nodes)
    return visited_nodes


def make_undirected(graph):
    # Idea: Duplicate the graph but with reverted edges.

    reversed_graph = {}
    for node, edges in graph.items():
        for edge in edges:
            reversed_graph.setdefault(edge, []).append(node)

    # now merge the graphs
    undirected_graph = {}
    for node in set(graph.keys()).union(reversed_graph.keys()):
        undirected_graph[node] = graph.get(node, set()).union(
            reversed_graph.get(node, set()))
    return undirected_graph


def get_graph_components(dependency_graph):
    # Idea: Make the graph undirected. Then do a DFS to find each component.
    # Remove the component/ subgraph from the overall graph and continue.

    undirected_dependency_graph = make_undirected(dependency_graph)

    components = []
    while dependency_graph != {}:
        random_next_node = list(dependency_graph.keys())[0]
        component_nodes = dfs(undirected_dependency_graph, random_next_node)
        component_graph = {}

        # remove the subgraph component_nodes from the graph dependency_graph
        for node in component_nodes:
            component_graph[node] = dependency_graph[node]
            del dependency_graph[node]
            del undirected_dependency_graph[node]
            for dep_node in dependency_graph.keys():
                if node in dependency_graph[dep_node]:
                    dependency_graph[dep_node].remove(node)
                    undirected_dependency_graph[dep_node].remove(node)

        components.append(component_graph)
    return components


def topological_sort(dependency_graph):
    return list(graphlib.TopologicalSorter(dependency_graph).static_order())


def github_actions_matrix(dependency_graph):
    # Idea: We want to parallelize building the Docker images as much as
    # possible.
    return map(topological_sort, get_graph_components(dependency_graph))


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dependencies', action='store_true')
    group.add_argument('--github-actions-matrix', action='store_true')
    parser.add_argument('repo_path', type=pathlib.Path,
                        help="Path to the repo root.")

    args = parser.parse_args()

    dependencies = dockerfiles_dependency_graph(args.repo_path)

    if args.dependencies:
        print(json.dumps(dependencies))
    elif args.github_actions_matrix:
        print(json.dumps([" ".join(x)
              for x in github_actions_matrix(dependencies)]))


if __name__ == '__main__':
    main()
