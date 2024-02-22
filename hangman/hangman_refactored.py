import hanged_man
import words
import requests
import threading


def get_word_definition(word, callback):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
        else:
            definition = "Definition not found."
    except requests.RequestException:
        definition = "Error fetching definition."
    callback(definition)


def display_definition(definition):
    global word_definition
    word_definition = definition


def print_characters(word, guesses):
    print(" ".join([letter if letter in guesses else "_" for letter in word]))


def check_input():
    while True:
        guess = input("Guess a letter: ")
        if len(guess) != 1:
            print("Please guess a single letter.")
        elif not guess.isalpha():
            print("Please guess a letter.")
        else:
            return guess.lower()


word_definition = None
word = words.get_word()
count = 0
guesses = set()

# Start fetching the definition in a background thread
definition_thread = threading.Thread(target=get_word_definition, args=(word, display_definition))
definition_thread.start()

while True:
    hanged_man.draw_hanged_man(count)
    print_characters(word, guesses)
    guess = check_input()

    if guess in word:
        guesses.add(guess)
        if all(letter in guesses for letter in word):
            print("\nYou won!")
            definition_thread.join()
            print(f"The word was: {word}")
            print(f"Definition: {word_definition}")
            break
        print("\n" + f"{guess} is Correct!")
    else:
        if guess not in guesses:
            count += 1
            print("\n" + f"{guess} is not in the word. Try again. Wrong!")
        guesses.add(guess)
        if count >= 6:
            hanged_man.draw_hanged_man(count)
            print("You have been hanged!")
            definition_thread.join()
            print(f"The word was: {word}")
            print(f"Definition: {word_definition}")
            break

    print(f"Guesses: {guesses}")
