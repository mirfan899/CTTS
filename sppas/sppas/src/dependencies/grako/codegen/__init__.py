# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from sppas.src.dependencies.grako.exceptions import CodegenError
from sppas.src.dependencies.grako.codegen.cgbase import *  # noqa
from sppas.src.dependencies.grako.codegen import python


pythoncg = python.codegen


def codegen(model, target='python'):
    if target.lower() == 'python':
        return pythoncg(model)
    else:
        raise CodegenError('Unknown target language: %s' % target)
