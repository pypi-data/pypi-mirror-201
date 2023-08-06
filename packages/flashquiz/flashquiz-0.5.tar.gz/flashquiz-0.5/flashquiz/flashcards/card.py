# contains class for flashcards with question and answers
from pygame.sprite import Sprite
from pygame.font import SysFont
from pygame.image import load
from pygame import Rect, Surface


class Card(Sprite):
    def __init__(self, x: int = 110, y: int = 120):
        """:param x starting x-position
        :param y starting y-position"""
        super().__init__()
        self.x, self.y = x, y
        self.font, self.text_sprite, self.text_rect = None, None, None
        self.question, self.answer = None, None
        self.rect, self.image = None, None
        self.front, self.back = None, None
        self.flipped = False

    def set_fields(self, question: str, answer: str):
        """Set question & answer fields, used in addition to __init__ for instantiating a flashcard
        :param question text of the card
        :param answer text for the card"""
        self.question, self.answer = question, answer
        return self

    def set_pos(self, x: int, y: int):
        """Set the card's position
        :param x new x-position
        :param y new y-position"""
        self.x, self.y = x, y

    def set_imgs(self, front: str, back: str):
        """Load the images initially
        :param front image path for the self.flipped=False side
        :param back image path for the self.flipped=True side"""
        self.front, self.back = front, back
        self.refresh_img()

    def load_text(self, font):
        """Load the text font and text sprite (without rendering)"""
        self.font = SysFont(font, 30, italic=False, bold=False)
        self.text_sprite = self.font.render(self.question, True, (255, 255, 255))
        self.text_rect = self.text_sprite.get_rect()

    def render_text(self, surface, x_offset=250, y_offset=115):
        """Renders text without wrap"""
        if self.flipped:
            txt = self.answer
        else:
            txt = self.question
        self.text_rect.center = (self.x + x_offset, self.y + y_offset)
        self.text_sprite = self.font.render(txt, True, (255, 255, 255))
        surface.blit(self.text_sprite, self.text_rect)

    def render_textwrap(self, surface: Surface, color: (int, int, int) = None,
                        font: SysFont = None, padding_left: int = 40, rect: Rect = None, aa=True):
        """Renders text on a card while wrapping anything that goes over its rect boundaries
           Function adapted from https://www.pygame.org/wiki/TextWrap
           :param surface which screen to draw text on
           :param color text color
           :param font text font
           :param padding_left how much space to leave on the left
           :param rect the rect to draw text on
           :param aa enable anti-aliasing?"""
        if color is None:
            color = (255, 255, 255)
        if rect is None:
            rect = self.rect
        if self.flipped:
            text = self.answer
        else:
            text = self.question
        if font is None:
            font = self.font

        lineSpacing = -2
        # get the height of the font
        fontHeight = font.size("Tg")[1]
        max_lines = int((rect.height - fontHeight) / (fontHeight + lineSpacing))

        # calculate the total number of lines for the given text
        rectWidth = rect.width - padding_left
        words = text.split()
        # calculate the width of each word
        wordWidths = [font.size(word)[0] for word in words]
        # calculate the number of lines required
        numLines = 1
        lineWidth = 0
        for i, word in enumerate(words):
            # add the width of the current word to the line width
            lineWidth += wordWidths[i]
            # add the width of the space character
            if i < len(words) - 1:
                lineWidth += font.size(' ')[0]
            # if the line width exceeds the width of the rect, start a new line
            if lineWidth > rectWidth:
                numLines += 1
                lineWidth = wordWidths[i]

        # center the text on the y-axis
        y = rect.top + (rect.height - (numLines * (fontHeight + lineSpacing) - lineSpacing)) // 2

        while text:
            i = 1
            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break
            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width - padding_left and i < len(text):
                i += 1
            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1
            image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left + padding_left, y))
            y += fontHeight + lineSpacing
            # remove the text we just blitted
            text = text[i:]
        return text

    def refresh_img(self):
        """Load the image corresponding to what side self.flipped shows"""
        if self.flipped:
            self.image = load(self.back)
        else:
            self.image = load(self.front)
        self.rect = self.image.get_rect()

    def flip(self):
        """Invert self.flipped and the card image"""
        self.flipped = not self.flipped
        self.refresh_img()

    def update(self) -> None:
        """Override pygame's default sprite update() to set the card's rect (actual) position to the correct values"""
        self.rect.x, self.rect.y = self.x, self.y

