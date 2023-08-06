import pygame
from ..flashcards import Deck
from pygame.sprite import Group as SpriteGroup


class GUI:
    def __init__(self, opts):
        self.screen, self.clock = None, None
        self.window_name = opts.title
        self.dimensions = (opts.w, opts.h)
        self.FPS = opts.fps

    def init_screen(self) -> 'GUI':
        """initialize the pygame environment, reset its clock, and initialize the pygame gui window"""
        pygame.init()
        self.reset_clock()
        self.screen = pygame.display.set_mode(self.dimensions)
        pygame.display.set_caption(self.window_name)
        return self

    def reset_clock(self):
        """reset pygame's clock"""
        self.clock = pygame.time.Clock()

    def render(self, group: SpriteGroup):
        """Render the card visible in the current frame
        :param group the group of cards to render (Deck().cards)"""
        self.clock.tick(self.FPS)
        card = group.sprites()[0]  # in this game we won't ever display anything except the first card in a deck
        card.update()
        card.render_textwrap(self.screen)
        pygame.display.update()

    @staticmethod
    def handle_events(deck: Deck) -> (bool, Deck):
        """Given a deck of flashcards, handle the 'pygame events' and determine the new deck orientation
            The user inputs will determine what card should be moved to the front/back, and the new deck is returned
            along with whether the game should continue running or not (based on if the quit button was pressed)
        :param deck the deck of flashcards to use, manipulate, and return"""
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.MOUSEBUTTONDOWN or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                deck.cards.sprites()[0].flip()  # first card of the deck is the only one in view
            if keys[pygame.K_RIGHT]:
                deck.move_first_to_back()
            if keys[pygame.K_LEFT]:
                deck.move_last_to_front()
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT:
                return False, deck
        return True, deck

    @staticmethod
    def get_mouse_pos() -> (int, int):
        """return the mouse position according to pygame"""
        return pygame.mouse.get_pos()

    @staticmethod
    def quit():
        """quit pygame"""
        pygame.quit()
