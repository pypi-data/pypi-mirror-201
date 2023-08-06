from .card import Card
from pygame.sprite import Group as SpriteGroup


class Deck:
    def __init__(self):
        """
        Attributes:
        self.cards = the deck, a group of cards
        self.card_in_focus = the first card of the deck, the one to show onscreen
        self.focused_card_number = the card number of the focused card based on the initial deck order
        """
        self.cards = SpriteGroup()
        self.card_in_focus = SpriteGroup()
        self.focused_card_number = 1

    def add_card(self, question: str, answer: str) -> 'Deck':
        """:param question the question for the Card to add to the deck
            :param answer the Card's answer"""
        self.cards.add(Card().set_fields(question, answer))
        return self

    def add_card_from_list(self, add: [str]) -> 'Deck':
        """:param add list of two strings formatted [question, answer]"""
        self.cards.add(Card().set_fields(add[0], add[1]))
        return self

    def add_card_from_obj(self, add: Card):
        """:param add the Card object to add to this deck"""
        self.cards.add(add)
        return self

    def init_cards(self, front: str, back: str, font: str) -> 'Deck':
        """Set the background images for all self.cards
        :param front .jpg (500x250) pixels to use for the front
        :param back .jpg to use for the back
        :param font name of the pygame font to load"""
        for card in self.cards:
            card.set_imgs(front, back)
            card.load_text(font)
        return self

    def get_first_card(self) -> SpriteGroup:
        """Get the current focused card as a pygame.Sprite.Group"""
        temp_group = SpriteGroup()
        temp_group.add(self.cards.sprites()[0])
        return temp_group

    def move_to_back(self, mv_card: Card) -> SpriteGroup:
        """Move the given card to the back of self.cards
        :param mv_card    the card to move to the back"""
        self.unflip()
        self.cards.remove(mv_card)
        self.cards.add(mv_card)
        return self.cards

    def move_first_to_back(self) -> SpriteGroup:
        """Move the self.card_in_focus to the back of self.cards"""
        self.iterate_focused_card(1)
        return self.move_to_back(self.cards.sprites()[0])

    def move_to_front(self, mv_card: Card) -> SpriteGroup:
        """Move the given card to the front of the deck
        :param mv_card   the card to move to the front"""
        self.unflip()
        grouplist = []
        for c in self.cards:
            grouplist.append(c)
        grouplist.remove(mv_card)
        grouplist.insert(0, mv_card)
        tempgroup = SpriteGroup()
        for c in grouplist:
            tempgroup.add(c)
        self.cards = tempgroup
        return self.cards

    def unflip(self):
        """Reset all cards in the deck to the flipped=False side"""
        for card in self.cards:
            if card.flipped:
                card.flip()

    def move_last_to_front(self) -> SpriteGroup:
        """Move the last card in the deck to the front"""
        self.iterate_focused_card(-1)
        return self.move_to_front(self.cards.sprites()[-1])

    def iterate_focused_card(self, by: int) -> int:
        """Iterates the self.focused_card_number variable, and resets it to 1 or len(self.cards) if needed
        :param by  the number to add to the current card number"""
        if self.focused_card_number + by > len(self.cards):
            self.focused_card_number = 1
        elif self.focused_card_number + by < 1:
            self.focused_card_number = len(self.cards)
        else:
            self.focused_card_number += by
        return self.focused_card_number

    def print(self):
        """Print each question: answer in the deck"""
        for card in self.cards:
            print(f"{card.question}: {card.answer}")
