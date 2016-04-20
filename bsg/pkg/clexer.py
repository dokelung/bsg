#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygments import lexer
from pygments import lexers

from . import ctoken


class BSGHtmlLexer(lexers.HtmlLexer):

    tokens = {
        'root': [
            # BSG custom tags.
            (r'</*bsg-ht>', ctoken.BSG_HT),
            (r'</*bsg-css-ht>', ctoken.BSG_CSS_HT),
            # inherit
            lexer.inherit,
        ],
    }
