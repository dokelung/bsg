#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

from pygments import highlight, token
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

import pkg.clexer as clexer
import pkg.cformatter as cformatter

class BSG:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_ht_html(self, soupstr):
        try:
            tags = eval('self.soup('+soupstr+')')
        except:
            tags = []

        for t in tags:
            t.wrap(self.soup.new_tag('bsg-ht'))
        # Garfield: apply pipeline to find other types like content, class, id, url ...

        html_lexer = clexer.BSGHtmlLexer()
        html_formatter = cformatter.BSGHtmlFormatter()
        highlight_html = highlight(self.soup.prettify(), html_lexer, html_formatter)

        highlight_html = re.sub("<bsg-ht>\s*\n", "<bsg-ht>", highlight_html)
        highlight_html = re.sub(">[\s\n]*</bsg-ht>", "></bsg-ht>", highlight_html)

        return highlight_html
