from flashquiz.flashcards.parser import from_csv
from flashquiz.args import handle_args
from flashquiz.gui import GUI, Text


def main():
    args = handle_args()
    game = GUI(args).init_screen()

    # convert the csv given in args to our deck
    deck = from_csv(args.file).init_cards(args.cards_front, args.cards_back, args.font)
    run = True
    while run:
        game.screen.fill((0, 0, 0))

        # create text that displays card number
        card_number_txt = Text(f"#{deck.focused_card_number}", 100, 100, args.font)
        card_number_txt.render_text(game.screen)

        # set card_in_focus to first card in the deck (we only need to render the first card)
        card_in_focus = deck.get_first_card()
        card_in_focus.draw(game.screen)
        game.render(card_in_focus)

        # handle_events() will determine any changes to make to the deck based on the user input
        # (what should be the new card in focus) and returns the updated deck
        # it also keeps track of if we should continue running based on if the quit key has been pressed (escape)
        run, deck = game.handle_events(deck)

    game.quit()


if __name__ == '__main__':
    main()
