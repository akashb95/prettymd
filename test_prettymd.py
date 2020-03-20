"""
Unit tests and integration tests for prettymd.PrettyMD class.
"""

from unittest import TestCase
from .prettymd import PrettyMD


class TestPrettyMD(TestCase):
    def test_parse_headings(self):



        return

    def test_make_toc(self):
        self.fail()

    def test_flatten_contents_tree(self):
        self.fail()

    def test_insert_anchors(self):
        self.fail()

    def test_get_heading_level(self):
        self.fail()

    def test_construct_contents_tree(self):
        self.fail()

    def test_toc(self):
        self.fail()

    def test_output(self):
        with open("./markdowns/input_0.md") as file:
            md_text = file.read()
        with open("./markdowns/output_0.md") as file:
            expected_output = file.read()

        p = PrettyMD(md_text, includes_title=False, link=True)

        self.assertEqual(p.output, expected_output)
        return
