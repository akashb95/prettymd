from typing import Literal, List
import re
from heading import Heading


class PrettyMD:
    HEADING_LEVEL = Literal[1, 2, 3, 4, 5, 6]

    # Headings start with '#' chars, which can have upto 3 whitespaces before it.
    # Heading then needs to have some text after it that is not whitespace or #.
    HEADING_REGEX = re.compile(r'^_{,3}(#{1,6})\s*([^#].+)\s*', re.MULTILInseINE)

    BULLET_POINT_CHAR = "*"

    def __init__(self, original: str, includes_title: bool = False, link: bool = True, back_to_toc_link: bool = True):
        """

        :param original: Input Markdown text.
        :param includes_title: Whether a Title is included in the input text. If so, it'll be excluded from the ToC.
        :param link: Whether to include hyperlinks from the ToC to the relevant headings.
        :param back_to_toc_link: Whether to include hyperlinks at end of each section that navigates to the ToC.
        """

        self._input = original
        self._output = ""
        self._includes_title = includes_title
        self._link = link
        self._navlink = back_to_toc_link

        self.title = None

        # Root node of Contents
        self._contents_tree = Heading(val=None, level=-1, start=0, end=0, subheadings=None, height=-1)

        # table of contents - need to join with \n
        self._toc_items = ["<a name='nav'></a>\n## Contents 🗺"]

        # Updates self._contents_tree - adds all Headings as subheadings. Still a mostly-flat structure.
        self.parse_headings()

        # if MD includes title, then don't put title in ToC, and put ToC's location to begin after the title.
        if self._includes_title:
            all_headings = self._contents_tree.subheadings[1:]
            self._toc_location = self._contents_tree.subheadings[0].end
        else:
            all_headings = self._contents_tree
            self._toc_location = 0

        # Make Contents Tree from list of Headings. Unflattened structure.
        self._contents_tree.set_subheadings(self.construct_contents_tree(all_headings))

        # update self._toc_items
        self.make_toc()
        return

    def parse_headings(self) -> None:
        """
        Finds using RegEx the headings in :instance_attribute:`self._input`. Add all these headings to the root of the
        contents tree, that is the :instance_attribute:`self._contents_tree`.

        :return:
        """

        # find all headings by matching regex
        headings_iterator = re.finditer(self.HEADING_REGEX, self._input)

        # make Heading objects and put them all in as roots to the Contents Tree.
        for i, heading_match in enumerate(headings_iterator):
            level = self.get_heading_level(heading_match.group(1))
            text = heading_match.group(2).rstrip()

            subheading = Heading(val=text, level=level, start=heading_match.start(), end=heading_match.end())
            self._contents_tree.add_subheading(subheading)

        if self._includes_title:
            self.title = self._contents_tree.subheadings[0]

        return

    def make_toc(self) -> None:
        """
        Updates :instance_attribute:`self._toc_items` with text that represents the Table of Contents.

        :return:
        """

        # 1st element is the root of the graph, which is always going to have val=None
        flattened_toc = self.flatten_contents_tree(self._contents_tree)[1:]

        i = 0
        while i < len(flattened_toc):

            if self._link:
                toc_line = "[{}](#{})".format(flattened_toc[i].val, flattened_toc[i].anchor_name)
            else:
                toc_line = "{}".format(flattened_toc[i].val)

            self._toc_items.append("\t" * flattened_toc[i].height + "{} {}".format(self.BULLET_POINT_CHAR, toc_line))

            i += 1

        # if ToC lines to be linked to the Headings, insert the anchors.
        if self._link:
            self.insert_anchors(flattened_toc)
        else:
            self._output = self._input

        return

    def flatten_contents_tree(self, heading: Heading) -> List[Heading]:
        """
        In-order traversal of :instance_attribute:`self._contents_tree`

        :return:
        """

        flat_contents_tree = [
            Heading(val=heading.val, level=heading.level, height=heading.height, start=heading.start, end=heading.end)]

        if len(heading) == 0:
            return flat_contents_tree

        for subheading in heading.subheadings:
            flat_contents_tree.extend(self.flatten_contents_tree(subheading))

        return flat_contents_tree

    def insert_anchors(self, flattened_toc: List[Heading]) -> None:
        """
        Inserts the anchors before each of the headings.

        Updates :instance_attribute:`self._output`.

        :param flattened_toc:
        :return:
        """

        input_str_ptr = 0
        if self._includes_title:
            input_str_ptr = flattened_toc[0].end

        for heading in flattened_toc:

            # get anchor str e.g. <a name='#anchor'></a>
            anchor = heading.generate_anchor()

            navlink = ""
            if self._navlink:
                navlink = "\n[🗺 Go back to Navigation &uarr;‍](#nav)\n\n"

            # update _output string by inserting anchor before the heading text
            self._output += "{}\n{}{}\n{}" \
                .format(self._input[input_str_ptr:heading.start], navlink,
                        anchor, self._input[heading.start:heading.end])

            # update pointer in _input string
            input_str_ptr = heading.end

        self._output += self._input[input_str_ptr:] + "\n\n[🗺 Go back to Navigation &uarr;‍](#nav)\n"

        return

    @staticmethod
    def get_heading_level(heading: str) -> HEADING_LEVEL:
        return min(len(heading), 6)

    @staticmethod
    def construct_contents_tree(headings_list: List[Heading]) -> List[Heading]:
        """
        Constructs a Tree that represents the Contents from a flat List of :class:`Heading`.

        :param headings_list:
        :return:
        """

        if len(headings_list) == 0:
            return []

        # list of root Headings
        graph = []
        lowest_level = headings_list[0].level

        for i, heading in enumerate(headings_list):
            if heading.level <= lowest_level:

                if heading.level < lowest_level:
                    lowest_level = heading.level

                graph.append(heading)

            else:
                subheading = Heading(heading.val, heading.level, heading.start, heading.end)
                graph[-1].add_subheading(subheading)

        for heading in graph:
            subheadings = PrettyMD.construct_contents_tree(heading.subheadings)
            heading.set_subheadings(subheadings)

        return graph

    @property
    def toc(self):
        return "\n".join(self._toc_items)

    @property
    def output(self):
        title = ""
        if self.title is not None:
            title = self._input[:self.title.end]

        return "{title}\n{contents}{body}".format(title=title, contents=self.toc, body=self._output)


if __name__ == "__main__":
    md_text = "## Hello \n" \
              "### Is it me you're looking for?\n" \
              "#### I can see it in your eyes\n" \
              "## I can feel it\n" \
              "\n\n\n\nsome random text §§§ `` potato           \n" \
              "# in my bones"

    p = PrettyMD(md_text, includes_title=False, link=True)

    assert (p.toc == "<a name='nav'></a>\n## Contents 🗺"
                     "\n"
                     "* [Hello](#hello)\n"
                     "\t* [Is it me you're looking for?](#is-it-me-youre-looking-for)\n"
                     "\t\t* [I can see it in your eyes](#i-can-see-it-in-your-eyes)\n"
                     "* [I can feel it](#i-can-feel-it)\n"
                     "* [in my bones](#in-my-bones)"), \
        "Generated ToC appears to be wrong!"

    with open("./markdowns/input_0.md", "r") as file:
        input_md = file.read()

    p = PrettyMD(input_md, includes_title=True, link=True, back_to_toc_link=True)
    print(p.output)
