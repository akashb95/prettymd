"""
Defines a Tree class that will represent the headings and sub-headings, which will inherently by a node's height,
indicate the indentation level that the heading needs to have.

# TODO: Modify as required to implement prettymd.PrettyMD functionality.
"""

import re
from typing import List, Optional


class Heading:
    """
    Class that represents Headings, which can have 'child Headings', or subheadings, which can be nested to a level of
    6 headings. This is essentially a Graph data structure, where each Heading is a node.
    """

    NODE_VALUE_TYPES = Optional[str]

    def __init__(self, val: NODE_VALUE_TYPES, level: int, subheadings: Optional[List['Heading']] = None):
        """
        A :class:`Heading` instance is essentially a 'node' in a Tree.

        :param val: Heading text
        :param level: Number of '#' chars before heading text
        :param subheadings: Nested Headings.
        """

        self.val = val
        self.level = level
        self._children = subheadings if subheadings is not None else []

        self.anchor_name = self.generate_anchor_name()

        return

    def __len__(self):
        return len(self._children)

    def __str__(self):
        return "#" * self.level + "{}".format(self.val)

    def set_subheadings(self, subheadings: List['Heading']):
        """
        Set the list of Headings as the subheadings.

        :param subheadings:
        :return:
        """

        self._children = subheadings

        return

    def generate_anchor_name(self) -> str:
        """
        Generates the name to be used within the <a> tag by stripping all leading and trailing whitespaces, and
        substituting the remaining whitespaces with hyphens.

        e.g. 'Hello World' -> 'hello-world'.

        To be used in: <a name="hello-world"></a>.

        :return:
        """

        if self.val is not None:
            replaced_whitespace = re.sub(r'\s+', "-", self.val.strip().lower())
            return re.sub(r'[^a-zA-Z0-9\-]', "", replaced_whitespace)

        return ""

    def generate_anchor(self) -> str:
        return "<a name='{}'></a>".format(self.anchor_name)

    @property
    def subheadings(self) -> List['Heading']:
        """
        Return List of subheadings.

        :return:
        """

        return self._children
