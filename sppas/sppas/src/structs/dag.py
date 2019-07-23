# -*- coding: UTF-8 -*-
"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    annotations.dag.py
    ~~~~~~~~~~~~~~~~~~

"""


class DAG(object):
    """Direct Acyclic Graph.

    Implementation inspired from: http://www.python.org/doc/essays/graphs/

    """

    def __init__(self):
        """Create a new DAG instance.

        This class represents the DAG as a dictionary.
        For example:
            - A -> B
            - A -> C
            - B -> C
            - B -> D
            - C -> D
        will be represented as:
        {'A': ['B', 'C'], 'B': ['C', 'D'], 'C': ['D'],}

        """
        self.__graph = dict()

    # -----------------------------------------------------------------------

    def __get(self):
        return self.__graph

    def __set(self, dag):
        self.__graph = dag

    Graph = property(__get, __set)

    # -----------------------------------------------------------------------

    def add_node(self, node):
        """Add a new node (not added if already in the DAG)."""

        if node not in self.__graph.keys():
            self.__graph[node] = list()

    def add_edge(self, src, dst):
        """Add a new edge to a node."""

        # TODO. Must check if no cycle...
        self.__graph[src].append(dst)

    def remove_node(self, node):
        """Remove a node."""

        if node in self.__graph.keys():
            del self.__graph[node]

    def remove_edge(self, src, dst):
        self.__graph[src].pop(dst)

    # -----------------------------------------------------------------------

    def find_path(self, start, end, path=[]):
        """Determine a path between two nodes.

        It takes a graph and the start and end nodes as arguments. It
        will return a list of nodes (including the start and end nodes)
        comprising the path. When no path can be found, it returns None.
        Note: The same node will not occur more than once on the path
        returned (i.e. it won't contain cycles).

            >>> find_path(graph, 'A', 'C')
            >>> ['A', 'B', 'C']
        """
        path += [start]
        if start == end:
            return [path]
        if start not in self.__graph:
            return []

        for node in self.__graph[start]:
            if node not in path:
                new_path = self.find_path(node, end, path)
                if len(new_path) > 0:
                    return new_path
        return []

    # -----------------------------------------------------------------------

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.__graph:
            return []

        paths = []
        for node in self.__graph[start]:
            if node not in path:
                new_paths = self.find_all_paths(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)

        return paths

    # -----------------------------------------------------------------------

    def find_shortest_path(self, start, end, path=[]):
        path += [start]
        if start == end:
            return path
        if start not in self.__graph.keys():
            return None

        shortest = None
        for node in self.__graph[start]:
            if node not in path:
                new_path = self.find_shortest_path(node, end, path)
                if new_path:
                    if not shortest or len(new_path) < len(shortest):
                        shortest = new_path

        return shortest

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __repr__(self):
        print("Number of nodes: {:d}".format(len(self.__graph.keys())))
        for i in self.__graph.keys():
            if self.__graph[i]:
                print("  Node {} has edge to --> {}"
                      "".format(i, self.__graph[i]))
            else:
                print("  Node {} has no edge ".format(i))

    def __len__(self):
        """Return the length of the DAG."""
        return len(self.__graph)
