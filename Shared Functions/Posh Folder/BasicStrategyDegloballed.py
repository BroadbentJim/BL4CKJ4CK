import random
import time
import timeit

global hardtotal
hardtotal = False
Deck=[]
strategy=[]


def new_deck():
    """
    New Deck Function:
    Parameters: NONE
    This function creates a Deck array and deals to it
    returns:
    Deck: The deck array that will hold the cards.

"""
    Deck = []  # Create deck array
    one_suit = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]  # Defines One suit
    q = 0
    while q < 24:  # 6 decks of 4 suits
        for i in one_suit:  # For each card in a suit
            Deck.append(i)  # Add that card to the deck
        q += 1
    random.shuffle(Deck)  # Randomly shuffle the deck
    return Deck


def initial_hit(hand):
    """
    Hit function used for dealing

    Parameter(s): hand
    hand: the hand that is being hit
    This function is important as it doesn't update the strategy array
    """
    card = Deck.pop(0)  # Set card to be first card in deck and remove it
    hand.append(card)  # Add the card to the hand array


def hit(hand):
    """
    Hit function used typically

    Parameter(s): hand
    hand: the hand that is being hit
    This function is significant as it updates the strategy array providing a useful statistic to my client
    """
    card = Deck.pop(0)  # Set card to be first card in deck and remove it
    hand.append(card)  # Add the card to the hand array
    strategy.append("Hit")  # Update the strategy array to reflect this move


def split(hand, hand2):
    """
    Split Function
    Parameter(s):
    hand: The player's first hand typically Phand
    hand2: The player's 2nd hand typically Phand2
    :param hand2:
    :return:
    """
    card = hand.pop(0)  # Remove a card from the first hand and save it as a variable
    hand2.append(card)  # Add that card to the player's 2nd hand
    initial_hit(hand)  # Silently hit both player hands
    initial_hit(hand2)
    strategy.append("Split")


def double(hand):
    """
    This function is not used in this strategy
 """
    hit(hand)
    # wager = 2 * wager


def stay():
    """
    Stay Function:
    This function will update the strategy array accordingly
    :return:
    """
    strategy.append("Stay")
    return


def deal(Phand, Dhand):
    """
    Deal function
    Parameter(s): Phand, Dhand
    NOTE TO SELF Change parameter name
    Phand: The player's hand
    Dhand: The dealer's hand
    :return:
    """
    initial_hit(Phand)
    initial_hit(Dhand)
    initial_hit(Phand)
    initial_hit(Dhand)

def basic_strategy(Pand, Pand2, Dand): #Basic Strategy
    """
    Basic Player Strategy
    This function takes 3 arguments.
    Pand: Current player hand
    Pand2: Alternate player hand
    Dand: Dealer hand

    This function will apply certain logic to the players decision
"""
    global hardtotal
    score(Pand)
    if split_style(Pand, Pand2, Dand) == True:
        split(Pand, Pand2)
    elif hardtotal == False:
        if score(Pand) < 18:
            hit(Pand)
        elif score(Pand) == 18 and score([Dand[0]]) > 8:
            hit(Pand)
        else:
            stay()
    elif hardtotal == True:
        if score(Pand) < 12:
            hit(Pand)
        elif score(Pand) < 17 and score([Dand[0]]) > 6:
            hit(Pand)
        elif score(Pand) == 12 and score([Dand[0]]) < 4:
            hit(Pand)
        else:
            stay()

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

def split_style(Pand, Pand2, Dand):
    """
    This function decides whether the player should split or not
    It takes exactly 3 arguments
    Pand which should be the current player hand
    Pand2 the other player hand
    Dand which is the dealer hand

    It will then follow some predefined rules and choose whether to split

    The function will return a Boolean on whether the player should split


"""
    if Pand[0] == Pand[1] and len(Pand2) == 0:
        if Pand[0] == 'A':
            return True
        elif Pand[0] == 8:
            return True
        elif (Pand[0] == 2 or Pand[0] == 3 or Pand[0] == 7) and score([Dand[0]]) < 8:
            return True
        elif Pand[0] == 6 and score([Dand[0]]) < 7:
            return True
        elif Pand[0] == 9 and score([Dand[0]]) < 10 and score([Dand[0]]) != 7:
            return True
        elif Pand[0] == 4 and score([Dand[0]]) < 7 and score([Dand[0]]) > 4:
            return True
    else:
        return False
