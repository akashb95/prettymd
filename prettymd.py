from typing import Literal, List
import re
from heading import Heading


class PrettyMD:

    # Headings start with '#' chars, which can have upto 3 whitespaces before it.
    # Heading then needs to have some text after it that is not whitespace or #.
    HEADING_REGEX = re.compile(r'^_{,3}(#{1,6})\s*([^#].+)\s*', re.MULTILINE)

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
        self._toc = ""

        # TODO
        return

    def parse_headings(self) -> None:
        """
        Finds using RegEx the headings in :instance_attribute:`self._input`. Add all these headings to the root of the
        contents tree, that is the :instance_attribute:`self._contents_tree`.

        :return:
        """

        # TODO: find each heading in the input Markdown using RegEx, and store in an instance variable.

        raise NotImplementedError("TODO!")

    def make_toc(self):
        """
        Updates :instance_attribute:`self._toc_items` with text that represents the Table of Contents.

        :return:
        """

        # TODO: Construct the text that represents the Table of Contents and store this in an instance variable.
        # Hint: Look at if __name__ == "__main__" for guidance on how the contents should look

        raise NotImplementedError("TODO!")

    def insert_anchors(self, flattened_toc: List[Heading]) -> None:
        """
        Inserts the anchors before each of the headings.

        e.g.

        ```
        ## Heading Example
        ...
        ```

        BECOMES

        ```

        [Go back to Navigation](#nav)

        <a name="heading-example"></a>
        ## Heading Example
        ...
        ```

        Updates :instance_attribute:`self._output`.

        :param flattened_toc:
        :return:
        """

        raise NotImplementedError("TODO!")

    @staticmethod
    def get_heading_level(heading: str):
        return min(len(heading), 6)

    @property
    def toc(self):
        return self._toc

    @property
    def output(self):
        """
        Return thte full output text, including the title, followed by the Table of Contents, followed by the main body
        of text.

        :return:
        """

        raise NotImplementedError("TODO!")


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
