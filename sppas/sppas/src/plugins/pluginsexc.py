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

    src.calculus.pluginsexc.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Exceptions for plugins package.

"""

from sppas.src.config import error

# -----------------------------------------------------------------------


class PluginConfigFileError(IOError):
    """:ERROR 4010:.

    Missing plugin configuration file.

    """

    def __init__(self):
        self.parameter = error(4010) + (error(4010, "plugins"))

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginSectionConfigFileError(ValueError):
    """:ERROR 4014:.

    Missing section {section_name} in the configuration file.

    """

    def __init__(self, section_name):
        self.parameter = error(4014) + \
                         (error(4014, "plugins")).format(section_name=section_name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginOptionConfigFileError(ValueError):
    """:ERROR 4016:.

    Missing option {:s} in section {:s} of the configuration file.

    """

    def __init__(self, section_name, option_name):
        self.parameter = error(4016) + \
                         (error(4016, "plugins")).format(
                             section_name=section_name,
                             option_name=option_name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginArchiveFileError(Exception):
    """:ERROR 4020:.

    Unsupported plugin file type.

    """

    def __init__(self):
        self.parameter = error(4020) + \
                         (error(4020, "plugins"))

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginArchiveIOError(IOError):
    """:ERROR 4024:.

    Unsupported plugin file type.

    """

    def __init__(self):
        self.parameter = error(4024) + \
                         (error(4024, "plugins"))

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginDuplicateError(IOError):
    """:ERROR 4030:.

     A plugin with the same name is already existing in the plugins
     folder.

    """

    def __init__(self):
        self.parameter = error(4030) + \
                         (error(4030, "plugins"))

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginIdError(ValueError):
    """:ERROR 4040:.

    No plugin with identifier {plugin_id} is available.

    """

    def __init__(self, plugin_id):
        self.parameter = error(4040) + \
                         (error(4040, "plugins")).format(
                             plugin_id=plugin_id)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginFolderError(IOError):
    """:ERROR 4050:.

    No such plugin folder: {:s}.

    """

    def __init__(self, plugin_folder):
        self.parameter = error(4050) + \
                         (error(4050, "plugins")).format(
                             plugin_folder=plugin_folder)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class PluginKeyError(KeyError):
    """:ERROR 4060:.

    A plugin with the same key is already existing or plugin already
    loaded.

    """

    def __init__(self):
        self.parameter = error(4060) + \
                         (error(4060, "plugins"))

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class CommandExecError(OSError):
    """:ERROR 4070:.

    {command_name} is not a valid command on your operating system.

    """

    def __init__(self, command_name):
        self.parameter = error(4070) + \
                         (error(4070, "plugins")).format(
                             command_name=command_name)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class CommandSystemError(OSError):
    """:ERROR 4075:.

    No command was defined for the system: {:s}.
    Supported systems of this plugin are: {:s}.

    """

    def __init__(self, current_system, supported_systems=[]):
        systems = ",".join(supported_systems)
        self.parameter = error(4075) + \
                         (error(4075, "plugins")).format(
                            current_system=current_system,
                            supported_systems=systems)

    def __str__(self):
        return repr(self.parameter)

# -----------------------------------------------------------------------


class OptionKeyError(KeyError):
    """:ERROR 4080:.

    No option with key {:s}.

    """

    def __init__(self, key):
        self.parameter = error(4080) + \
                         (error(4080, "plugins")).format(key=key)

    def __str__(self):
        return repr(self.parameter)
