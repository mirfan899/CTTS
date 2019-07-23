# -*- coding: utf-8 -*-
"""
Tests for consistency of the line information caches kept by
grako.buffering.Buffer.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import random
import unittest

from dependencies.grako.buffering import Buffer


class BufferingTests(unittest.TestCase):

    def setUp(self):
        testfile = os.path.splitext(__file__)[0] + '.py'
        with open(testfile) as f:
            self.text = str(f.read())
        self.buf = Buffer(self.text, whitespace='')

    def test_pos_consistency(self):
        line = col = 0
        for p, c in enumerate(self.text):
            bl, bc = self.buf.line_info(p)[1:3]
            d = self.buf.next()
#            print('tx', line, col, c.encode('string-escape'))
#            print('bu', bl, bc, d.encode('string-escape'))
            self.assertEqual(bl, line)
            self.assertEqual(bc, col)
            self.assertEqual(d, c)
            if c == '\n':
                col = 0
                line += 1
            else:
                col += 1

    def test_next_consisntency(self):
        while not self.buf.atend():
            bl, bc = self.buf.line_info()[1:3]
#            print('li', bl, bc)
#            print('bu', self.buf.line, self.buf.col)
            self.assertEqual(bl, self.buf.line)
            self.assertEqual(bc, self.buf.col)
            self.buf.next()

    def test_goto_consistency(self):
        for _ in range(100):
            self.buf.goto(random.randrange(len(self.text)))
            bl, bc = self.buf.line_info()[1:3]
#            print('li', bl, bc)
#            print('bu', self.buf.line, self.buf.col)
            self.assertEqual(bl, self.buf.line)
            self.assertEqual(bc, self.buf.col)

    def test_line_consistency(self):
        lines = self.text.splitlines()
        for n, line in enumerate(lines):
            self.assertEqual(line, self.buf.get_line(n))

    def test_line_info_consistency(self):
        lines = self.text.splitlines(True)
        line = 0
        col = 0
        start = 0
        for n, char in enumerate(self.text):
            info = self.buf.line_info(n)
            self.assertEqual(info.line, line)
            self.assertEqual(info.col, col)
            self.assertEqual(info.start, start)
            self.assertEqual(info.text, lines[line])
            col = col + 1
            if char == '\n':
                line += 1
                col = 0
                start = n + 1
        text_len = len(self.text)
        info = self.buf.line_info(text_len)
        self.assertEqual(info.line, len(self.text.splitlines()))
        self.assertEqual(info.start, text_len)

    def test_linecount(self):
        b = Buffer('')
        self.assertEqual(1, b.linecount)

        b = Buffer('Hello World!')
        self.assertEqual(1, b.linecount)

        b = Buffer('\n')
        self.assertEqual(2, b.linecount)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(BufferingTests)


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())

if __name__ == '__main__':
    main()
