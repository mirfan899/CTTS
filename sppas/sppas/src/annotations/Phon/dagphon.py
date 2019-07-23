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

    src.annotations.dagphon.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    A Direct Acyclic Graph is used to phonetize unknown entries.

"""
import re

from sppas.src.config import separators
from sppas.src.structs.dag import DAG

# ----------------------------------------------------------------------------


class sppasDAGPhonetizer(object):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Utility class to manage phonetizations with a DAG.

    """
    def __init__(self, variants=4):
        """Create a sppasDAGPhonetizer instance.

        :param variants: (int) Maximum number of variants for phonetizations.

        """
        self.variants = 0
        self.set_variants(variants)

    # -----------------------------------------------------------------------

    def set_variants(self, v):
        """Fix the maximum number of variants.

        :param v: (int) If v is set to 0, all variants will be returned.

        """
        if v < 0 or v > 20:
            raise ValueError('Unexpected value for the number of variants.')
        self.variants = v

    # -----------------------------------------------------------------------

    def phon2DAG(self, pron):
        """Convert a phonetization into a DAG.

        :param pron:

        """
        tabpron = pron.split()
        graph = DAG()        # the Graph: store segments and get all paths
        prongraph = list()   # the pronunciation of each segment

        # A Start node (required if the 1st segment has variants)
        graph.add_node(0)
        prongraph.append("start")

        # Init values
        prec = 1
        precv = 1

        # Get all longest-segments of a token
        for i in range(len(tabpron)):

            variants = tabpron[i].split(separators.variants)
            # Get all variants of this part-of-token
            for v in range(len(variants)):

                # store variants
                prongraph.append(variants[v])
                if i < len(tabpron):
                    graph.add_node(prec+v)
                # add these variants to the preceding segments
                for k in range(prec-precv, prec):
                    graph.add_edge(k, prec+v)

            prec += len(variants)
            precv = len(variants)

        # add a "End" node
        prongraph.append("end")
        graph.add_node(prec)

        for k in range(prec-precv, prec):
            graph.add_edge(k, prec)

        return graph, prongraph

    # -----------------------------------------------------------------------

    def DAG2phon(self, graph, pron_graph):
        """Convert a DAG into a dict, including all pronunciation variants.

        :param graph:
        :param pron_graph:
        :returns:

        """
        pathslist = graph.find_all_paths(0, len(graph)-1)

        pron = dict()
        for variant in pathslist:
            p = ""
            for i in variant[1:len(variant)-1]:  # ignore Start and End nodes
                p = p + separators.phonemes + pron_graph[i]
            p = re.sub('^.', "", p)
            pron[p] = len(p.split(separators.phonemes))

        return pron

    # -----------------------------------------------------------------------

    def decompose(self, pron1, pron2=""):
        """Create a decomposed phonetization from a string as follow:

            >>> self.decompose("p1 p2|x2 p3|x3")
            >>> p1-p2-p3|p1-p2-x3|p1-x2-p3|p1-x2-x3

        The input string is converted into a DAG, then output corresponds
        to all paths.

        """
        if len(pron1) == 0 and len(pron2) == 0:
            return ""

        # Complex phonetization: converted into a DAG
        (graph1, prongraph1) = self.phon2DAG(pron1)
        (graph2, prongraph2) = DAG(), list()
        if len(pron2) > 0:
            (graph2, prongraph2) = self.phon2DAG(pron2)

        # Create all pronunciations from the DAG
        pron1 = self.DAG2phon(graph1, prongraph1)
        if len(pron2) > 0:
            pron2 = self.DAG2phon(graph2, prongraph2)
        else:
            pron2 = dict()

        # Merge =======>
        # TODO: MERGE DAGs instead of merging prons
        pron = dict()
        pron.update(pron1)
        pron.update(pron2)

        # Output selection

        v = separators.variants

        # Return all variants
        if self.variants == 0:
            return v.join(pron.keys())

        # Choose the shorter variants
        if self.variants == 1:
            return min(pron.items(), key=lambda x: x[1])[0]

        # Other number of variants: choose shorters
        ll = sorted(pron.items(), key=lambda x: x[1])[:self.variants]
        return v.join(list(zip(*ll))[0])
