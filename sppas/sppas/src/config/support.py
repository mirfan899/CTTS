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

    config.support.py
    ~~~~~~~~~~~~~~~~~

"""

import os
import logging
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from .sglobal import sppasPathSettings, sppasGlobalSettings


class PostInstall:

    @staticmethod
    def sppas_directories():
        """Create the required directories in the SPPAS package."""
        logging.debug('Check for directories')
        with sppasPathSettings() as paths:

            if os.path.exists(paths.logs) is False:
                os.mkdir(paths.logs)
                logging.info(
                    "The directory {:s} to store logs is created."
                    "".format(paths.logs))

            # if os.path.exists(paths.wkps) is False:
            #     os.mkdir(paths.wkps)
            #     logging.info(
            #         "The directory {:s} to store workspaces is created."
            #         "".format(paths.wkps))

            if os.path.exists(paths.trash) is False:
                os.mkdir(paths.trash)
                logging.info(
                    "The Trash directory {:s} is created."
                    "".format(paths.trash))


class Update:

    @staticmethod
    def check_update():
        with sppasGlobalSettings as sg:
            current = sg.__version__

            url = sg.__url__ + '/download.html'
            response = urlopen(url)
            data = str(response.read())
            print(data)

