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

    src.models.modelsexc.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Exceptions for models package.

"""
from sppas.src.config import error

# -----------------------------------------------------------------------


class ModelsDataTypeError(TypeError):
    """:ERROR 7010:.

    Expected a {data_name} of type {expected_type}. Got {data_type} instead.

    """

    def __init__(self, data_name, expected_type, data_type):
        self.parameter = error(7010) + \
                         (error(7010, "models")).format(
                             data_name=data_name,
                             expected_type=expected_type,
                             data_type=data_type)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class MioEncodingError(UnicodeDecodeError):
    """:ERROR 7500:.

    The file {!s:s} contains non UTF-8 characters: {:s}.

    """

    def __init__(self, filename, error_name):
        self.parameter = error(7500) + \
                         (error(7500, "models")).format(filename, error_name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class MioFileFormatError(IOError):
    """:ERROR 7505:.

    Fail formats: unrecognized file format {!s:s}.

    """

    def __init__(self, name):
        self.parameter = error(7505) + \
                         (error(7505, "models")).format(name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class MioFileError(IOError):
    """:ERROR 7515:.

    No model found or empty model in {!s:s}.

    """

    def __init__(self, name):
        self.parameter = error(7515) + \
                         (error(7515, "models")).format(name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class MioFolderError(IOError):
    """:ERROR 7510:.

    Fail formats: the folder {!s:s} does not contain a known model.

    """

    def __init__(self, folder):
        self.parameter = error(7510) + \
                         (error(7510, "models")).format(folder)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class NgramOrderValueError(ValueError):
    """:ERROR 7110:.

    Expected an ngram order value between {min_value} and {max_value}.
    Got {got_value} instead.

    """

    def __init__(self, min_value, max_value, got_value):
        self.parameter = error(7110) + \
                         (error(7110, "models")).format(min_value=min_value,
                                                        max_value=max_value,
                                                        got_value=got_value)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class NgramCountValueError(ValueError):
    """:ERROR 7120:.

    Expected a minimum count value of {min_value}. Got {got_value} instead.

    """

    def __init__(self, min_value, got_value):
        self.parameter = error(7120) + \
                         (error(7120, "models")).format(min_value=min_value,
                                                        got_value=got_value)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class NgramMethodNameError(NameError):
    """:ERROR 7130:.

    Expected a known name of the method. Got {got_name} instead.

    """

    def __init__(self, got_name):
        self.parameter = error(7130) + \
                         (error(7130, "models")).format(got_name=got_name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class ArpaFileError(IOError):
    """:ERROR 7210:.

    Expected a standard arpa file. Error with line: {line}.

    """

    def __init__(self, line):
        self.parameter = error(7210) + \
                         (error(7210, "models")).format(line=line)

    def __str__(self):
        return repr(self.parameter)
