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

    src.models.acm.hmm.py
    ~~~~~~~~~~~~~~~~~~~~~

"""
import collections
import copy
import json

from sppas.src.utils.makeunicode import basestring
from ..modelsexc import ModelsDataTypeError

# ---------------------------------------------------------------------------


class sppasHMM(object):
    """HMM representation for one phone.

    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :author:       Brigitte Bigi
    :contact:      develop@sppas.org

    Hidden Markov Models (HMMs) provide a simple and effective framework for
    modeling time-varying spectral vector sequences. As a consequence, most
    of speech technology systems are based on HMMs.
    Each base phone is represented by a continuous density HMM, with transition
    probability parameters and output observation distributions.
    One of the most commonly used extensions to standard HMMs is to model the
    state-output distribution as a mixture model, a mixture of Gaussians is a
    highly flexible distribution able to model, for example, asymmetric and
    multi-modal distributed data.

    An HMM-definition is made of:
        - state_count: int
        - states: list of OrderedDict with "index" and "state" as keys.
        - transition: OrderedDict with "dim" and "matrix" as keys.
        - options
        - regression_tree
        - duration

    """

    DEFAULT_NAME = "und"

    # -----------------------------------------------------------------------

    def __init__(self, name=DEFAULT_NAME):
        """Create a sppasHMM instance.

        The model includes a default name and an empty definition.

        :param name: (str) Name of the HMM (usually the phoneme in SAMPA)

        """
        self.__name = name
        self._definition = collections.OrderedDict()
        self.set_default_definition()

    # -----------------------------------------------------------------------

    def set(self, name, definition):
        """Set the model.

        :param name: (str) Name of the HMM
        :param definition: (OrderedDict) Definition of the HMM (states
        and transitions)

        """
        self.set_name(name)
        self.set_definition(definition)

    # -----------------------------------------------------------------------

    def get_name(self):
        """Return the name (str) of the model."""
        return self.__name

    # -----------------------------------------------------------------------

    def set_name(self, name):
        """Set the name of the model.

        :param name: (str) Name of the HMM.
        :raises: ModelsDataTypeError

        """
        if name is None:
            self.__name = sppasHMM.DEFAULT_NAME
        else:
            if isinstance(name, basestring) is False:
                raise ModelsDataTypeError("name of the HMM model",
                                          "string",
                                          type(name))
            self.__name = name

    # -----------------------------------------------------------------------

    def get_definition(self):
        """Return the definition (OrderedDict) of the model."""
        return self._definition

    # -----------------------------------------------------------------------

    def set_default_definition(self):
        """Set an empty definition."""
        self._definition = collections.OrderedDict()
        self._definition['state_count'] = 0
        self._definition['states'] = list()
        self._definition['transition'] = list()

    # -----------------------------------------------------------------------

    def set_definition(self, definition):
        """Set the definition of the model.

        :param definition: (OrderedDict) Definition of the HMM
        (states and transitions)
        :raises: ModelsDataTypeError

        """
        if isinstance(definition, collections.OrderedDict) is False:
            raise ModelsDataTypeError("definition of the HMM model",
                                      "collections.OrderedDict",
                                      type(definition))

        self._definition = definition

    # -----------------------------------------------------------------------

    def create(self, states, transition, name=None):
        """Create the hmm and set it.

        :param states: (OrderedDict)
        :param transition: (OrderedDict)
        :param name: (string) The name of the HMM.
        If name is set to None, the default name is assigned.

        """
        self.set_name(name)
        self.set_default_definition()

        self._definition['state_count'] = len(states) + 2
        self._definition['states'] = list()
        for i, state in enumerate(states):
            hmm_state = sppasHMM.create_default()
            hmm_state['index'] = i + 2
            hmm_state['state'] = state
            self._definition['states'].append(hmm_state)

        self._definition['transition'] = transition

    # -----------------------------------------------------------------------

    def create_proto(self, proto_size, nb_mix=1):
        """Create the 5-states HMM `proto` and set it.

        :param proto_size: (int) Number of mean and variance values.
        It's commonly either 25 or 39, it depends on the MFCC parameters.
        :param nb_mix: (int) Number of mixtures
        (i.e. the number of times means and variances occur)

        """
        # Fix the name and an empty definition
        self.__name = "proto"
        self.set_default_definition()

        # Fix the definition
        means = [0.0]*proto_size
        variances = [1.0]*proto_size

        # Define states
        self._definition['state_count'] = 5
        self._definition['states'] = list()
        for i in range(3):
            hmm_state = sppasHMM.create_default()
            hmm_state['index'] = i + 2
            hmm_state['state'] = sppasHMM.create_gmm([means]*nb_mix,
                                                     [variances]*nb_mix)
            self._definition['states'].append(hmm_state)

        # Define transitions
        self._definition['transition'] = sppasHMM.create_transition()

    # -----------------------------------------------------------------------

    def create_sp(self):
        """Create the 3-states HMM `sp` and set it.

        The `sp` model is based on a 3-state HMM with string "silst"
        as state 2, and a 3x3 transition matrix as follow:
           0.0 1.0 0.0
           0.0 0.9 0.1
           0.0 0.0 0.0

        """
        self.__name = "sp"
        self.set_default_definition()

        # Define states
        self._definition['state_count'] = 3
        self._definition['states'] = []
        hmm_state = sppasHMM.create_default()
        hmm_state['index'] = 2
        hmm_state['state'] = "silst"
        self._definition['states'].append(hmm_state)

        # Define transitions
        self._definition['transition'] = sppasHMM.create_transition([0.9])

    # -----------------------------------------------------------------------

    def get_state(self, index):
        """Return the state of a given index or None if index is not found.

        :param index: (int) State index (commonly between 1 and 5)
        :returns: collections.OrderedDict or None

        """
        states = self._definition['states']
        for item in states:
            if int(item['index']) == index:
                return item['state']

        return None

    # -----------------------------------------------------------------------

    def get_vecsize(self):
        """Return the number of means and variance of each state.

        If state is pointing to a macro, 0 is returned.

        """
        state = self._definition['states'][0]['state']

        # but a state can be either an OrderedDict or a string (to refer to a macro)
        if isinstance(state, collections.OrderedDict):
            return state['streams'][0]['mixtures'][0]['pdf']['mean']['dim']

        return 0

    # -----------------------------------------------------------------------

    def static_linear_interpolation(self, hmm, gamma):
        """Static Linear Interpolation.

        This is perhaps one of the most straightforward manner to combine models.
        This is an efficient way for merging the GMMs of the component models.

        Gamma coefficient is applied to self and (1-gamma) to the other hmm.

        :param hmm: (HMM) the hmm to be interpolated with.
        :param gamma: (float) coefficient to be applied to self.
        :returns: (bool) Status of the interpolation.

        """
        lin = HMMInterpolation()

        my_states = self._definition['states']
        other_states = hmm.definition['states']
        int_sts = lin.linear_states([my_states, other_states],
                                    [gamma, 1.-gamma])
        if int_sts is None:
            return False

        my_transition = self._definition['transition']
        other_transition = hmm.definition['transition']
        int_trs = lin.linear_transitions([my_transition, other_transition],
                                         [gamma, 1.-gamma])
        if int_trs is None:
            return False

        self._definition['states'] = int_sts
        self._definition['transition'] = int_trs

        return True

    # -----------------------------------------------------------------------

    @staticmethod
    def create_transition(state_stay_probabilities=(0.6, 0.6, 0.7)):
        """Create and return a transition matrix.

        :param state_stay_probabilities: (list) Center transition probabilities
        :returns: collections.OrderedDict()

        """
        n_states = len(state_stay_probabilities) + 2
        transitions = list()
        for i in range(n_states):
            transitions.append([0.]*n_states)
        transitions[0][1] = 1.
        for i, p in enumerate(state_stay_probabilities):
            transitions[i+1][i+1] = p
            transitions[i+1][i+2] = 1 - p

        return sppasHMM.create_square_matrix(transitions)

    # ----------------------------------

    @staticmethod
    def create_gmm(means, variances, gconsts=None, weights=None):
        """Create and return a GMM.

        :returns: collections.OrderedDict()

        """
        mixtures = list()

        if len(means[0]) == 1:
            means = means[None, :]
            variances = variances[None, :]

        gmm = sppasHMM.create_default()

        for i in range(len(means)):
            mixture = sppasHMM.create_default()
            mixture['pdf'] = sppasHMM.create_default()
            mixture['pdf']['mean'] = sppasHMM.create_vector(means[i])
            mixture['pdf']['covariance'] = sppasHMM.create_default()
            mixture['pdf']['covariance']['variance'] = \
                sppasHMM.create_vector(variances[i])

            if gconsts is not None:
                mixture['pdf']['gconst'] = gconsts[i]
            if weights is not None:
                mixture['weight'] = weights[i]
            else:
                mixture['weight'] = 1.0 / len(means)
            mixture['index'] = i + 1

            mixtures.append(mixture)

        stream = sppasHMM.create_default()
        stream['mixtures'] = mixtures
        gmm['streams'] = [stream]
        gmm['streams_mixcount'] = [len(means)]

        return gmm
    # -----------------------------------------------------------------------

    @staticmethod
    def create_default():
        """Create a default ordered dictionary, used for states.

        :returns: collections.OrderedDict()

        """
        return collections.OrderedDict()

    # ----------------------------------

    @staticmethod
    def create_vector(vector):
        """Create a default vector.

        :returns: collections.OrderedDict()

        """
        v = sppasHMM.create_default()
        v['dim'] = len(vector)
        v['vector'] = vector
        return v

    # ----------------------------------

    @staticmethod
    def create_square_matrix(matrix):
        """Create a default matrix.

        :returns: collections.OrderedDict()

        """
        m = sppasHMM.create_default()
        m['dim'] = len(matrix[0])
        m['matrix'] = matrix
        return m

    # -----------------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------------

    name = property(fget=get_name, fset=set_name, fdel=None, doc=None)
    definition = property(fget=get_definition, fset=set_definition,
                          fdel=None, doc=None)

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __repr__(self):
        return "Name:" + self.__name + "\n" + json.dumps(self._definition,
                                                         indent=2)

# ---------------------------------------------------------------------------
# Interpolation of HMMs.
# ---------------------------------------------------------------------------


class HMMInterpolation:
    """HMM interpolation.

    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :author:       Brigitte Bigi
    :contact:      develop@sppas.org

    """

    @staticmethod
    def linear_states(states, coefficients):
        """Linear interpolation of a set of states.

        :param states: (OrderedDict)
        :param coefficients: List of coefficients (must sum to 1.)

        :returns: state (OrderedDict)

        """
        if all(type(s) == list for s in states) is False:
            return None
        if len(states) != len(coefficients):
            return None
        if len(states) == 0:
            return None
        if len(states) == 1:
            return states[0]

        int_sts = list()
        for i in range(len(states[0])):
            index_states = [v[i] for v in states]
            int_sts.append(HMMInterpolation.linear_interpolate_states(index_states, coefficients))

        return int_sts

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_transitions(transitions, coefficients):
        """Linear interpolation of a set of transitions.

        :param transitions: (OrderedDict): with key='dim' and key='matrix'
        :param coefficients: List of coefficients (must sum to 1.)

        :returns: transition (OrderedDict)

        """
        if all(type(t) == collections.OrderedDict for t in transitions) is False:
            return None
        if len(transitions) != len(coefficients):
            return None
        if len(transitions) == 0:
            return []
        if len(transitions) == 1:
            return transitions[0]

        return HMMInterpolation.linear_interpolate_transitions(transitions,
                                                               coefficients)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_values(values, gammas):
        """Interpolate linearly values with gamma coefficients.

        :param values: List of values
        :param gammas: List of coefficients (must sum to 1.)

        """
        int_values = [v*g for (v, g) in zip(values, gammas)]
        return sum(int_values)

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_vectors(vectors, gammas):
        """Interpolate linearly vectors with gamma coefficients.

        :param vectors: List of vectors
        :param gammas: List of coefficients (must sum to 1.)

        """
        intvec = list()
        for i in range(len(vectors[0])):
            values = [v[i] for v in vectors]
            intvec.append(HMMInterpolation.linear_interpolate_values(values,
                                                                     gammas))
        return intvec

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_matrix(matrices, gammas):
        """Interpolate linearly matrix with gamma coefficients.

        :param matrices: List of matrix
        :param gammas: List of coefficients (must sum to 1.)

        """
        intmat = list()
        for i in range(len(matrices[0])):
            vectors = [m[i] for m in matrices]
            intmat.append(HMMInterpolation.linear_interpolate_vectors(vectors,
                                                                      gammas))
        return intmat

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_transitions(transitions, gammas):
        """Linear interpolation of a set of transitions, of an hmm.

        :param transitions: (OrderedDict): with key='dim' and key='matrix'
        :param gammas: List of coefficients (must sum to 1.)

        :returns: transition (OrderedDict)

        """
        if all(t['dim'] == transitions[0]['dim'] for t in transitions) is False:
            return None

        trans_matrix = [t['matrix'] for t in transitions]
        if len(trans_matrix) != len(gammas):
            return None

        matrix = HMMInterpolation.linear_interpolate_matrix(trans_matrix,
                                                            gammas)

        # t = collections.OrderedDict()
        t = copy.deepcopy(transitions[0])
        t['matrix'] = matrix
        return t

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_states(states, gammas):
        """Linear interpolation of a set of states, of one index only.

        :param states: (OrderedDict)
        :param gammas: List of coefficients (must sum to 1.)

        :returns: state (OrderedDict)

        """
        # interpolated state
        int_state = copy.deepcopy(states[0])

        # get states
        state = [s['state'] for s in states]
        if all(type(item) == collections.OrderedDict for item in state) is False:
            return None

        # Keys of state are: 'streams', 'streams_mixcount', 'weights', 'duration'

        # streams / weights are lists.
        streams = [s['streams'] for s in state]
        for i in range(len(streams[0])):
            values = [v[i] for v in streams]
            int_state['state']['streams'][i] = \
                HMMInterpolation.linear_interpolate_streams(values, gammas)

        weights = [w['weights'] for w in state]
        if all(type(item) == collections.OrderedDict for item in weights) is True:
            for i in range(len(weights[0])):
                values = [v[i] for v in weights]
                int_state['state']['weights'][i] = \
                    HMMInterpolation.linear_interpolate_vectors(values, gammas)

        return int_state

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_streams(streams, gammas):
        """Linear interpolation of a set of streams, of one state only.

        :param streams: (OrderedDict)
        :param gammas: List of coefficients (must sum to 1.)

        :returns: stream (OrderedDict)

        """
        # interpolated mixtures
        int_mix = copy.deepcopy(streams[0])

        mixtures = [item['mixtures'] for item in streams]
        for i in range(len(mixtures[0])):
            values = [v[i] for v in mixtures]
            int_mix['mixtures'][i] = \
                HMMInterpolation.linear_interpolate_mixtures(values, gammas)

        return int_mix

    # -----------------------------------------------------------------------

    @staticmethod
    def linear_interpolate_mixtures(mixtures, gammas):
        """Linear interpolation of a set of mixtures, of one stream only.

        :param mixtures: (OrderedDict)
        :param gammas: List of coefficients (must sum to 1.)

        :returns: mixture (OrderedDict)

        """
        pdfs = [item['pdf'] for item in mixtures]
        means = [item['mean']['vector'] for item in pdfs]
        variances = [item['covariance']['variance']['vector'] for item in pdfs]
        gconsts = [item['gconst'] for item in pdfs]

        dim = pdfs[0]['mean']['dim']
        if all(item['mean']['dim'] == dim for item in pdfs) is False:
            return None
        dim = pdfs[0]['covariance']['variance']['dim']
        if all(item['covariance']['variance']['dim'] == dim for item in pdfs) is False:
            return None

        # interpolate weights
        int_wgt = None
        w = []
        for m in mixtures:
            if m['weight'] is not None:
                w.append(m['weight'])
        if len(w) == len(mixtures[0]):
            int_wgt = HMMInterpolation.linear_interpolate_values(w, gammas)

        # interpolate means, variance and gconsts
        int_mean = HMMInterpolation.linear_interpolate_vectors(means, gammas)
        int_vari = HMMInterpolation.linear_interpolate_vectors(variances, gammas)
        int_gcst = HMMInterpolation.linear_interpolate_values(gconsts, gammas)

        # Assign to a new state
        if int_mean is None or int_vari is None or int_gcst is None:
            return None

        int_mixt = copy.deepcopy(mixtures[0])
        int_mixt['weight'] = int_wgt
        int_mixt['pdf']['mean']['vector'] = int_mean
        int_mixt['pdf']['covariance']['variance']['vector'] = int_vari
        int_mixt['pdf']['gconst'] = int_gcst

        return int_mixt
