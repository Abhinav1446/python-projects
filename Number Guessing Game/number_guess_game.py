import random
import sys
import time


class NumberGuessGame:
    """
    A simple number guessing game:
    - Player picks a difficulty (which sets number of chances)
    - Player optionally chooses a custom range
    - Game generates a random number in that range
    - Player tries to guess within the allowed chances
    """

    def __init__(self):
        pass

    # ---------- Helper methods ----------

    def check_close(self, human_number: int, computer_number: int) -> None:
        """
        Print a hint about how close the guess is to the actual number.
        """
        diff = abs(human_number - computer_number)
        if diff <= 5:
            print("🔥 Very close!")
        elif diff <= 15:
            print("🙂 Getting closer.")
        else:
            print("🥶 Very far away.")

    def get_number_range(self) -> tuple[int, int]:
        """
        Ask the user to enter a minimum and maximum number.
        Ensures valid integers and that min < max.
        Returns (min_number, max_number).
        """
        while True:
            try:
                min_input = input("\nSelect the minimum number: ")
                min_number = int(min_input)
            except ValueError:
                print("❌ Invalid input! Please enter a valid integer for minimum.")
                continue  # ask again

            try:
                max_input = input("Select the maximum number: ")
                max_number = int(max_input)
            except ValueError:
                print("❌ Invalid input! Please enter a valid integer for maximum.")
                continue  # ask again

            if min_number >= max_number:
                print("❌ Minimum must be less than maximum. Please try again.")
                continue

            return min_number, max_number

    # ---------- Core game logic ----------

    def play_round(self, chances: int) -> int | None:
        """
        Play one round of the game with the given number of chances.
        Returns:
            - int: number of guesses used (if player wins)
            - None: if player fails to guess correctly
        """
        number_of_guesses = 0

        print("\nSelect the range of numbers.")
        min_number, max_number = self.get_number_range()

        # Generate secret number in [min_number, max_number] inclusive
        computer_num = random.randint(min_number, max_number)

        print(f"\nI'm thinking of a number between {min_number} and {max_number}.")
        print(f"You have {chances} chances. Good luck!")

        while number_of_guesses < chances:
            # Take guess safely
            human_input = input("\nEnter your guess (or 'q' to quit this round): ")

            if human_input.lower() == "q":
                print("You chose to quit this round.")
                return None  # treat quitting as not winning

            try:
                human_number = int(human_input)
            except ValueError:
                print("❌ Invalid input! Please enter a valid integer.")
                continue  # don't count this as an attempt

            # Count this as a valid guess
            number_of_guesses += 1

            # Compare guess to secret number and give feedback
            if human_number > computer_num:
                print("Incorrect! The number is LESS than your guess.")
                self.check_close(human_number, computer_num)
            elif human_number < computer_num:
                print("Incorrect! The number is GREATER than your guess.")
                self.check_close(human_number, computer_num)
            else:
                print(
                    f"\n🎉 Congratulations! You guessed the correct number "
                    f"in {number_of_guesses} attempts."
                )
                return number_of_guesses  # won the game

        # If loop ends without returning, player failed
        print(f"\n❌ You failed to guess the correct number in {chances} attempts.")
        print(f"The correct number was: {computer_num}")
        return None  # lost the game

    def get_difficulty(self) -> int:
        """
        Ask the user for difficulty and return number of chances.
        Loops until a valid difficulty is chosen.
        """
        while True:
            print(
                "\nWelcome to the Number Guessing Game!"
                "\nChoose a difficulty level:"
                "\n1. Easy   (10 chances)"
                "\n2. Medium (5 chances)"
                "\n3. Hard   (3 chances)"
            )

            choice = input("\nPlease select the difficulty level (1/2/3): ")

            # Validate it's an integer
            try:
                difficulty = int(choice)
            except ValueError:
                print("❌ Invalid input! Please enter 1, 2, or 3.")
                continue

            if difficulty == 1:
                print("\n🙂 Great! You selected EASY difficulty.")
                return 10
            elif difficulty == 2:
                print("\n😄 Great! You selected MEDIUM difficulty.")
                return 5
            elif difficulty == 3:
                print("\n😈 Great! You selected HARD difficulty.")
                return 3
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")


# ---------- Main game loop and stats ----------

def main():
    # Overall stats across all rounds
    games_played = 0
    games_won = 0
    best_score: int | None = None  # lower is better (fewest attempts)

    while True:
        game = NumberGuessGame()

        # 1. Get difficulty → returns number of chances
        chances = game.get_difficulty()

        # 2. Time the round
        start_time = time.time()
        attempts = game.play_round(chances)
        end_time = time.time()

        elapsed = end_time - start_time
        games_played += 1

        # 3. Update stats if player won (attempts will be an int)
        if attempts is not None:
            games_won += 1
            # Update best_score: keep the smallest number of attempts
            if best_score is None or attempts < best_score:
                best_score = attempts

        # 4. Show round time
        print(f"\n⏱ You took {elapsed:.2f} seconds for this round.")

        # 5. Show stats so far
        print("\n📊 Stats so far:")
        print(f"   Games played : {games_played}")
        print(f"   Games won    : {games_won}")
        if best_score is not None:
            print(f"   Best game    : {best_score} attempts")
        else:
            print("   Best game    : N/A (no wins yet)")

        # 6. Ask to play again
        choice = input("\nDo you want to play again? (y/n): ").strip().lower()

        if choice == "n":
            print("\nThanks for playing! Goodbye 👋")
            sys.exit()
        elif choice != "y":
            print("Unrecognized input, exiting the game. Bye!")
            sys.exit()
        # if 'y', loop continues and a new round starts


if __name__ == '__main__':
    main()
