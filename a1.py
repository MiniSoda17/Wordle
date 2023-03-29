"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001/CSSE7030
"""

from string import ascii_lowercase
from typing import Optional

from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)

__author__ = "<Isaac Arli>, <s4720429>"
__email__ = "<i.arli@uqconnect.edu.au>"

#5.1 returns true if guess matches answer exactly
def has_won(guess: str, answer: str) -> bool:
    if guess == answer:
        return True
    else:
        return False

#5.2 Returns true if the number of guess that have occurred are equal or more
def has_lost(guess_number: int) -> bool:
    x = guess_number
    if x >= 6:
        return True
    else:
        return False

#5.3 Returns a copy of words with word removed
def remove_word(words: tuple[str,...], word: str) -> tuple[str,...]:

    #changes words into list because it is immutable as a tuple, then changes it back to a tuple after a change is made
    words = list(words)
    words.remove(word)
    words = tuple(words)
    return words

#5.4 reprompting until either a valid guess is entered or a selection for help
def prompt_user(guess_number: int, words: tuple[str]) -> str:
    
    while True:
        attempt = str(input("Enter guess " + str(guess_number) + ": "))  
        if attempt.lower() == "q":
            return attempt.lower()
        elif attempt.lower() == "h":
            return attempt.lower()
        elif attempt.lower() == "k":
            return attempt.lower()
        elif len(attempt) != 6:
            print ("Invalid! Guess must be of length 6")
        elif attempt not in words:
            print ("Invalid! Unknown word")
        else:
            return attempt    

#5.5 returns a modified representation of guess, in which each letter is replace
def process_guess(guess: str, answer: str) -> str:
    coloredList = [INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT, INCORRECT]

    #if a letter from guess is equal to a letter from answer, that letter will be removed from answer.
    new = answer
    for i in range(6):
        if answer[i] == guess[i]:
            coloredList[i] = CORRECT
            new = new.replace(guess[i], '')
    for i in range(6):
        if guess[i] in new:
            coloredList[i] = MISPLACED
            new = new.replace(guess[i], '')        
    return "".join(coloredList)

#5.6 Returns a copy of history updated to include the latest guess and its process form.
def update_history(history: tuple[tuple[str, str], ...], guess:str, answer: str) -> tuple[tuple[str, str],...]:

    return history + ((guess, process_guess(guess, answer)),)

#5.7 Prints the guess history in a user-friendly way.
def print_history(history: tuple[tuple[str, str],...]) -> None:

    x = 1
    for i in history:
        print ("---------------")
        print ("Guess " + str(x) +":  " + " ".join(i[0]))
        print ("         " + i[1])       
        x += 1
    print ("---------------\n")

#5.8 prints an entire keyboard showing which letters have been used and their relationship to the answer
def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    print ("\nKeyboard information")
    print ("------------")

    #goes through each letter of the alphabeter to check if it corresponds to a letter in a word from "history"
    count = 0
    for letter in ascii_lowercase:
        temp = UNSEEN
        for i in history:
            if letter in i[0]:

                #if the letter is in one of the words from history, it will assign the letter to either CORRECT or MISPLACED
                for index in range(6):
                    if i[0][index] == letter:
                        assign = index
                        if i[1][assign] == CORRECT:
                            temp = CORRECT
                        elif i[1][assign] == MISPLACED and temp != CORRECT:
                            temp = MISPLACED
                        elif temp == UNSEEN:
                            temp = i[1][assign]
                
        #This block of code organises the keyboard so that it creates a new line after every 2 letters.       
        if count % 2 != 0:
            print(letter + ": " + temp)
        else:
            print(letter + ": " + temp, end='\t')
        count += 1
    print("")

#5.9 Prints the entire statistics of games won and their total amount of moves.                    
def print_stats(stats: tuple[int, ...]) -> None:

    #creates the list of games won and uses the stats variable to see how many games have been won
    print("\nGames won in:")
    for i in range(6):
        print(str(i+1) + " moves: " + str(stats[i]))      
    print("Games lost: " + str(stats[6]))

#runs the entire game with all the previous function             
def main():
    
    vocabulary = load_words(VOCAB_FILE)
    list_of_answers = load_words(ANSWERS_FILE)
    answer = choose_word(list_of_answers)
    history = ()
    statistics = [0, 0, 0, 0, 0, 0, 0]
    x = 1
  
    while True:
        guess = prompt_user(x, vocabulary)
        if guess == "h":
            print("Ah, you need help? Unfortunate.")
            continue
        elif guess == "k":
            print_keyboard(history)
            continue
        elif guess == "q":
            break

        #prints an updated history
        processed = process_guess(guess, answer)
        history = update_history(history, guess, answer)
        print_history(history)

        #once has_won or has_lost is equal to true, it will add the win to the specific index of statistics and add 1 to it
        if has_won(guess, answer) == True:         
            print("Correct! You won in " + str(x) + " guesses!")
            statistics[x-1] += 1           
        elif has_lost(x) == True:            
            print("You lose! The answer was: " + answer)
            statistics[6] += 1

        if has_lost(x) == True or has_won(guess, answer) == True:
            print_stats(tuple(statistics))
            play_again = input("Would you like to play again (y/n)? ")
            if play_again.lower() == "y":
                x = 1
                history = ()
                list_of_answers = remove_word(list_of_answers, answer)
                answer = choose_word(list_of_answers)
                continue          
            else:
                break
        x += 1  


if __name__ == "__main__":
    main()
