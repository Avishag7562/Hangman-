import sys
import os

# import random

# print hangman once:
logo = r'''   
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/'''

HANGMAN_PHOTOS = {
    "fail0": "x-------x",
    "fail1": "x-------x\n|\n|\n|\n|\n|",
    "fail2": "x-------x\n|       |\n|       0\n|\n|\n|",
    "fail3": "x-------x\n|       |\n|       0\n|       |\n|\n|",
    "fail4": "x-------x\n|       |\n|       0\n|      /|\\ \n|\n|",
    "fail5": "x-------x\n|       |\n|       0\n|      /|\\ \n|      /\\\n|",
    "fail6": "x-------x\n|       |\n|       0\n|      /|\\ \n|      / \\ \n|"}


# Validity check for received character
def validity(guess_letter):
    if len(guess_letter) > 1:
        print('E1 - The length of the character is more than 1\n')
        return False
    elif guess_letter.isascii() and not guess_letter.isalpha():
        print('E2 - The character is not an English letter\n')
        return False
    elif len(guess_letter) > 1 and guess_letter.isascii() and not guess_letter.isalpha():
        print('E3\n')
        return False
    return True


# הפונקציה בודקת שהמשתמש מזין תו אחד באנגלית שטרם נוחש במשחק ושהוא תקין לשימוש
def check_valid_input(letter_guessed, old_letters_guessed):
    if len(letter_guessed) != 1 or not letter_guessed.isalpha() or letter_guessed in old_letters_guessed:
        return False
    return True


# הפונקציה שימושית לעדכון רשימת האותיות שנוחשו במשחק.
# הפונקציה קוראת תחילה לפונקציה check_valid_input
# כדי להבטיח את תקינות הקלט של המשתמש.
# אם הקלט תקין, היא מוסיפה את האות לרשימת  התווים שנוחשו
# המחרוזת מודפסת כדי להראות למשתמש את הרשימה הממוינת של האותיות שנוחשו בעבר.
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print('X')
        old_letters_guessed.sort()
        str_sorted = " -> ".join(old_letters_guessed)
        print(str_sorted)
        return False


# הפונקציה show_hidden_word
# משמשת להצגת המילה המוסתרת
# הפונקציה עוברת על כל אות במילה המוסתרת ובודקת אם היא כבר נוחשה ונמצאת ברשימת
# אם האות כבר נוחשה, היא מוסיפה את האות למחרוזת החדשה new_str.
# אחרת, היא מוסיפה מקום רווח וסימן תחתון למחרוזת כדי לסמן את האות המוסתרת.
def show_hidden_word(secret_word, old_letters_guessed):
    new_str = ''
    for letter in secret_word:
        if letter in old_letters_guessed:
            new_str += letter + ''
        else:
            new_str += ' _ '
    return new_str


# הפונקציה משמשת לבדיקה אם המשתמש ניחש את כל האותיות הנכונות במילה המוסתרת
def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[f'fail{num_of_tries}'])


def find_different_words(path, index):
    with open(path, 'r') as file:
        text = file.read()

    words = text.split()
    num_words = len(words)

    if index >= num_words:
        index = index % num_words

    secret_word = words[index - 1]
    # Remove duplicates
    unique_words = set(words)

    count_different_words = len(unique_words)
    return (count_different_words, secret_word)


def main():
    play_again = True
    old_letters_guess = []
    fail_try_count = 1
    character_choose = ''
    num_guesses = 7

    print(logo)

    # Guessing_attempts = random.randint(5, 10)
    # num_guesses = Guessing_attempts
    # print(f'You have {Guessing_attempts} guesses\n')

    file_path = input('Please enter WordsList path to WordsList word file\n')
    while not os.path.exists(file_path) or not os.path.isfile(file_path):
        print("Invalid file path. Please try again.")
        file_path = input()

    location = input('Great! Enter WordsList location for WordsList word in the file\n')
    while not location.isdigit():
        print("Invalid location. Please try again.")
        location = input()

    num_different_words, secret_word = find_different_words(file_path, int(location))

    print("Let's start!\n")

    print(HANGMAN_PHOTOS['fail0'])

    print('_ ' * len(secret_word))

    print(f'You have 7 guesses')

    while num_guesses > 0 and fail_try_count < 8 and play_again:
    # while HANGMAN_PHOTOS['fail6'] and play_again:

        character_choose = input(f'Guess WordsList letter: ').lower()
        validity(character_choose)

        result_input = try_update_letter_guessed(character_choose, old_letters_guess)

        if result_input and character_choose not in secret_word:
            print(":(")
            print_hangman(fail_try_count)
            print(show_hidden_word(secret_word, old_letters_guess))
            num_guesses -= 1
            fail_try_count += 1
            print(f'You have {num_guesses} guesses left')

        else:
            hidden_word = show_hidden_word(secret_word, old_letters_guess)
            print(hidden_word)
            num_guesses -= 1
            print(f'You have {num_guesses} guesses left')

        if check_win(secret_word, old_letters_guess):
            print('Congratulation You Win!!! :)')
            input()
            break

    if not check_win(secret_word, old_letters_guess):
        print('You Lose!')

    play_again_input = input("Do you want to play again? (yes/no): ")
    while play_again_input.lower() not in ['yes', 'no']:
        print("Invalid input. Please enter 'yes' or 'no'.")
        play_again_input = input("Do you want to play again? (yes/no): ")

    if play_again_input.lower() == 'no':
        play_again = False
    else:
        main()


if __name__ == '__main__':
    main()
