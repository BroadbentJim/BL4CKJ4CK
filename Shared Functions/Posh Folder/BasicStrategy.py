import random
import time, timeit
import numpy as np


player_wins = 0
dealer_wins = 0
split_player_wins = 0
split_dealer_wins = 0
global hardtotal
hardtotal = False


Deck=[]
Phand=[]
Phand2=[]
Dhand=[]
strategy=[]

def new_deck():

    one_suit=[2,3,4,5,6,7,8,9,10,"J", "Q", "K", "A"] #One suit
    q = 0
    while q < 24: #6 decks of 4 suits
        for i in one_suit:
            Deck.append(i)
        q +=1
    random.shuffle(Deck) #Randomly shuffle the hand

def initial_hit(hand):
    card = Deck.pop(0) #Set card to be first card in deck and remove it
    hand.append(card)

def hit(hand):
    card = Deck.pop(0)
    hand.append(card)
    strategy.append("Hit")

def split(hand):
    card = hand.pop(0)
    Phand2.append(card)
    hit(Phand)
    hit(Phand2)

def double(hand):
    hit(hand)
    #wager = 2 * wager

def stay():
    strategy.append("Stay")
    return

def deal():
    initial_hit(Phand)
    initial_hit(Dhand)
    initial_hit(Phand)
    initial_hit(Dhand)

def bust(hand):
    if score(hand) > 21:
        return ""
    else:
        return "not "

def score(hand):
    """
    Score Function
    This function changes the global hardtotal
    hardtotal is changed here as this function evaluates whether or not they are hardtotals
    Parameters: hand
    hand: this is the hand ARRAY for which the score is being evaluated.
    returns value of the hand
    """
    global hardtotal
    #Create empty holder variables and reset hardtotal
    total = 0
    Aces = 0
    hardtotal = True
    for cards in hand:#iterate through every card in the hand array
        if cards == "J" or cards == "Q" or cards == "K":#if the card is a Jack, Queen, Kind
            total += 10#The score of the hand is increased by 10
        elif cards == "A":#If the card is an Ace
            total += 11
            Aces += 1
            hardtotal = False#Hardtotal is changed to reflect that the hand contains an Ace
        else:
            total += cards #Otherwise just add the numerical value of the card to the total

    while Aces > 0 and total > 21: #If the total would cause the player to bust and there are ace(s)
        total -= 10#Take the Ace to be worth 1
        Aces -= 1#Decrement the number of aces
    if Aces == 0:#If no aces or all aces taken to be 1
        hardtotal = True#The hand is a hardtotal

    return total


def basic_strategy(Pand, Dand): #Basic Strategy
    """
        Basic Player Strategy
        This function takes 3 arguments.
        Pand: Current player hand
        Pand2: Alternate player hand
        Dand: Dealer hand

        This function will apply certain logic to the players decision
    """
    global hardtotal
    if split_style(Pand, Dand) == True:
        #If split_style says to split, split
        split(Pand)
    elif hardtotal == False:# NOT Hardtotal logic
        if score(Pand) < 18:#if score of hand is less than 18
            hit(Pand)
        elif score(Pand) == 18 and score([Dand[0]]) > 8:
            #if score of hand is 18 and score of dealer's card > 8
            hit(Pand)
        else:
            stay()
    elif hardtotal == True:#hardtotal logic
        if score(Pand) < 12:
            hit(Pand)
        elif score(Pand) < 17 and score([Dand[0]]) > 6:
            hit(Pand)
        elif score(Pand) == 12 and score([Dand[0]]) < 4:
            hit(Pand)
        else:
            stay()

def split_style(Pand, Dand):
    """
    This function decides whether the player should split or not
    It takes exactly 3 arguments
    Pand which should be the current player hand
    Pand2 the other player hand
    Dand which is the dealer hand

    It will then follow some predefined rules and choose whether to split

    The function will return a Boolean on whether the player should split
    True means split. False means don't split


"""
    if Pand[0] == Pand[1] and len(Phand2) == 0:#If player hasn't split and the two cards of the hand are same
        if Pand[0] == 'A':#If the card is an Ace
            return True
        elif Pand[0] == 8:
            return True
        elif (Pand[0] == 2 or Pand[0] == 3 or Pand[0] == 7) and score([Dand[0]]) < 8:
            #If the card is 2/3/7 and the score of the dealer's card is less than 8
            return True
        elif Pand[0] == 6 and score([Dand[0]]) < 7:
            #If card is 6 and dealer's card is less than 7
            return True
        elif Pand[0] == 9 and score([Dand[0]]) < 10 and score([Dand[0]]) != 7:
            #If card is 9 and dealer's card is less than 10 but not 7
            return True
        elif Phand[0] == 4 and score([Dand[0]]) < 7 and score([Dand[0]]) > 4:
            #if score is 4 and dealer's card is between 4 and 7
            return True
    else:
        return False



