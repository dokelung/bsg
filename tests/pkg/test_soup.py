#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from bsg.pkg import soup


class TestSoup(unittest.TestCase):

    def test_get_ht_html(self):

        # simple
        bsg = soup.BSG("<html><body></body></html>")
        content = bsg.get_ht_html('"body"')
        wrapped_content = (
            '<div class="highlight"><pre>'
            '<span></span><span class="p">&lt;</span><span class="nt">html</span><span class="p">&gt;</span>\n'
            '<bsg-ht>  <span class="p">&lt;</span><span class="nt">body</span><span class="p">&gt;</span>'
            '\n  <span class="p">&lt;/</span><span class="nt">body</span><span class="p">&gt;</span></bsg-ht> \n'
            '<span class="p">&lt;/</span><span class="nt">html</span><span class="p">&gt;</span>\n'
            '</pre></div>\n'
        )
        self.assertEqual(wrapped_content, content)
