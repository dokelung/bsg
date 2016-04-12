#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pygments import lexers

from . import ctoken

class BSGHtmlLexer(lexers.HtmlLexer):

    def __init__(self, **options):
        super(BSGHtmlLexer, self).__init__(**options)

        # see: pygments/lexer.py #419
        # XXX: we are using inproper way to extend here...
        self._tokens['root'].insert(3, (re.compile(r'</*bsg-ht>').match, ctoken.BSG_HT, None))
