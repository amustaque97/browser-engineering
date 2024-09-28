import tkinter
import tkinter.font

from url_parser import Url, lex
from text_style import Text, Tag

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
                self.window,
                width=WIDTH,
                height=HEIGHT,
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def load(self, url):
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi!")

    def load(self, url):
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c, font in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(
                x, 
                y - self.scroll, 
                text=c, 
                anchor="nw", 
                font=font
            )

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

def layout(tokens):
    weight = "normal"
    style = "roman"
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for tok in tokens:
        if isinstance(tok, Text):
            for word in tok.text.split():
                font = tkinter.font.Font(
                    size=16,
                    weight=weight,
                    slant=style,
                )
                w = font.measure(word)
                display_list.append((cursor_x, cursor_y, word, font))
                cursor_x += w + font.measure(" ")
                if cursor_x + w > WIDTH - HSTEP:
                    cursor_y += font.metrics("linespace") * 1.25
                    cursor_x = HSTEP
        elif tok.tag == "i":
            style = "italic"
        elif tok.tag == "/i":
            style = "roman"
        elif tok.tag == "b" or tok.tag == "h1":
            weight = "bold"
        elif tok.tag == "/b" or tok.tag == "/h1":
            weight = "normal"
    return display_list


if __name__ == "__main__":
    import sys
    Browser().load(Url(sys.argv[1]))
    tkinter.mainloop()


