import math
from .locals import ascii_chars as default_chars


class Consol:
    def __init__(
        self,
        consol_width: int = 18,
        char_height: int = 7,
        char_width: int = 8,
        char_set: dict = default_chars,
    ) -> None:
        """The default_chars only have numbers and uppercase letters A to Z"""
        self.consol_width = consol_width
        self.char_height = char_height
        self.char_width = char_width
        self.char_set = char_set

        # Debug settings
        self.debug_mode = False

    def render(self, text: str):
        """Turns 'text' into a consol.print()-able list"""

        new_line_idx = list(range(math.ceil(len(text) / self.consol_width)))

        self.lines = []

        for line_idx in new_line_idx:
            txt_len = len(text)
            chars_to_print = line_idx * self.consol_width

            if "\n" in text:
                # TODO Handle newline characters in text
                # ! TEMP CODE
                start = line_idx * self.consol_width
                end = min(chars_to_print + self.consol_width, txt_len)
                # ! TEMP CODE

            else:
                start = line_idx * self.consol_width
                end = min(chars_to_print + self.consol_width, txt_len)

            text_line = text[start:end]

            line = []
            for _ in range(self.char_height):
                line.append("")

            for char_key in text_line:
                value = self.char_set[char_key]

                if char_key not in self.char_set.keys():
                    char_key = "$NOT_IN"

                for char_idx, char_str in enumerate(value):
                    line[char_idx] += char_str

            line[-1] += "\n"
            self.lines.append(line.copy())

    def print(self, text: str = "$NONE"):
        """If no input is given - prints the text set by consol.render()
        Else renders the new text (previous text will be deleted)"""
        if text != "$NONE":
            self.render(text)

        print(("\n" * 0))
        for text_line in self.lines:
            for line in text_line:
                print(line)

        print(("\n" * 0))

    def get_print(self, text: str = "$NONE"):
        """Returns the rendered text as a multi-line string"""

        if text != "$NONE":
            self.render(text)

        output_string = ""

        for text_line in self.lines:
            for line in text_line:
                output_string += f"{line}\n"

        return output_string


if __name__ == "__main__":
    from terminal import getTerminalSize

    tw, th = getTerminalSize()

    chars_per_line = tw // 8

    consol = Consol(chars_per_line, 7, 8)
    consol.render("Hello World! This is my own text to ASCII renderer, 0123456789")
