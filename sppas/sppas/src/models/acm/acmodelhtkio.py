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

    src.models.acm.acmodelhtkio.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
"""
import os
import collections
import glob

from sppas.src.dependencies.grako.parsing import graken, Parser
from sppas.src.utils.makeunicode import basestring

from ..modelsexc import MioFolderError, MioFileError
from .hmm import sppasHMM
from .acmbaseio import sppasBaseIO

# ---------------------------------------------------------------------------


def _to_ordered_dict(ast):
    result = collections.OrderedDict()
    for k, v in ast.items():
        result[k] = v

    return result

# ---------------------------------------------------------------------------


class sppasHtkIO(sppasBaseIO):
    """HTK-ASCII acoustic models reader/writer.

    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :author:       Brigitte Bigi
    :contact:      develop@sppas.org

    This class is able to load and save HMM-based acoustic models from
    HTK-ASCII files.

    """
    @staticmethod
    def detect(folder):
        """Return True if the folder contains the HTK-ASCII file(s) of an ACM.

        Expected files of this reader is mainly "hmmdefs".

        """
        hmmdefs_files = glob.glob(os.path.join(folder, 'hmmdefs'))
        if len(hmmdefs_files) == 0:
            hmmdefs_files = glob.glob(os.path.join(folder, 'macros'))
            hmmdefs_files.extend(glob.glob(os.path.join(folder, 'vFloors')))
            hmmdefs_files.extend(glob.glob(os.path.join(folder, '*.hmm')))
            if len(hmmdefs_files) == 0:
                return False

        return True

    # -----------------------------------------------------------------

    def __init__(self, name=None):
        """Create a sppasHtkIO instances.

        :param name: (str) An identifier name for the Acoustic Model.
        By default, the name of the class is used.

        """
        if name is None:
            name = self.__class__.__name__
        super(sppasHtkIO, self).__init__(name)

    # -----------------------------------------------------------------------

    def read(self, folder, filename=None):
        """Load all known data from a folder or only the given file.

        The default file names are:

            - hmmdefs for an HTK-ASCII acoustic model;
            - macros for a separated macro description;
            - vFloors for a separated description allowing to construct
              the macro;
            - tiedlist for triphone models;
            - monophones.repl to map between phoneme representations.

        :param folder: (str) Folder name of the acoustic model
        :param filename: (str) Optional name of a single file to read

        """
        # Find the hmmdefs file, or the other files
        if filename is None:
            hmmdefs_files = glob.glob(os.path.join(folder, "hmmdefs"))
            if len(hmmdefs_files) == 0:
                hmmdefs_files = glob.glob(os.path.join(folder, 'macros'))
                hmmdefs_files.extend(glob.glob(os.path.join(folder, '*.hmm')))
                if len(hmmdefs_files) == 0:
                    hmmdefs_files = glob.glob(os.path.join(folder, 'vFloors'))
                    if len(hmmdefs_files) == 0:
                        raise MioFolderError(folder)
        else:
            # Find the given file
            hmmdefs_files = glob.glob(os.path.join(folder, filename))
            if len(hmmdefs_files) == 0:
                raise MioFolderError(folder)

        # Read the macros and the hmms
        try:
            self.read_macros_hmms(hmmdefs_files)
        except Exception:
            raise MioFolderError(folder)

        if filename is None:
            # Find and load the tiedlist file
            tiedlist_files = glob.glob(os.path.join(folder, 'tiedlist'))
            if len(tiedlist_files) == 1:
                self.read_tiedlist(tiedlist_files[0])

            # Find and load the monophones.repl file
            repl_files = glob.glob(os.path.join(folder, 'monophones.repl'))
            if len(repl_files) == 1:
                self.read_phonesrepl(repl_files[0])

    # -----------------------------------------------------------------------

    def write(self, folder, filename="hmmdefs"):
        """Save the model into a file, in HTK-ASCII standard format.

        The default file names are:
            - hmmdefs (macros + hmms);
            - tiedlist (if triphones);
            - monophones.repl.

        :param folder: (str) Folder name of the acoustic model
        :param filename: (str) Optional name of the file to write macros and hmms

        """
        if os.path.isdir(folder) is False:
            os.mkdir(folder)

        # Write macros and hmms in the hmmdefs file
        filename = os.path.join(folder, filename)
        with open(filename, 'w') as f:
            if self._macros is not None:
                if len(self._hmms) > 0:
                    f.write(sppasHtkIO._serialize_macros(self._macros,
                                                         variance=False,
                                                         mean=False))
                else:
                    f.write(sppasHtkIO._serialize_macros(self._macros))

            if len(self._hmms) > 0:
                f.write(sppasHtkIO._serialize_hmms(self._hmms))

        # write tiedlist
        if self._tiedlist.is_empty() is False:
            self._tiedlist.save(os.path.join(folder, 'tiedlist'))

        # write monophones.repl
        if self._repllist.is_empty() is False:
            self._repllist.save_as_ascii(os.path.join(folder, 'monophones.repl'))

    # -----------------------------------------------------------------------

    @staticmethod
    def read_hmm(filename):
        """Return the (first) HMM described into the given filename.

        :param filename: (str) File to read.
        :returns: (sppasHMM)

        """
        folder_name, file_name = os.path.split(filename)
        parser = sppasHtkIO()
        parser.read(folder_name, file_name)
        if len(parser.get_hmms()) < 1:
            raise MioFolderError(filename)

        return parser.get_hmms()[0]

    # -----------------------------------------------------------------------

    @staticmethod
    def write_hmm(hmm, filename):
        """Save a single hmm into the given filename.

        :param hmm: (sppasHMM) The HMM model to write
        :param filename: (str) Name of the file to write.

        """
        result = sppasHtkIO._serialize_hmms([hmm])
        with open(filename, 'w') as f:
            f.write(result)

    # -----------------------------------------------------------------------

    @staticmethod
    def write_hmm_proto(proto_size, proto_filename):
        """Write a `proto` file. The proto is based on a 5-states HMM.

        :param proto_size: (int) Number of mean and variance values. It's
        commonly either 25 or 39, it depends on the MFCC parameters.
        :param proto_filename: (str) Full name of the prototype to write.

        """
        with open(proto_filename, "w") as fp:
            means = "0.0 " * proto_size
            variances = "1.0 " * proto_size
            means = means.strip()
            variances = variances.strip()

            fp.write("~h \"proto\"\n")
            fp.write("<BeginHMM>\n")
            fp.write("<NumStates> 5\n")
            for i in range(2, 5):
                fp.write("<State> {}\n".format(i))
                fp.write("<NumMixes> 1\n")
                fp.write("<Mixture> 1 1.0\n")
                fp.write("<Mean> {:d}\n".format(proto_size))
                fp.write("{:s}\n".format(means))
                fp.write("<Variance> {:d}\n".format(proto_size))
                fp.write("{:s}\n".format(variances))
            fp.write("<Transp> 5\n")
            fp.write(" 0.0 1.0 0.0 0.0 0.0\n")
            fp.write(" 0.0 0.6 0.4 0.0 0.0\n")
            fp.write(" 0.0 0.0 0.6 0.4 0.0\n")
            fp.write(" 0.0 0.0 0.0 0.7 0.3\n")
            fp.write(" 0.0 0.0 0.0 0.0 0.0\n")
            fp.write("<EndHMM>\n")

    # -----------------------------------------------------------------------

    def read_macros_hmms(self, filenames):
        """Load an HTK-ASCII model from one or more files.

        :param filenames: Name of the files of the model
        (e.g. macros and/or hmms files and/or hmmdefs)

        """
        text = ''
        for fnm in filenames:
            with open(fnm, 'r') as fp:
                for line in fp.readlines():
                    line = line.strip()
                    if len(line) > 0:
                        text += line + "\n"

        if len(text) == 0:
            raise MioFileError(" ".join(filenames))

        parser = HtkModelParser()
        htk_model = HtkModelSemantics()  # OrderedDict()
        model = parser.parse(text,
                             rule_name='model',
                             ignorecase=True,
                             semantics=htk_model,
                             comments_re="\(\*.*?\*\)",
                             trace=False)

        self._macros = model['macros']
        self._hmms = list()
        for h in model['hmms']:
            new_hmm = sppasHMM()
            new_hmm.set_name(h['name'])
            new_hmm.set_definition(h['definition'])
            self._hmms.append(new_hmm)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    @staticmethod
    def _serialize_macros(macros, options=True, transition=True,
                          variance=True, mean=True, state=True,
                          duration=True):
        """Serialize macros into a string, in HTK-ASCII standard format.

        :param macros: (OrderedDict) Macros to save
        :returns: The HTK-ASCII macros as a string.

        """
        result = ''

        # First serialize the macros
        for macro in macros:

            if macro.get('options', None) and options is True:
                result += '~o '
                for option in macro['options']['definition']:
                    result += sppasHtkIO._serialize_option(option)

            elif macro.get('transition', None) and transition is True:
                result += '~t "{}"\n'.format(macro['transition']['name'])
                result += sppasHtkIO._serialize_transp(macro['transition']['definition'])

            elif macro.get('variance', None) and variance is True:
                result += '~v "{}"\n'.format(macro['variance']['name'])
                result += sppasHtkIO._serialize_variance(macro['variance']['definition'])

            elif macro.get('state', None) and state is True:
                result += '~s "{}"\n'.format(macro['state']['name'])
                result += sppasHtkIO._serialize_stateinfo(macro['state']['definition'])

            elif macro.get('mean', None) and mean is True:
                result += '~u "{}"\n'.format(macro['mean']['name'])
                result += sppasHtkIO._serialize_mean(macro['mean']['definition'])

            elif macro.get('duration', None) and duration is True:
                result += '~d "{}"\n'.format(macro['duration']['name'])
                result += sppasHtkIO._serialize_duration(macro['duration']['definition'])

            #else:
            #    raise NotImplementedError('Cannot serialize {}'.format(macro))

        return result

    # -----------------------------------

    @staticmethod
    def _serialize_hmms(hmms):
        """Serialize hmms into a string, in HTK-ASCII standard format.

        :returns: The HTK-ASCII model as a string.

        """
        result = ''
        for hmm_model in hmms:
            if hmm_model.name is not None:
                result += sppasHtkIO._serialize_name(hmm_model.name)
            result += sppasHtkIO._serialize_definition(hmm_model.definition)

        return result

    # ----------------------------------

    @staticmethod
    def _serialize_name(name):
        return '~h "{}"\n'.format(name)

    # ----------------------------------

    @staticmethod
    def _serialize_definition(definition):
        result = ''

        result += '<BeginHMM>\n'
        if definition.get('options', None):
            for option in definition['options']:
                result += sppasHtkIO._serialize_option(option)

        result += '<NumStates> {}\n'.format(definition['state_count'])

        for state in definition['states']:
            result += sppasHtkIO._serialize_state(state)

        if definition.get('regression_tree', None) is not None:
            raise NotImplementedError('Cannot serialize {}'.format(definition['regression_tree']))

        result += sppasHtkIO._serialize_transp(definition['transition'])

        if definition.get('duration', None) is not None:
            result += sppasHtkIO._serialize_duration(definition['duration'])

        result += '<EndHMM>\n'

        return result

    # ----------------------------------

    @staticmethod
    def _serialize_option(option):
        result = ''
        if option.get('hmm_set_id', None) is not None:
            result += '<HmmSetId> {}'.format(option['hmm_set_id'])

        if option.get('stream_info', None) is not None:
            result += '<StreamInfo> {}'.format(option['stream_info']['count'])

            if option['stream_info'].get('sizes', None) is not None:
                result += ' {}'.format(' '.join(['{:d}'.format(v) for v in option['stream_info']['sizes']]))

        if option.get('vector_size', None) is not None:
            result += '<VecSize> {:d}'.format(option['vector_size'])

        if option.get('input_transform', None) is not None:
            raise NotImplementedError('Serialization of {} '
                                      'is not implemented.'.format(option['input_transform']))

        if option.get('covariance_kind', None) is not None:
            result += '<{}>'.format(option['covariance_kind'])

        if option.get('duration_kind', None) is not None:
            result += '<{}>'.format(option['duration_kind'])

        if option.get('parameter_kind', None) is not None:
            result += '<{}{}>'.format(option['parameter_kind']['base'],
                                      ''.join(option['parameter_kind']['options']))

        result += '\n'
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_transp(definition):
        if isinstance(definition, basestring):
            return '~t "{}"\n'.format(definition)

        result = ''
        result += '<TransP> {}\n'.format(definition['dim'])
        result += '{}'.format(sppasHtkIO._matrix_to_htk(definition['matrix']))
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_variance(definition):
        if isinstance(definition, basestring):
            return '~v {}\n'.format(definition)

        result = ''
        result += '<Variance> {}\n'.format(definition['dim'])
        result += '{}'.format(sppasHtkIO._array_to_htk(definition['vector']))
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_mean(definition):
        if isinstance(definition, basestring):
            return '~u "{}"\n'.format(definition)

        result = ''
        result += '<Mean> {}\n'.format(definition['dim'])
        result += '{}'.format(sppasHtkIO._array_to_htk(definition['vector']))
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_duration(definition):
        if isinstance(definition, basestring):
            return '~d "{}"\n'.format(definition)

        result = ''
        result += '<Duration> {}\n'.format(definition['dim'])
        result += '{}'.format(sppasHtkIO._array_to_htk(definition['vector']))
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_weights(definition):
        if isinstance(definition, basestring):
            return '~w "{}"\n'.format(definition)

        result = ''
        result += '<SWeights> {}\n'.format(definition['dim'])
        result += '{}'.format(sppasHtkIO._array_to_htk(definition['vector']))
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_covariance(definition):
        result = ''
        if definition['variance'] is not None:
            result += sppasHtkIO._serialize_variance(definition['variance'])

        else:
            raise NotImplementedError('Cannot serialize {}'.format(definition))

        return result

    # ----------------------------------

    @staticmethod
    def _serialize_mixpdf(definition):
        if isinstance(definition, basestring):
            return '~m "{}"\n'.format(definition)

        result = ''
        if definition.get('regression_class', None) is not None:
            result += '<RClass> {}\n'.format(definition['regression_class'])

        result += sppasHtkIO._serialize_mean(definition['mean'])
        result += sppasHtkIO._serialize_covariance(definition['covariance'])

        if definition.get('gconst', None) is not None:
            result += '<GConst> {:.6e}\n'.format(definition['gconst'])

        return result

    # ----------------------------------

    @staticmethod
    def _serialize_mixture(definition):
        result = ''

        if definition.get('index', None) is not None:
            result += '<Mixture> {} {:.6e}\n'.format(definition['index'], definition['weight'])

        result += sppasHtkIO._serialize_mixpdf(definition['pdf'])
        return result

    # ----------------------------------

    @staticmethod
    def _serialize_stream(definition):
        result = ''

        if definition.get('dim', None) is not None:
            result += '<Stream> {}\n'.format(definition['dim'])

        if definition.get('mixtures', None) is not None:
            for mixture in definition['mixtures']:
                result += sppasHtkIO._serialize_mixture(mixture)

        else:
            raise NotImplementedError('Cannot serialize {}'.format(definition))

        return result

    # ----------------------------------

    @staticmethod
    def _serialize_stateinfo(definition):
        if isinstance(definition, basestring):
            return '~s "{}"\n'.format(definition)

        result = ''
        if definition.get('streams_mixcount', None):
            result += '<NumMixes> {}\n'.format(' '.join(['{}'.format(v) for v in definition['streams_mixcount']]))

        if definition.get('weights', None) is not None:
            result += sppasHtkIO._serialize_weights(definition['weights'])

        for stream in definition['streams']:
            result += sppasHtkIO._serialize_stream(stream)

        if definition.get('duration', None) is not None:
            result += sppasHtkIO._serialize_duration(definition['duration'])

        return result

    # ----------------------------------

    @staticmethod
    def _serialize_state(definition):
        result = ''

        result += '<State> {}\n'.format(definition['index'])
        result += sppasHtkIO._serialize_stateinfo(definition['state'])

        return result

    # ----------------------------------

    @staticmethod
    def _array_to_htk(arr):
        return ' {}\n'.format(' '.join(['{:2.6e}'.format(value) for value in arr]))

    # ----------------------------------

    @staticmethod
    def _matrix_to_htk(mat):
        result = ''
        for arr in mat:
            result = result + sppasHtkIO._array_to_htk(arr)
        return result

# ---------------------------------------------------------------------------
# Semantic of an HTK acoustic model. Used to parse files.
# ---------------------------------------------------------------------------


class HtkModelSemantics(object):
    """Part of the Inspire package: https://github.com/rikrd/inspire.

    :author: Ricard Marxer.
    :license: GPL, v2

    """
    def __init__(self):
        pass

    def matrix(self, ast):
        #  return [float(v) for v in ast.split(' ')]
        return [float(v) for v in ast.split()]

    def vector(self, ast):
        return [float(v) for v in ast.split(' ')]

    def short(self, ast):
        return int(ast)

    def float(self, ast):
        return float(ast)

    def transPdef(self, ast):
        d = _to_ordered_dict(ast)
        d['matrix'] = []
        aarray = []
        d['array'].append(None)  # for the last serie to be appended!
        for a in d['array']:
            if len(aarray) == ast['dim']:
                d['matrix'].append(aarray)
                aarray = [a]
            else:
                aarray.append(a)
        #  numpy solution:
        #  d['matrix'] = d['array'].reshape((ast['dim'], ast['dim']))
        d.pop('array')
        return d

    def _default(self, ast):
        if isinstance(ast, collections.Mapping):
            return _to_ordered_dict(ast)

        return ast

    def _unquote(self, txt):
        if txt.startswith('"') and txt.endswith('"'):
            return txt[1:-1]

        return txt

    def string(self, ast):
        return self._unquote(ast)

    def __repr__(self):
        return ''

# ---------------------------------------------------------------------------
# HTK-ASCII Acoustic Model: Set of rules for the parser
# ---------------------------------------------------------------------------


class HtkModelParser(Parser):

    def __init__(self, whitespace=None, nameguard=True, **kwargs):
        super(HtkModelParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            **kwargs
        )

    @graken()
    def _model_(self):
        def block0():
            self._macrodef_()
            self.ast.setlist('macros', self.last_node)
        self._closure(block0)

        def block2():
            self._hmmmacro_()
            self.ast.setlist('hmms', self.last_node)
        self._closure(block2)

        self.ast._define(
            [],
            ['macros', 'hmms']
        )

    @graken()
    def _macrodef_(self):
        with self._choice():
            with self._option():
                self._transPmacro_()
                self.ast['transition'] = self.last_node
            with self._option():
                self._stateinfomacro_()
                self.ast['state'] = self.last_node
            with self._option():
                self._optmacro_()
                self.ast['options'] = self.last_node
            with self._option():
                self._varmacro_()
                self.ast['variance'] = self.last_node
            with self._option():
                self._meanmacro_()
                self.ast['mean'] = self.last_node
            with self._option():
                self._durationmacro_()
                self.ast['duration'] = self.last_node
            self._error('no available options')

        self.ast._define(
            ['transition', 'state', 'options', 'variance', 'mean', 'duration'],
            []
        )

    @graken()
    def _hmmmacro_(self):
        with self._optional():
            self._hmmref_()
            self.ast['name'] = self.last_node
        self._hmmdef_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['name', 'definition'],
            []
        )

    @graken()
    def _optmacro_(self):
        self._token('~o')
        self._cut()
        self._globalOpts_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['definition'],
            []
        )

    @graken()
    def _transPmacro_(self):
        self._transPref_()
        self.ast['name'] = self.last_node
        self._transPdef_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['name', 'definition'],
            []
        )

    @graken()
    def _stateinfomacro_(self):
        self._stateinforef_()
        self.ast['name'] = self.last_node
        self._stateinfodef_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['name', 'definition'],
            []
        )

    @graken()
    def _varmacro_(self):
        self._varref_()
        self.ast['name'] = self.last_node
        self._vardef_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['name', 'definition'],
            []
        )

    @graken()
    def _meanmacro_(self):
        self._meanref_()
        self.ast['name'] = self.last_node
        self._meandef_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['name', 'definition'],
            []
        )

    @graken()
    def _durationmacro_(self):
        self._durationref_()
        self.ast['name'] = self.last_node
        self._durationdef_()
        self.ast['definition'] = self.last_node

        self.ast._define(
            ['name', 'definition'],
            []
        )

    @graken()
    def _varref_(self):
        self._token('~v')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _transPref_(self):
        self._token('~t')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _stateinforef_(self):
        self._token('~s')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _hmmref_(self):
        self._token('~h')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _weightsref_(self):
        self._token('~w')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _mixpdfref_(self):
        self._token('~m')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _meanref_(self):
        self._token('~u')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _durationref_(self):
        self._token('~d')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _invref_(self):
        self._token('~i')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _xformref_(self):
        self._token('~x')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _inputXformref_(self):
        self._token('~j')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node

    @graken()
    def _macro_(self):
        self._string_()

    @graken()
    def _hmmdef_(self):
        self._token('<BeginHMM>')
        self._cut()
        with self._optional():
            self._globalOpts_()
            self.ast['options'] = self.last_node
        self._token('<NumStates>')
        self._cut()
        self._short_()
        self.ast['state_count'] = self.last_node

        def block2():
            self._state_()
            self.ast.setlist('states', self.last_node)
        self._positive_closure(block2)

        with self._optional():
            self._regTree_()
            self.ast['regression_tree'] = self.last_node
        self._transP_()
        self.ast['transition'] = self.last_node
        with self._optional():
            self._duration_()
            self.ast['duration'] = self.last_node
        self._token('<EndHMM>')

        self.ast._define(
            ['options', 'state_count', 'regression_tree', 'transition', 'duration'],
            ['states']
        )

    @graken()
    def _globalOpts_(self):

        def block1():
            self._option_()
        self._positive_closure(block1)

        self.ast['@'] = self.last_node

    @graken()
    def _option_(self):
        with self._choice():
            with self._option():
                self._token('<HmmSetId>')
                self._cut()
                self._string_()
                self.ast['hmm_set_id'] = self.last_node
            with self._option():
                self._token('<StreamInfo>')
                self._cut()
                self._streaminfo_()
                self.ast['stream_info'] = self.last_node
            with self._option():
                self._token('<VecSize>')
                self._cut()
                self._short_()
                self.ast['vector_size'] = self.last_node
            with self._option():
                self._token('<InputXform>')
                self._cut()
                self._inputXform_()
                self.ast['input_transform'] = self.last_node
            with self._option():
                self._covkind_()
                self.ast['covariance_kind'] = self.last_node
            with self._option():
                self._durkind_()
                self.ast['duration_kind'] = self.last_node
            with self._option():
                self._parmkind_()
                self.ast['parameter_kind'] = self.last_node
            self._error('no available options')

        self.ast._define(
            ['hmm_set_id', 'stream_info', 'vector_size', 'input_transform',
             'covariance_kind', 'duration_kind', 'parameter_kind'],
            []
        )

    @graken()
    def _streaminfo_(self):
        self._short_()
        self.ast['count'] = self.last_node

        def block2():
            self._short_()
        self._closure(block2)
        self.ast['sizes'] = self.last_node

        self.ast._define(
            ['count', 'sizes'],
            []
        )

    @graken()
    def _covkind_(self):
        self._token('<')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('diagc')
                with self._option():
                    self._token('invdiagc')
                with self._option():
                    self._token('fullc')
                with self._option():
                    self._token('lltc')
                with self._option():
                    self._token('xformc')
                self._error('expecting one of: diagc fullc invdiagc lltc xformc')
        self.ast['@'] = self.last_node
        self._token('>')

    @graken()
    def _durkind_(self):
        self._token('<')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('nulld')
                with self._option():
                    self._token('poissond')
                with self._option():
                    self._token('gammad')
                with self._option():
                    self._token('gen')
                self._error('expecting one of: gammad gen nulld poissond')
        self.ast['@'] = self.last_node
        self._token('>')

    @graken()
    def _parmkind_(self):
        self._token('<')
        self._basekind_()
        self.ast['base'] = self.last_node

        def block2():
            with self._choice():
                with self._option():
                    self._token('_D')
                with self._option():
                    self._token('_A')
                with self._option():
                    self._token('_T')
                with self._option():
                    self._token('_E')
                with self._option():
                    self._token('_N')
                with self._option():
                    self._token('_Z')
                with self._option():
                    self._token('_O')
                with self._option():
                    self._token('_0')
                with self._option():
                    self._token('_V')
                with self._option():
                    self._token('_C')
                with self._option():
                    self._token('_K')
                self._error('expecting one of: _A _C _D _E _K _N _O _0 _T _V _Z')
        self._closure(block2)
        self.ast['options'] = self.last_node
        self._token('>')

        self.ast._define(
            ['base', 'options'],
            []
        )

    @graken()
    def _basekind_(self):
        with self._choice():
            with self._option():
                self._token('discrete')
            with self._option():
                self._token('lpc')
            with self._option():
                self._token('lpcepstra')
            with self._option():
                self._token('mfcc')
            with self._option():
                self._token('fbank')
            with self._option():
                self._token('melspec')
            with self._option():
                self._token('lprefc')
            with self._option():
                self._token('lpdelcep')
            with self._option():
                self._token('user')
            self._error('expecting one of: discrete fbank lpc lpcepstra lpdelcep lprefc melspec mfcc user')

    @graken()
    def _state_(self):
        self._token('<State>')
        self._cut()
        self._short_()
        self.ast['index'] = self.last_node
        self._stateinfo_()
        self.ast['state'] = self.last_node

        self.ast._define(
            ['index', 'state'],
            []
        )

    @graken()
    def _stateinfo_(self):
        with self._choice():
            with self._option():
                self._stateinforef_()
                self.ast['@'] = self.last_node
            with self._option():
                self._stateinfodef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _stateinfodef_(self):
        with self._optional():
            self._mixes_()
            self.ast['streams_mixcount'] = self.last_node
        with self._optional():
            self._weights_()
            self.ast['weights'] = self.last_node

        def block2():
            self._stream_()
            self.ast.setlist('streams', self.last_node)
        self._positive_closure(block2)

        with self._optional():
            self._duration_()
            self.ast['duration'] = self.last_node

        self.ast._define(
            ['streams_mixcount', 'weights', 'duration'],
            ['streams']
        )

    @graken()
    def _mixes_(self):
        self._token('<NumMixes>')
        self._cut()

        def block1():
            self._short_()
        self._positive_closure(block1)

        self.ast['@'] = self.last_node

    @graken()
    def _weights_(self):
        with self._choice():
            with self._option():
                self._weightsref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._weightsdef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _weightsdef_(self):
        self._token('<SWeights>')
        self._cut()
        self._short_()
        self.ast['dim'] = self.last_node
        self._vector_()
        self.ast['vector'] = self.last_node

        self.ast._define(
            ['dim', 'vector'],
            []
        )

    @graken()
    def _stream_(self):
        with self._optional():
            self._token('<Stream>')
            self._cut()
            self._short_()
            self.ast['dim'] = self.last_node
        with self._group():
            with self._choice():
                with self._option():

                    def block1():
                        self._mixture_()
                        self.ast.setlist('mixtures', self.last_node)
                    self._positive_closure(block1)
                with self._option():
                    self._tmixpdf_()
                    self.ast['tmixpdf'] = self.last_node
                with self._option():
                    self._discpdf_()
                    self.ast['discpdf'] = self.last_node
                self._error('no available options')

        self.ast._define(
            ['dim', 'tmixpdf', 'discpdf'],
            ['mixtures']
        )

    @graken()
    def _mixture_(self):
        with self._optional():
            self._token('<Mixture>')
            self._cut()
            self._short_()
            self.ast['index'] = self.last_node
            self._float_()
            self.ast['weight'] = self.last_node
        self._mixpdf_()
        self.ast['pdf'] = self.last_node

        self.ast._define(
            ['index', 'weight', 'pdf'],
            []
        )

    @graken()
    def _tmixpdf_(self):
        self._token('<TMix>')
        self._cut()
        self._macro_()
        self._weightList_()

    @graken()
    def _weightList_(self):

        def block0():
            self._repShort_()
        self._positive_closure(block0)

    @graken()
    def _repShort_(self):
        self._short_()
        with self._optional():
            self._token('*')
            self._cut()
            self._char_()

    @graken()
    def _discpdf_(self):
        self._token('<DProb>')
        self._cut()
        self._weightList_()

    @graken()
    def _mixpdf_(self):
        with self._choice():
            with self._option():
                self._mixpdfref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._mixpdfdef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _mixpdfdef_(self):
        with self._optional():
            self._rclass_()
            self.ast['regression_class'] = self.last_node
        self._mean_()
        self.ast['mean'] = self.last_node
        self._cov_()
        self.ast['covariance'] = self.last_node
        with self._optional():
            self._token('<GConst>')
            self._cut()
            self._float_()
            self.ast['gconst'] = self.last_node

        self.ast._define(
            ['regression_class', 'mean', 'covariance', 'gconst'],
            []
        )

    @graken()
    def _rclass_(self):
        self._token('<RClass>')
        self._cut()
        self._short_()
        self.ast['@'] = self.last_node

    @graken()
    def _mean_(self):
        with self._choice():
            with self._option():
                self._meanref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._meandef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _meandef_(self):
        self._token('<Mean>')
        self._cut()
        self._short_()
        self.ast['dim'] = self.last_node
        self._vector_()
        self.ast['vector'] = self.last_node

        self.ast._define(
            ['dim', 'vector'],
            []
        )

    @graken()
    def _cov_(self):
        with self._choice():
            with self._option():
                self._var_()
                self.ast['variance'] = self.last_node
            with self._option():
                self._inv_()
            with self._option():
                self._xform_()
            self._error('no available options')

        self.ast._define(
            ['variance'],
            []
        )

    @graken()
    def _var_(self):
        with self._choice():
            with self._option():
                self._varref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._vardef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _vardef_(self):
        self._token('<Variance>')
        self._cut()
        self._short_()
        self.ast['dim'] = self.last_node
        self._vector_()
        self.ast['vector'] = self.last_node

        self.ast._define(
            ['dim', 'vector'],
            []
        )

    @graken()
    def _inv_(self):
        with self._choice():
            with self._option():
                self._invref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._invdef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _invdef_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('<InvCovar>')
                with self._option():
                    self._token('<LLTCovar>')
                self._error('expecting one of: <InvCovar> <LLTCovar>')
        self.ast['type'] = self.last_node
        self._cut()
        self._short_()
        self.ast['dim'] = self.last_node
        self._tmatrix_()
        self.ast['matrix'] = self.last_node

        self.ast._define(
            ['type', 'dim', 'matrix'],
            []
        )

    @graken()
    def _xform_(self):
        with self._choice():
            with self._option():
                self._xformref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._xformdef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _xformdef_(self):
        self._token('<Xform>')
        self._cut()
        self._short_()
        self.ast['dim1'] = self.last_node
        self._short_()
        self.ast['dim2'] = self.last_node
        self._matrix_()
        self.ast['matrix'] = self.last_node

        self.ast._define(
            ['dim1', 'dim2', 'matrix'],
            []
        )

    @graken()
    def _tmatrix_(self):
        self._matrix_()

    @graken()
    def _duration_(self):
        with self._choice():
            with self._option():
                self._durationref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._durationdef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _durationdef_(self):
        self._token('<Duration>')
        self._cut()
        self._short_()
        self.ast['dim'] = self.last_node
        self._vector_()
        self.ast['vector'] = self.last_node

        self.ast._define(
            ['dim', 'vector'],
            []
        )

    @graken()
    def _regTree_(self):
        self._token('~r')
        self._cut()
        self._macro_()
        self.ast['@'] = self.last_node
        self._tree_()
        self.ast['tree'] = self.last_node

        self.ast._define(
            ['tree'],
            []
        )

    @graken()
    def _tree_(self):
        self._token('<RegTree>')
        self._cut()
        self._short_()
        self._nodes_()

    @graken()
    def _nodes_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('<Node>')
                    self._cut()
                    self._short_()
                    self._short_()
                    self._short_()
                with self._option():
                    self._token('<TNode>')
                    self._cut()
                    self._short_()
                    self._int_()
                self._error('no available options')
        with self._optional():
            self._nodes_()

    @graken()
    def _transP_(self):
        with self._choice():
            with self._option():
                self._transPref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._transPdef_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _transPdef_(self):
        self._token('<TransP>')
        self._cut()
        self._short_()
        self.ast['dim'] = self.last_node
        self._matrix_()
        self.ast['array'] = self.last_node

        self.ast._define(
            ['dim', 'array'],
            []
        )

    @graken()
    def _inputXform_(self):
        with self._choice():
            with self._option():
                self._inputXformref_()
                self.ast['@'] = self.last_node
            with self._option():
                self._inhead_()
                self._inmatrix_()
            self._error('no available options')

    @graken()
    def _inhead_(self):
        self._token('<MMFIdMask>')
        self._cut()
        self._string_()
        self._parmkind_()
        with self._optional():
            self._token('<PreQual>')

    @graken()
    def _inmatrix_(self):
        self._token('<LinXform>')
        self._token('<VecSize>')
        self._cut()
        self._short_()
        self._token('<BlockInfo>')
        self._cut()
        self._short_()

        def block0():
            self._short_()
        self._positive_closure(block0)

        def block1():
            self._block_()
        self._positive_closure(block1)

    @graken()
    def _block_(self):
        self._token('<Block>')
        self._cut()
        self._short_()
        self._xform_()

    @graken()
    def _string_(self):
        self._pattern(r'.*')

    @graken()
    def _vector_(self):
        self._pattern(r'[\d.\-\+eE \n]+')

    @graken()
    def _matrix_(self):
        self._pattern(r'[\d.\-\+eE \n]+')

    @graken()
    def _short_(self):
        self._pattern(r'\d+')

    @graken()
    def _float_(self):
        self._pattern(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')

    @graken()
    def _char_(self):
        self._pattern(r'.')

    @graken()
    def _int_(self):
        self._pattern(r'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)')
