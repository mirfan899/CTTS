# -*- coding: utf-8 -*-
"""
Implements parsing of Grako's EBNF idiom for grammars, and grammar model
creation using the .grammars module.

GrakoParserRoot is the bootstrap parser. It uses the facilities of parsing.Parser
as generated parsers do, but it does not conform to the patterns in the generated
code. Why? Because having Grako bootstrap itself from its grammar would be cool,
but very bad engineering. GrakoParserRoot is hand-crafted.

The GrakoGrammarGenerator class, a descendant of GrakoParserRoot constructs
a model of the grammar using semantic actions the model elements defined
in the .grammars module.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from sppas.src.dependencies.grako.bootstrap import GrakoBootstrapParser
from sppas.src.dependencies.grako.grammars import GrakoContext
from sppas.src.dependencies.grako.semantics import GrakoASTSemantics, GrakoSemantics

__all__ = ['GrakoParser', 'GrakoGrammarGenerator']


class GrakoParserBase(GrakoBootstrapParser, GrakoContext):
    pass


class GrakoParser(GrakoParserBase):
    def __init__(self, grammar_name, semantics=None, **kwargs):
        if semantics is None:
            semantics = GrakoASTSemantics()
        super(GrakoParser, self).__init__(semantics=semantics, **kwargs)


class GrakoGrammarGenerator(GrakoParserBase):
    def __init__(self, grammar_name, semantics=None, parseinfo=True, **kwargs):
        if semantics is None:
            semantics = GrakoSemantics(grammar_name)
        super(GrakoGrammarGenerator, self).__init__(
            semantics=semantics,
            parseinfo=True,
            **kwargs
        )
