from pygame.font import SysFont


class Text:
    """Manages all text to display onscreen (except for flashcards text)"""
    def __init__(self, text: str, x: int, y: int, font: str, size: int = 30, red: int = 255, green: int = 255, blue: int = 255):
        self.text = text
        self.field = SysFont(font, size, italic=False, bold=False)
        self.font = font
        self.sprite = self.field.render(self.text, True, (red, green, blue))
        self.rect = self.sprite.get_rect()
        self.x, self.y = x, y

    def render_text(self, surface, x_offset=0, y_offset=0):
        """Renders text without wrap"""
        self.rect.center = (self.x + x_offset, self.y + y_offset)
        self.field = self.field.render(self.text, True, (255, 255, 255))
        surface.blit(self.sprite, self.rect)
