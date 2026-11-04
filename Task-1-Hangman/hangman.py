import csv
import random
import os

WORDS = []

file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Words.csv"
)

with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        WORDS.append(row["word"].strip().lower())
HANGMAN_STAGES = [
    r"""
     _______
    |/      |
    |
    |
    |
    |
    |___
""",
    r"""
     _______
    |/      |
    |      (_)
    |
    |
    |
    |___
""",
    r"""
     _______
    |/      |
    |      (_)
    |       |
    |       |
    |
    |___
""",
    r"""
     _______
    |/      |
    |      (_)
    |      \|
    |       |
    |
    |___
""",
    r"""
     _______
    |/      |
    |      (_)
    |      \|/
    |       |
    |
    |___
""",
    r"""
     _______
    |/      |
    |      (_)
    |      \|/
    |       |
    |      /
    |___
""",
    r"""
     _______
    |/      |
    |      (_)
    |      \|/
    |       |
    |      / \\
    |___
"""
]
def display_game(secret_word, guessed_letters, wrong_guesses):
    print(HANGMAN_STAGES[wrong_guesses])
    masked_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )
    print("Word:", masked_word)
    print("Guessed letters:", " ".join(sorted(guessed_letters)) or "None")
    print(f"Incorrect guesses: {wrong_guesses}/6")
def play_game():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6
    print("=" * 42)
    print("       HANGMAN WORD GUESSING GAME")
    print("=" * 42)
    print("Guess the hidden word one letter at a time.")
    print(f"You have {max_attempts} incorrect guesses available.")
    while wrong_guesses < max_attempts:
        display_game(secret_word, guessed_letters, wrong_guesses)
        if all(letter in guessed_letters for letter in secret_word):
            print("\n" + "=" * 42)
            print("CONGRATULATIONS! YOU WIN!")
            print(f"You guessed the word: {secret_word.upper()}")
            print("=" * 42)
            return
        guess = input("\nEnter a letter (or type 'quit' to exit): ").strip().lower()
        if guess == "quit":
            print(f"\nGame ended. The word was: {secret_word.upper()}")
            return
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single alphabet letter.")
            continue
        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue
        guessed_letters.add(guess)
        if guess in secret_word:
            print(f"Good guess! '{guess}' is in the word.")
        else:
            wrong_guesses += 1
            print(f"Sorry! '{guess}' is not in the word.")
    display_game(secret_word, guessed_letters, wrong_guesses)
    print("\n" + "=" * 42)
    print("GAME OVER! YOU LOST.")
    print(f"The correct word was: {secret_word.upper()}")
    print("=" * 42)
def main():
    while True:
        play_game()
        again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("\nThanks for playing Hangman. Goodbye!")
            break
if __name__ == "__main__":
    main()
