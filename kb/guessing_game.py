import random

def number_guessing_game():
    number = random.randint(1, 100)
    attempts = 5
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    while attempts > 0:
        try:
            guess = int(input("Take a guess: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if guess < number:
            print("Too low!")
        elif guess > number:
            print("Too high!")
        else:
            print(f"Congratulations! You guessed the number {number} in {5 - attempts + 1} attempts.")
            break
        attempts -= 1
        print(f"You have {attempts} attempts remaining.")
    if attempts == 0:
        print(f"Sorry, you ran out of attempts. The number was {number}.")

if __name__ == "__main__":
    number_guessing_game()