def dealer(hand):
    """
    Dealer function:
    Parameter: hand
    hand: The dealer's hand for which the logic must be followed
    """
    while score(hand) < 17: #While the dealer's score is less than 17
        initial_hit(hand) #Invisibly hit the dealer's hand

def compare(hand1, hand2): #True means Hand1 has won, False means hand2 has won.
    """
    Compare Function:
    This function takes 2 arguments.
    hand1 which is the player hand to be compared
    hand which is the dealer hand to be compared

    This function then follows some set logic to work out what the player score
    should be increased.

    The increase to player score is returned from this function.

"""


    if score(hand1) == 21 and len(hand1) == 2: #If Player Blackjack
        if score(hand2) == 21 and len(hand2) == 2:#If Dealer Blackjack
            return 1 #Player wins 1
        else:
            return 1.5#Player wins 3:2

    if score(hand1) <= 21 and score(hand2) > 21: #If player not bust but dealer bust
        return 1#Player wins 1
    elif score(hand1) > 21 and score(hand2) <= 21:#If player bust but dealer not bust
        return 0#Player loses
    elif score(hand1) > score(hand2) and score(hand1)<= 21:
        #If player is greater than dealer and not bust
        return 1
    else:

        return 0

def game(loop):
    """
    Main Game Loop:
    This function takes 1 arguments.
    loop: int which controls how many simulations to do

    This function controls all of the subfunctions that make up a game

    This function returns a dictionary which should be consistent across all game types.
    This allows for GUI to then show that data.
    """
    global Deck
    #this global variable holds the deck
    #Create and set to zero score variables
    player_wins, dealer_wins, split_player_wins, split_dealer_wins = (0,)*4
    #Create an empty Deck variable
    Deck = new_deck()
    #Record start_time
    start_time = time.time()

    for _ in range(loop):
        #Loop for required number
        #Create empty arrays to hold the hands
        Phand = []
        Phand2 = []
        Dhand = []
        #Deal to both hands
        deal(Phand, Dhand)
        #Play out the player hands
        basic_strategy(Phand, Phand2, Dhand)
        if len(Phand2) > 0:
            basic_strategy(Phand2, Phand, Dhand)
        #Play out the dealer strategy
        dealer(Dhand)
        #Begin comparison of hands and score
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
            Deck = new_deck()
    #Calculate time
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    #Calculate values about the game
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    total_games = total_dealer_wins + total_player_wins
    net_gain_abs = total_player_wins - total_dealer_wins #abs is short for absolute

    try:
        net_gain_per = net_gain_abs/total_dealer_wins * 100
    except:
        net_gain_per = 100
    #calculate and round the winrate
    win_rate = round(total_player_wins / total_games * 100, 2)
    #Calculate how many times the player did each move
    hits = strategy.count("Hit")
    stays = strategy.count("Stay")
    splits = strategy.count("Split")
    doubles = strategy.count("Doubles")


    #Create a dictionary holding valuable results from the simulation
    dictionary = {'Total Games': total_games,
    'Total player wins': total_player_wins,
    'Total dealer wins': total_dealer_wins,
    'Percentage netgain': net_gain_per,
    'Percentage winrate': win_rate,
    "Strategy" : strategy,
    "Time Taken": elapsed_time}
    return dictionary


#Debugging code

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

if __name__ == "__main__":
    # sims = int(input("Please input the number of times you would like to loop "))
    # dictionary = game(sims)
    # print("Time taken: ", dictionary["Time Taken"])
    # print("Netgain: ", round(dictionary["Percentage netgain"], 2), "%")
    # print("Winrate: ", dictionary["Percentage winrate"], "%")
    # print("Times hit: ", dictionary["Strategy"].count("Hit"))
    # print("Total games", dictionary["Total Games"])
    wrapped = wrapper(game, 10000)
    print(timeit.timeit(wrapped, number=100))
