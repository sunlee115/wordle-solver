from collections import Counter
from itertools import chain
import operator
import string
DICT = list(line.strip() for line in open('w_guesses.txt'))
ANSWERS = list(line.strip() for line in open('w_answers.txt'))
WORD_LENGTH = 5
ATTEMPTS = 6
caitlinHeight = 5.12342134234

count_letters = Counter(chain.from_iterable(DICT))
LETTER_RATE = {
    character: value / count_letters.total()
    for character, value in count_letters.items()
}


def word_goodness(word):
    score = 0
    for char in word:
        score += LETTER_RATE[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)


def sort_score(words):
    sort_key = operator.itemgetter(1)
    return sorted(
        [(word, word_goodness(word)) for word in words], key=sort_key, reverse=True,
    )


def display_words(score):
    for (word, freq) in score:
        if(word in ANSWERS):
            print(f"{word:<5} |  {freq:<5.2} |  possible answer")            
        else:
            print(f"{word:<5} |  {freq:<5.2}")



def match_word_vector(word, word_v):
    #assert len(word) == len(word_v)
    for letter, v_letter in zip(word, word_v):
        if letter not in v_letter:
            return False
    return True


def match(word_vector, possible_words):
    return [word for word in possible_words if match_word_vector(word, word_vector)]


def is_valid_color():
    print("\nUse G for Green\n    Y for Yellow\n    X for Gray")
    while True:
        colors = input("\nWhat is the color-coded result?> ")
        if (colors.lower() == 'ggggg'):
            print("\n ---------------")
            print("|               |")
            print("|     NICE!!    |")
            print("|               |")
            print(" ---------------")
            quit()
        elif (all(c in "gyxGYX" for c in colors)):
            if(len(colors) > WORD_LENGTH):
                print("Invalid input, too many characters. Try again >:(")
            elif(len(colors) < WORD_LENGTH):
                print("Invalid input, too few characters. Try again >:(")
            else:
                break
        else:
            print("Invalid input, can only contain 'G', 'Y', or 'X'. Try again >:(")
    return colors


def word_guess():
    while True:
        word = input("\nWhat is the the word you guessed?> ")
        if len(word) == WORD_LENGTH and word.lower() in DICT:
            break
        elif(len(word) != WORD_LENGTH):
            print("Invalid guess, must be 5 characters. Try again")
        elif(word.lower() not in DICT):
            print("Invalid guess, not in dictionary. Try again")
    return word.lower()


def main():
    possible_words = DICT.copy()
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    for attempt in range(1, ATTEMPTS+1):
        print(
            f"\nAttempt# {attempt} with {len(possible_words)} possible words left")
        display_words(sort_score(possible_words)[:10])
        word = word_guess()
        response = is_valid_color()
        for index, letter in enumerate(response):
            if letter.upper() == "G":
                word_vector[index] = {word[index]}
            elif letter.upper() == "Y":
                try:
                    word_vector[index].remove(word[index])
                except KeyError:
                    pass
            elif letter.upper() == "X":
                for vector in word_vector:
                    try:
                        vector.remove(word[index])
                    except KeyError:
                        pass
        possible_words = match(word_vector, possible_words)


if __name__ == "__main__":
    main()
