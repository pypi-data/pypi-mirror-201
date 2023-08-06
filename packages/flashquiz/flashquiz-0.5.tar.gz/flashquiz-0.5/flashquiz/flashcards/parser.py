from .deck import Deck


# For parsing csv documents into question | answer format


def from_csv(filepath: str) -> Deck:
    """Takes the first two columns of the filepath csv and translates them into col1: questions col2: answers
    :param filepath the path to the input csv"""
    csv_deck = Deck()
    with open(filepath, "r") as f:
        for line in f.readlines():
            csv_deck.add_card_from_list(line.strip().split(","))
    return csv_deck
