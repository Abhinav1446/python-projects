


# 🎮 Number Guessing Game (Python)

This is a simple **terminal-based number guessing game** written in Python.

The player chooses a **difficulty level** (number of chances), selects a **range of numbers**, and then tries to guess the secret number. The game gives **hints**, tracks **stats** like games played / won, and keeps a **best score** (fewest attempts to win).

---

## 🚀 What this code does

- Asks the user to choose a **difficulty**:
  - Easy   → 10 chances  
  - Medium → 5 chances  
  - Hard   → 3 chances  
- Asks the user to choose a **number range** (minimum and maximum).
- Randomly picks a **secret number** in that range.
- Lets the user guess the number:
  - Tells if the secret number is **greater** or **less** than the guess.
  - Gives hints like:
    - 🔥 "Very close!" (difference ≤ 5)  
    - 🙂 "Getting closer." (difference ≤ 15)  
    - 🥶 "Very far away." (difference > 15)
- Tracks:
  - Total games played  
  - Games won  
  - Best game (fewest attempts used to win)
- Shows how many **seconds** the user took for each round.
- Lets the user **play again** or **exit**.

---

## 📂 File Overview

All logic is in a single Python file (for example):

```text
number_guess_game.py
````

Inside it, you’ll find:

* `class NumberGuessGame`:
  Contains the core game logic (difficulty selection, guessing loop, hints, range selection).

* `main()`:
  Runs the game loop, tracks stats, and asks whether the player wants to play again.

---

## 🧠 How the game works (Step-by-step)

1. **Start the game**

   * `main()` is called when you run the script.
   * It initializes:

     * `games_played`
     * `games_won`
     * `best_score` (fewest attempts so far)

2. **Choose difficulty**

   * `NumberGuessGame.get_difficulty()`:

     * Shows a menu: 1 (Easy), 2 (Medium), 3 (Hard)
     * Keeps asking until the user enters a valid number.
     * Returns the **number of chances** based on the selected difficulty.

3. **Select number range**

   * `NumberGuessGame.get_number_range()`:

     * Asks the user to enter a **minimum number** and **maximum number**.
     * Validates:

       * Both must be integers.
       * Minimum must be **less than** maximum.
     * Returns `(min_number, max_number)`.

4. **Play one round**

   * `NumberGuessGame.play_round(chances)`:

     * Picks a random secret number in the chosen range using `random.randint(min_number, max_number)`.
     * Allows the user to guess up to `chances` times.
     * For each guess:

       * User can type a number or `'q'` to quit the round.
       * Game tells if the guess is too high or too low.
       * Calls `check_close()` to tell how close the guess is.
     * If the player guesses correctly:

       * Returns the **number of attempts** used.
     * If the player fails to guess:

       * Shows the correct number.
       * Returns `None`.

5. **Update stats**

   * Back in `main()`:

     * `games_played` is incremented after each round.
     * If `attempts` is not `None`, the player won:

       * `games_won` is incremented.
       * `best_score` is updated if this game used fewer attempts than previous best.
     * Shows:

       * Games played
       * Games won
       * Best game (fewest attempts), or `N/A` if no wins yet.

6. **Play again?**

   * User is asked: `Do you want to play again? (y/n)`
   * If:

     * `y` → game starts another round.
     * `n` → game prints a goodbye message and exits.
     * anything else → game exits with a message.

---

## 🧩 Code Structure (High-level)

### `class NumberGuessGame`

* `get_difficulty(self) -> int`

  * Handles input for difficulty.
  * Returns number of chances (10 / 5 / 3).
  * Includes validation and error messages.

* `get_number_range(self) -> tuple[int, int]`

  * Asks for minimum and maximum numbers.
  * Ensures valid integers and that `min < max`.
  * Returns `(min_number, max_number)`.

* `check_close(self, human_number: int, computer_number: int) -> None`

  * Checks how close the guess is to the secret number.
  * Prints:

    * "Very close!"
    * "Getting closer."
    * "Very far away."

* `play_round(self, chances: int) -> int | None`

  * Core game loop for a single round.
  * Uses difficulty (chances) and the selected range.
  * Returns:

    * `int` → number of attempts if the player wins.
    * `None` → if player fails to guess or quits with `'q'`.

### `main()`

* Initializes stats:

  * `games_played`, `games_won`, `best_score`.
* Runs a `while True` game loop:

  * Gets difficulty.
  * Plays one round.
  * Measures time taken.
  * Updates stats.
  * Prints stats.
  * Asks if user wants to play again.

---

## ▶️ How to run the game

1. Make sure you have **Python 3** installed.

2. Save the script as, for example:

```text
number_guess_game.py
```

3. Run it from the terminal:

```bash
python number_guess_game.py
```

4. Follow on-screen instructions:

   * Choose difficulty.
   * Select number range.
   * Start guessing!

---

## ✅ Example session

```text
Welcome to the Number Guessing Game!
Choose a difficulty level:
1. Easy   (10 chances)
2. Medium (5 chances)
3. Hard   (3 chances)

Please select the difficulty level (1/2/3): 2

😄 Great! You selected MEDIUM difficulty.

Select the range of numbers.
Select the minimum number: 10
Select the maximum number: 50

I'm thinking of a number between 10 and 50.
You have 5 chances. Good luck!

Enter your guess (or 'q' to quit this round): 30
Incorrect! The number is GREATER than your guess.
🙂 Getting closer.

Enter your guess (or 'q' to quit this round): 40
Incorrect! The number is LESS than your guess.
🔥 Very close!

Enter your guess (or 'q' to quit this round): 37

🎉 Congratulations! You guessed the correct number in 3 attempts.

⏱ You took 12.45 seconds for this round.

📊 Stats so far:
   Games played : 1
   Games won    : 1
   Best game    : 3 attempts

Do you want to play again? (y/n):
```

---

## 🛠 Possible Improvements

Some ideas you can add later:

* Save `games_played`, `games_won`, `best_score` in a file (persistent stats).
* Add difficulty-based score (e.g., more points for winning on Hard).
* Add color to text using `colorama` for better UI.
* Limit the range (e.g., min ≥ 1, max ≤ 1000).
* Add a “practice mode” with unlimited guesses.

---

## 📚 Purpose of this project

This project is great for practicing:

* Basic Python syntax
* Loops (`while`, `if/elif/else`)
* Functions and classes
* Input validation (`try/except`)
* Random number generation (`random.randint`)
* Simple game design and user interaction
* Tracking and updating state across rounds (stats)

It’s a solid beginner project to understand **control flow** and **user interaction** in Python.


