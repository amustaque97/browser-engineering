from __future__ import annotations

import tkinter
import tkinter.font

from text_style import Text, Tag
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
# key will be tuple(size, weight, style)
FONTS = {}

def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,
                                 slant=style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]


class Layout:
    def __init__(self, tokens):
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 12

        for tok in tokens:
            self.token(tok)

    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        self.display_list.append((self.cursor_x, self.cursor_y, word, font))
        self.cursor_x += w + font.measure(" ")
        if self.cursor_x + w > WIDTH - HSTEP:
            self.cursor_y += font.metrics("linespace") * 1.25
            self.cursor_x = HSTEP


    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b" or tok.tag == "h1":
            self.weight = "bold"
        elif tok.tag == "/b" or tok.tag == "/h1":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4


