# FlashQuiz
## Installation & Running

`pip install flashquiz`

After installation is finished you can run the program by using the `flashquiz` command

## Usage

With the FlashQuiz window in focus, you can interact with the loaded flashcards with the mouse & keyboard:

- Left & Right arrows move to the previous/next flashcard correspondingly
- Up & Down arrows, as well as clicking the mouse, will flip the current flashcard over
R
## Optional Arguments

`flashquiz --arg ARG`

| Argument        | Behavior                                                      | Default                         |
|-----------------|---------------------------------------------------------------|---------------------------------|
| `--file`        | .csv file containing questions and answers for the flashcards | flashquiz/default.csv           |
| `--font`        | Sets the font for all text (must be pygame-supported)         | inkfree                         |
| `--cards_front` | .jpg file to use as the background for cards' front           | flashquiz/assets/card_front.jpg |
| `--cards_back`  | .jpg file to use as the background for cards' back            | flashquiz/assets/card_back.jpg  |
| `--h`           | Sets the window height                                        | 500                             |
| `--w`           | Sets the window width                                         | 700                             |
| `--title`       | Changes the window title                                      | FlashQuiz                       |
| `--fps`         | Set the fps for the window to run at                          | 30                              |


## Usage

Although FlashQuiz contains 10 default flashcards to show its functionality, this package is designed to help you study your own flashcards.

In order to study your own questions and answers, simply create a .csv file formatted:

| Questions   | Answers |
|-------------|---------|
| What's 1+1? | 2       |
| ...         | ...     |

Lets say for example you named this file `math.csv`

To use FlashQuiz with this custom .csv document, `cd` into the directory containing `math.csv` and run

`flashquiz --file math.csv`