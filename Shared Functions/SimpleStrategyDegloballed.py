import random
import time


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
    Deck = [] #Create deck array
    one_suit=[2,3,4,5,6,7,8,9,10,"J", "Q", "K", "A"] #Defines One suit
    q = 0
    while q < 24: #6 decks of 4 suits
        for i in one_suit:#For each card in a suit
            Deck.append(i)#Add that card to the deck
        q +=1
    random.shuffle(Deck) #Randomly shuffle the deck
    return Deck

def initial_hit(hand):
    """
    Hit function used for dealing

    Parameter(s): hand
    hand: the hand that is being hit
    This function is important as it doesn't update the strategy array
    """
    card = Deck.pop(0) #Set card to be first card in deck and remove it
    hand.append(card) #Add the card to the hand array

def hit(hand):
    """
    Hit function used typically

    Parameter(s): hand
    hand: the hand that is being hit
    This function is significant as it updates the strategy array providing a useful statistic to my client
    :param hand:
    :return:
    """
    card = Deck.pop(0) #Set card to be first card in deck and remove it
    hand.append(card) #Add the card to the hand array
    strategy.append("Hit") #Update the strategy array to reflect this move

def split(hand, hand2):
    """
    Split Function
    Parameter(s):
    hand: The player's first hand typically Phand
    hand2: The player's 2nd hand typically Phand2
    :param hand2:
    :return:
    """
    card = hand.pop(0) #Remove a card from the first hand and save it as a variable
    hand2.append(card) #Add that card to the player's 2nd hand
    initial_hit(hand) #Silently hit both player hands
    initial_hit(hand2)

def double(hand):
    """
    This function is not used in this strategy
 """
    hit(hand)
    #wager = 2 * wager

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

def simple_strategy(want, Phand, Phand2):
    """
    Simple Strategy algorithm
    Parameters: want, Phand, Phand2
    NOTE TO SELF CHANGE PARAMETERS NAME
    want: The value the player wants to hit INT
    Phand: The player's first hand ARRAY
    Phand: The player's 2nd hand ARRAY
    """
    if Phand[0] == Phand[1]: #If splittable, split
        split(Phand, Phand2)
    while score(Phand) <= want: #Whilst score is less than wanted score
        hit(Phand) #Hit
    if len(Phand2) > 0:#If have split
        while score(Phand2) <= want:#Apply same logic to 2nd hand
            hit(Phand2)

def dealer(hand):
    """
    Dealer function:
    Parameter: hand
    hand: The dealer's hand for which the logic must be followed
    """
    while score(hand) < 17: #While the dealer's score is less than 17
        initial_hit(hand) #Invisibly hit the dealer's hand

def compare(hand1, hand2):
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

def game(loop, want):
    """
    Main Game Function:
    Parameter(s):
    loop: Number of simulations to do
    want: Value player wants to hit too
    returns:
    dictionary: A dictionary containing all of the relevant results.
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
        #Empty relevant arrays
        Phand = []
        Dhand = []
        Phand2 = []
        #Deal to players
        deal()
        #Call player strategy
        simple_strategy(want)
        #Compare results
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
        #If the length of the deck goes below 1 deck, redeal
        if len(Deck) <= 52:
            new_deck()

    #Calculate time
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    #Calculate values about the game
    split_games = split_player_wins + split_dealer_wins
    total_games = loop + split_games
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    net_gain_abs = total_player_wins - total_dealer_wins #abs is short for absolute

    try:
        net_gain_per = net_gain_abs/total_dealer_wins
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
    "Time": elapsed_time}
    return dictionary


#Debugging code

if __name__ == "__main__":
    sims = int(input("Please input the number of times you would like to loop "))
    wanted = int(input("Please input the number of you'd like to hit too "))
    dictionary = game(sims, wanted)
    print("Time taken: ", dictionary["Time Taken"])
    print("Netgain: ", dictionary["Percentage netgain"])
    print("Winrate: ", dictionary["Percentage winrate"], "%")
    print("Times hit: ", dictionary["Strategy"].count("Hit"))