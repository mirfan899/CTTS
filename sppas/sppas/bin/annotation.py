#!/usr/bin/env python
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

    bin.annotation.py
    ~~~~~~~~~~~~~~~~

    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      contact@sppas.org
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2018  Brigitte Bigi
    :summary:      Run any or all automatic annotations.

"""
import sys
import os
from argparse import ArgumentParser

PROGRAM = os.path.abspath(__file__)
SPPAS = os.path.dirname(os.path.dirname(os.path.dirname(PROGRAM)))
sys.path.append(SPPAS)

from sppas import sg
from sppas import sppasParam
from sppas import sppasAnnotationsManager
from sppas import sppasLogSetup

from sppas.src.anndata.aio import extensions_out
from sppas.src.ui.term.textprogress import ProcessProgressTerminal
from sppas.src.ui.term.terminalcontroller import TerminalController


# ----------------------------------------------------------------------------
# Verify and extract args:
# ----------------------------------------------------------------------------

parameters = sppasParam()
parser = ArgumentParser(usage="{:s} -w file|folder [options]"
                              "".format(os.path.basename(PROGRAM)),
                        prog=PROGRAM,
                        description="Automatic annotations.")

parser.add_argument("-w",
                    required=True,
                    metavar="file|folder",
                    help='Input wav file name, or directory')

parser.add_argument("-l",
                    metavar="lang",
                    help='Input language, using iso639-3 code')

parser.add_argument("-e",
                    default=".xra",
                    metavar="extension",
                    help='Output extension. One of: {:s}'
                         ''.format(" ".join(extensions_out)))

# todo: we should read sppasui.json instead...
parser.add_argument("--momel", action='store_true',
                    help="Activate Momel")
parser.add_argument("--intsint", action='store_true',
                    help="Activate INTSINT")
parser.add_argument("--ipus", action='store_true',
                    help="Activate Search for IPUs")
parser.add_argument("--tok", action='store_true',
                    help="Activate Tokenization")
parser.add_argument("--phon", action='store_true',
                    help="Activate Phonetization")
parser.add_argument("--align", action='store_true',
                    help="Activate Phones alignment")
parser.add_argument("--syll", action='store_true',
                    help="Activate Syllabification")
parser.add_argument("--tga", action='store_true',
                    help="Activate TimeGroupAnalyzer")
parser.add_argument("--repet", action='store_true',
                    help="Activate Self-Repetitions")
parser.add_argument("--all", action='store_true',
                    help="Activate ALL automatic annotations")

parser.add_argument("--merge",
                    action='store_true',
                    help="Create a merged file with all annotations")

if len(sys.argv) <= 1:
    sys.argv.append('-h')

args = parser.parse_args()

# ----------------------------------------------------------------------------
# Automatic Annotations are here:
# ----------------------------------------------------------------------------

sep = "-"*72

parameters.add_to_workspace(os.path.abspath(args.w))

if args.l:
    parameters.set_lang(args.l)
parameters.set_output_format(args.e)

if args.momel:
    parameters.activate_annotation("momel")
if args.intsint:
    parameters.activate_annotation("intsint")
if args.ipus:
    parameters.activate_annotation("searchipus")
if args.tok:
    parameters.activate_annotation("textnorm")
if args.phon:
    parameters.activate_annotation("phonetize")
if args.align:
    parameters.activate_annotation("alignment")
if args.syll:
    parameters.activate_annotation("syllabify")
if args.tga:
    parameters.activate_annotation("tga")
if args.repet:
    parameters.activate_annotation("selfrepet")
if args.all:
    for step in range(parameters.get_step_numbers()):
        parameters.activate_step(step)

try:
    term = TerminalController()
    print(term.render('${GREEN}{:s}${NORMAL}').format(sep))
    print(term.render('${RED} {} - Version {}${NORMAL}'
                      '').format(sg.__name__, sg.__version__))
    print(term.render('${BLUE} {} ${NORMAL}').format(sg.__copyright__))
    print(term.render('${BLUE} {} ${NORMAL}').format(sg.__url__))
    print(term.render('${GREEN}{:s}${NORMAL}\n').format(sep))

    # Redirect all messages to a quiet logging
    # ----------------------------------------
    lgs = sppasLogSetup(50)
    lgs.null_handler()

except:
    print('{:s}\n'.format(sep))
    print('{}   -  Version {}'.format(sg.__name__, sg.__version__))
    print(sg.__copyright__)
    print(sg.__url__+'\n')
    print('{:s}\n'.format(sep))

    # Redirect all messages to a quiet logging
    # ----------------------------------------
    lgs = sppasLogSetup(50)
    lgs.stream_handler()

# ----------------------------------------------------------------------------
# Annotation is here
# ----------------------------------------------------------------------------

p = ProcessProgressTerminal()
manager = sppasAnnotationsManager()
if args.merge:
    manager.set_do_merge(True)
manager.annotate(parameters, p)

try:
    term = TerminalController()
    print(term.render('\n${GREEN}{:s}${NORMAL}').format(sep))
    print(term.render('${RED}See {}.').format(parameters.get_report_filename()))
    print(term.render('${GREEN}Thank you for using {}.').format(sg.__name__))
    print(term.render('${GREEN}{:s}${NORMAL}').format(sep))
except:
    print('\n{:s}\n'.format(sep))
    print("See {} for details.\nThank you for using {}."
          "".format(parameters.get_report_filename(), sg.__name__))
    print('{:s}\n'.format(sep))
