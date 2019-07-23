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

    src.models.acm.tiedlist.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import codecs
from sppas.src.config import sg

# ---------------------------------------------------------------------------


class sppasTiedList(object):
    """Tiedlist of an acoustic model.

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      develop@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi

    This class is used to manage the tiedlist of a triphone acoustic model,
    i.e:
        - the list of observed phones, biphones, triphones,
        - a list of biphones or triphones to tie.

    """

    def __init__(self):
        """Create a sppasTiedList instance."""
        self.observed = list()
        self.tied = dict()

    # -----------------------------------------------------------------------

    def read(self, filename):
        """Read a tiedlist from a file and set it.

        :param filename: (str)

        """
        with codecs.open(filename, 'r', sg.__encoding__) as fd:
            for nbl, line in enumerate(fd, 1):
                line = line.strip()
                try:
                    tab = line.split(' ')
                    if len(tab) == 1:
                        self.add_observed(line)
                    elif len(tab) == 2:
                        self.add_tied(tab[0].strip(), tab[1].strip())
                    else:
                        raise ValueError('Unexpected entry at line %d: %r'
                                         '' % (nbl, tab))
                except Exception as e:
                    raise IOError("Read file failed due to the following "
                                  "error at line %d: %s" % (nbl, str(e)))

    # -----------------------------------------------------------------------

    def save(self, filename):
        """Save the tiedlist into a file.

        :param filename: Name of the file of the tiedlist

        """
        with codecs.open(filename, 'w', sg.__encoding__) as fp:

            for triphone in self.observed:
                fp.write(triphone + "\n")

            for k, v in sorted(self.tied.items()):
                fp.write(k + " " + v + "\n")

    # -----------------------------------------------------------------------

    def is_empty(self):
        """Return True if the tiedlist is empty."""
        return len(self.observed) == 0 and len(self.tied) == 0

    # -----------------------------------------------------------------------

    def is_observed(self, entry):
        """Return True if entry is really observed (not tied!).

        :param entry: (str) triphone/biphone/monophone

        """
        return entry in self.observed

    # -----------------------------------------------------------------------

    def is_tied(self, entry):
        """Return True if entry is tied.

        :param entry: (str) a triphone/biphone/monophone

        """
        return entry in self.tied

    # -----------------------------------------------------------------------

    def add_tied(self, tied, observed=None):
        """Add an entry into the tiedlist.

        If observed is None, an heuristic will assign one.

        :param tied: (str) the biphone/triphone to add,
        :param observed: (str) the biphone/triphone to tie with.
        :returns: bool

        """
        if tied in self.tied or tied in self.observed:
            return False

        if observed is None:
            # Which type of entry?
            if tied.find("+") == -1:
                # NOT either a biphone or triphone
                return False
            if tied.find("-") == -1:
                return self.__add_biphone(tied)
            return self.__add_triphone(tied)

        self.tied[tied] = observed
        return True

    # -----------------------------------------------------------------------

    def add_to_tie(self, entries):
        """Add several un-observed entries in the tiedlist.

        :param entries: (list)
        :returns: list of entries really added into the tiedlist

        """
        add_entries = list()
        for entry in entries:
            if self.is_observed(entry) is False and \
                    self.is_tied(entry) is False:
                ret = self.add_tied(entry)
                if ret is True:
                    add_entries.append(entry)
        return add_entries

    # -----------------------------------------------------------------------

    def add_observed(self, entry):
        """Add an observed entry.

        :param entry: (str)
        :returns: bool

        """
        if entry not in self.observed:
            self.observed.append(entry)
            return True
        return False

    # -----------------------------------------------------------------------

    def merge(self, other):
        """Merge self with another tiedlist.

        :param other: (sppasTiedList)

        """
        if isinstance(other, sppasTiedList) is False:
            raise TypeError('A sppasTiedList can only be merged with '
                            'another sppasTiedList. '
                            'Got {:s}.'.format(type(other)))

        for obs in other.observed:
            self.add_observed(obs)

        for tie, obs in other.tied.items():
            self.add_tied(tie, obs)

    # -----------------------------------------------------------------------

    def remove(self, entry, propagate=False):
        """Remove an entry of the list of observed or tied entries.

        :param entry: (str) the entry to be removed
        :param propagate: (bool) if entry is an observed item, remove all tied
        that are using this observed item.

        """
        if entry in self.observed:
            self.observed.remove(entry)
            if propagate is True:
                for k, v in self.tied.items():
                    if v == entry:
                        self.tied.pop(k)

        if entry in self.tied.keys():
            self.tied.pop(entry)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __find(self, tied):
        """Find which observed model will match to tie the given entry.

        :param tied: (str) the model to be tied
        :returns: the observed model to tie with.

        """
        observed = ""
        frqtied = {}
        for v in self.tied.values():
            if v.find(tied) > -1:
                # Caution: a biphone can only be tied with a biphone
                if tied.find("-") == -1 and v.find("-") > -1:
                    pass
                else:
                    if v in frqtied:
                        frqtied[v] = frqtied[v] + 1
                    else:
                        frqtied[v] = 1
        frqmax = 0
        for p, f in frqtied.items():
            if f > frqmax:
                frqmax = f
                observed = p

        return observed

    # -----------------------------------------------------------------------

    def __add_triphone(self, entry):
        """Add an observed model to tie with the given entry.

        :param entry: (str) the model to be tied
        :returns: (bool)

        """
        # Get the biphone to tie
        biphone = entry[entry.find('-')+1:]
        observed = self.__find(biphone)

        if len(observed) == 0:
            # Get the monophone to tie
            monophone = entry[entry.find('-'):entry.find('+')+1]
            observed = self.__find(monophone)
            if len(observed) == 0:
                return False

        self.tied[entry] = observed

        return True

    # -----------------------------------------------------------------------

    def __add_biphone(self, entry):
        """Add an observed model to tie with the given entry.

        :param entry: (str) the model to be tied
        :returns: (bool)

        """
        # Get the monophone to tie
        monophone = entry[:entry.find('+')+1]
        observed = self.__find(monophone)
        if len(observed) == 0:
            return False

        self.tied[entry] = observed

        return True