def dealer(wanted):
    while score(Dhand) < wanted:
        hit(Dhand)

def compare(hand1, hand2): #True means Hand1 has won, False means hand2 has won.

    if score(hand1) == 21 and len(hand1) == 2:
        if score(hand2) == 21 and len(hand2) == 2:
            return 1
        else:
            return 1.5

    if score(hand1) <= 21 and score(hand2) > 21:
        return 1
    elif score(hand1) > 21 and score(hand2) <= 21:
        return 0
    elif score(hand1) > score(hand2) and score(hand1)<= 21:

        return 1
    else:
        return 0

def game(loop):
    global Deck, Phand, Phand2, Dhand
    player_wins = dealer_wins = split_player_wins = split_dealer_wins = 0
    start_time = time.time()
    new_deck()

    for _ in range(loop):
        Phand = []
        Dhand = []
        Phand2 = []
        deal()
        basic_strategy(Phand, Dhand)
        if len(Phand2) > 0:
            basic_strategy(Phand2, Dhand)
        dealer(17)
        if compare(Phand, Dhand) == 1:
            player_wins += 1
        elif compare(Phand, Dhand) == 1.5:
            player_wins += 1.5
        else:
            dealer_wins += 1
        if len(Phand2) > 0:
            if compare(Phand2, Dhand) == 1:
                split_player_wins += 1
            elif compare(Phand2, Dhand) == 1.5:
                split_player_wins += 1.5
            else:
                split_dealer_wins += 1
        if len(Deck) <= 52:
            new_deck()

    finish_time = time.time()
    elapsed_time = finish_time - start_time
    split_games = split_player_wins + split_dealer_wins
    total_games = loop + split_games
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    net_gain_abs = total_player_wins - total_dealer_wins #abs is short for absolute
    net_gain_per = net_gain_abs / total_dealer_wins
    win_rate = round(total_player_wins / total_games * 100, 2)
    #Calculate how many times the player did each move
    hits = strategy.count("Hit")
    stays = strategy.count("Stay")
    splits = strategy.count("Split")
    doubles = strategy.count("Doubles")

    dictionary = {'Total Games': total_games,
                  'Total player wins': total_player_wins,
                  'Total dealer wins': total_dealer_wins,
                  'Percentage netgain': net_gain_per,
                  'Percentage winrate': win_rate,
                  "Strategy": strategy,
                  "Time": elapsed_time, }
    return dictionary

def simulations(loop):
    gains = []
    start_time = time.time()
    for i in range(99):
        gains.append(game(loop)["Percentage netgain"])
    dictionary = game(loop)
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    dictionary["Time"] = elapsed_time
    gains.append(dictionary["Percentage netgain"])

    dictionary["Gainz"] = gains
    #print(dictionary)
    return dictionary

#Debugging code
def wrapper(func, *args, **kwargs):
    #Used for timeit with functions with arguments
    def wrapped():#Create a subfunction
        return func(*args, **kwargs)
    return wrapped#Return that subfunction

if __name__ == "__main__":
    # sims = int(input("Please input the number of times you would like to loop "))
    # dictionary = game(sims)
    # print("Time taken: ", dictionary["Time Taken"])
    # print("Netgain: ", round(dictionary["Percentage netgain"], 2), "%")
    # print("Winrate: ", dictionary["Percentage winrate"], "%")
    # print("Times hit: ", dictionary["Strategy"].count("Hit"))
    # print("Total games", dictionary["Total Games"])
    wrapped = wrapper(game, 10000) #Create a function that will be tested
    print(timeit.timeit(wrapped, number=100))#Go through the function wrapped 100 times and print the total time
