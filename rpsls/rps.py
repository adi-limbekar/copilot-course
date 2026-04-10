# TODO: Develop a console-based Rock Paper Scissors game in Python
# Game should be modular, allowing for easy updates or rule changes
# Implement game rules:
# - Scissors cuts paper
# - Paper covers rock 
# - Rock crushes scissors
# Include user input for selecting options and display game results

import random

def get_user_choice():
    choices = ['rock', 'paper', 'scissors']
    choice_map = {
        '1': 'rock',
        '2': 'paper',
        '3': 'scissors'
    }
    user_input = input("Enter your choice (1-rock, 2-paper, 3-scissors): ").lower()
    while user_input not in choices and user_input not in choice_map:
        print("Invalid choice. Please try again.")
        user_input = input("Enter your choice (1-rock, 2-paper, 3-scissors): ").lower()
    return choice_map.get(user_input, user_input)

def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    
    wins = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    if computer_choice == wins[user_choice]:
        return "You win!"
    else:
        return "Computer wins!"
    
def play_game():
    print("Welcome to Rock Paper Scissors!")
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    
    print(f"You chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")
    
    result = determine_winner(user_choice, computer_choice)
    print(result)

if __name__ == "__main__":
    play_game() 
    