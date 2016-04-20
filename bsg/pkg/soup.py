#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

from pygments import highlight

from . import clexer, cformatter


class BSG(object):

    css_ht_tag = 'bsg-css-ht'

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_ht_html(self, soupstr):
        try:
            tags = eval('self.soup('+soupstr+')')
        except:
            tags = []

        for t in tags:
            t.wrap(self.soup.new_tag('bsg-ht'))

        html_lexer = clexer.BSGHtmlLexer()
        html_formatter = cformatter.BSGHtmlFormatter()
        highlight_html = highlight(self.soup.prettify(), html_lexer, html_formatter)

        highlight_html = re.sub("<bsg-ht>\s*\n", "<bsg-ht>", highlight_html)
        highlight_html = re.sub(">[\s\n]*</bsg-ht>", "></bsg-ht>", highlight_html)

        return highlight_html

    def highlight_by_css(self, css_str):
        tags = self.soup.select(css_str)

        if not tags:
            return self.soup.prettify()

        return self._highlight(tags, self.css_ht_tag)

    def _highlight(self, tags, wrap_str):
        for t in tags:
            t.wrap(self.soup.new_tag(wrap_str))

        html_lexer = clexer.BSGHtmlLexer()
        html_formatter = cformatter.BSGHtmlFormatter()
        highlight_html = highlight(self.soup.prettify(), html_lexer, html_formatter)

        wrap_tag, wrap_tag_end = "<{}>".format(wrap_str), "</{}>".format(wrap_str)
        highlight_html = re.sub(
            r">[\s\n]*{}".format(wrap_tag_end), ">"+wrap_tag_end,
            re.sub(r"{}\s*\n".format(wrap_str), wrap_tag, highlight_html)
        )
        return highlight_html
