"""
Defines a Tree class that will represent the headings and sub-headings, which will inherently by a node's height,
indicate the indentation level that the heading needs to have.
"""

import re
from typing import List, Optional


class Heading:
    """
    Class that represents Headings, which can have 'child Headings', or subheadings, which can be nested to a level of
    6 headings. This is essentially a Graph data structure, where each Heading is a node.
    """

    NODE_VALUE_TYPES = Optional[str]

    def __init__(self, val: NODE_VALUE_TYPES, level: int, start: int, end: int,
                 subheadings: Optional[List['Heading']] = None, height: Optional[int] = 0):
        """
        A :class:`Heading` instance is essentially a 'node' in a Tree.

        :param val: Heading text
        :param level: Number of '#' chars before heading text
        :param start: Starting location of Heading
        :param end: End location of Heading
        :param subheadings: Nested Headings.
        :param height: Nesting level/indentation level
        """

        self.val = val
        self.level = level
        self._children = subheadings if subheadings is not None else []
        self.height = height if height is not None else 0

        self.anchor_name = self.generate_anchor_name()

        self._start = start
        self._end = end

        return

    def __len__(self):
        return len(self._children)

    def __str__(self):
        return "#" * self.level + "{}".format(self.val)

    def __getitem__(self, item):
        return self._children[item]

    def add_subheading(self, subheading: 'Heading') -> None:
        """
        Append a node to :instance_parameter:`children` with incremented height.

        :param subheading:
        :return:
        """

        subheading.height = self.height + 1
        self._children.append(subheading)

        return

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
            return re.sub(r'[^a-zA-z0-9\-]', "", replaced_whitespace)

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

    @property
    def start(self) -> int:
        """
        String location - where the Heading starts.

        :return:
        """

        return self._start

    @property
    def end(self) -> int:
        """
        String location - where the Heading ends.

        :return:
        """

        return self._end
