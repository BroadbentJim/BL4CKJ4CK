import random
import time


global true_count
hardtotal = False
Deck=[]
strategy=[]


def new_deck():
    """
        New Deck Function:
        Parameters: NONE
        This function creates a Deck array and deals to it
        THIS FUNCTION updates one global: running_count
        It resets running_count when the deck is refreshed
        returns:
        Deck: The deck array that will hold the cards.

    """
    global running_count
    Deck = []
    # Create deck array
    one_suit = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]  # Defines One suit
    q = 0
    while q < 24:  # 6 decks of 4 suits
        for i in one_suit:  # For each card in a suit
            Deck.append(i)  # Add that card to the deck
        q += 1
    random.shuffle(Deck)  # Randomly shuffle the deck
    running_count = 0
    return Deck

def obscure_hit(hand):
    """
    Obscure Hit
    This hit is used for the dealer's 2nd card
    Parameter(s): hand
     hand: This hand is being hit. Should be the dealer's hand
    :return:
    """
    card = Deck.pop(0)
    hand.append(card)

def initial_hit(hand):
    """
    Hit function used for dealing

    Parameter(s): hand
    hand: the hand that is being hit
    This function is important as it doesn't update the strategy array
    """
    card = Deck.pop(0) #Set card to be first card in deck and remove it
    keep_running_count(card) #Take the running count of the card
    hand.append(card) # Add the card to the hand array

def hit(hand):
    """
    Hit function used typically

    Parameter(s): hand
    hand: the hand that is being hit
    This function is significant as it updates the strategy array providing a useful statistic to my client
    """
    card = Deck.pop(0)  # Set card to be first card in deck and remove it
    keep_running_count(card) # Take the running count of the card
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
    Double Function
    THIS FUNCTION CHANGES ONE GLOBAL Stay
    Stay: Whether the plays stayed or not
    hand: The player's first hand. Typically Phand
    return 2 cause that is how I change the wager
    """
    #Declare the global stay
    global Stay

    initial_hit(hand)#Hit the hand silently
    strategy.append("Double")#Update the strategy array
    Stay = True
    return 2

def stay(hand):
    """
    Stay Function:
    This function will update the strategy array accordingly
    THIS FUNCTION CHANGES ONE GLOBAL
    Stay: It changes it cause it is the stay function
    """
    #Declare global variables
    global Stay

    strategy.append("Stay") #Update the strategy array
    Stay = True

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
    obscure_hit(Dhand)


def score(hand):
    """
    THIS FUNCTION CHANGES A GLOBAL SPECIFICALLY HARDTOTAL
    It should score the hand
    It takes exactly one argument
    hand which is the hand which needs to be scored

    Global Explaination:
        hardtotal is whether the hard contains Aces or not
        Elsewhere in the program, we need to be aware of whether the hand
        is a hardtotal or not

    This function returns the score to where it was called from
"""
    global hardtotal
    # Create empty holder variables and reset hardtotal
    total = 0
    Aces = 0
    hardtotal = True
    for cards in hand:#iterate through every card in the hand array
        if cards == "J" or cards == "Q" or cards == "K":  # if the card is a Jack, Queen, Kind
            total += 10  # The score of the hand is increased by 10
        elif cards == "A":  # If the card is an Ace
            total += 11
            Aces += 1
            hardtotal = False  # Hardtotal is changed to reflect that the hand contains an Ace
        else:
            total += cards  # Otherwise just add the numerical value of the card to the total

    while Aces > 0 and total > 21:  # If the total would cause the player to bust and there are ace(s)
        total -= 10  # Take the Ace to be worth 1
        Aces -= 1  # Decrement the number of aces
    if Aces == 0:  # If no aces or all aces taken to be 1
        hardtotal = True  # The hand is a hardtotal

    return total

def perfect_strategy(Pand, Pand2, Dand):
    """
    Perfect Strategy
    :param Pand:  Pand is the current player hand
    :param Pand2: Pand2 is the alternate player hand
    :param Dand:  Dand is the dealer hand
    :return: It returns whether the player has doubled or not
    """

    var = 1

    if score(Pand) == 16 and score([Dand[0]]) == 10: #16 vs 10
        if true_count > 0:
            if split_style(Pand, Pand2, Dand) == True:
                split(Pand, Pand2)
                #print("Score = 16, dealer score = 10, true count +ve and splittable")
            else:
                #print("Score = 16, dealer score = 10, true count +ve and  NOT splittable")
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 15 and score([Dand[0]]) == 10: #15 vs 10
        if true_count >= 4:
            if split_style(Pand, Pand2, Dand) == True:
                #print("Score = 15, dealer score = 10, true count 4+ and splittable")
                split(Pand, Pand2)
            else:
                #print("Score = 15, dealer score = 10, true count 4+ and  NOT splittable")
                stay(Pand)
        else:
            #print("Score = 15, dealer score = 10, true count -4")
            hit(Pand)
    elif Pand[0] == Pand[1] and score([Pand[0]]) == 10 and len(Pand2) == 0 and score([Dand[0]]) == 5: #10 vs 5
        if true_count >= 5:
            #print("Splittable, score = 20, dealer = 6, true count 5+")
            split(Pand, Pand2)
        else:
            #print("Splittable, score = 20, dealer = 6, true count <5")
            stay(Pand)
    elif Pand[0] == Pand[1] and score([Pand[0]]) == 10 and len(Pand2) == 0 and score([Dand[0]]) == 6: #10 vs 6
        if true_count >= 4:
            #Splittable, Score of dealer hand = 6 and true count>=4
            split(Pand, Pand2)
        else:
            #True count <4
            stay(Pand)
    elif score(Pand) == 10 and score([Dand[0]]) == 10: #10 vs 10
        if true_count >= 4:
            var = double(Pand)
            #If true_count >= 4, double
        else:
            #True count <4
            hit(Pand)
    elif score(Pand) == 12 and score([Dand[0]]) == 3:#12 vs 3
        if true_count >= 2:
            if split_style(Pand, Pand2, Dand) == 1:
                #If Split_style evaluates to true
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 12 and score([Dand[0]]) == 2: #12 vs 2
        if true_count >= 3:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 11 and score ([Dand[0]]) == 11:#11 vs 11
        if true_count >= 1:
            var = double(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 9 and score([Dand[0]]) == 2:#9 vs 2
        if true_count >= 1:
            var = double(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 10 and score([Dand[0]]) == 11:#10 vs 11
        if true_count >= 4:
            var = double(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 9 and score([Dand[0]]) == 7:
        if true_count >= 3:
            var = double(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 16 and score([Dand[0]]) == 9:
        if true_count >= 5:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 13 and score([Dand[0]]) == 2:
        if true_count >= -1:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 12 and score([Dand[0]]) == 4:
        if true_count >= 0:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 12 and score([Dand[0]]) == 5:
        if true_count >= -1:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 12 and score([Dand[0]]) == 6:
        if true_count >= -1:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 13 and score([Dand[0]]) == 3:
        if true_count >= -2:
            if split_style(Pand, Pand2, Dand) == 1:
                split(Pand, Pand2)
            else:
                stay(Pand)
        else:
            hit(Pand)
    elif split_style(Pand, Pand2, Dand) == True:
        split(Pand, Pand2)
    elif hardtotal == False:
        # print("hardtotal = False")
        if score(Pand) == 13 and score([Dand[0]]) > 4 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) == 14 and score([Dand[0]]) > 4 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) == 15 and score([Dand[0]]) > 3 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) == 16 and score([Dand[0]]) > 3 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) == 17 and score([Dand[0]]) > 2 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) == 18 and score([Dand[0]]) > 2 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) < 18:
            hit(Pand)
        elif score(Pand) == 18 and score([Dand[0]]) > 8:
            hit(Pand)
        else:
            stay(Pand)

    elif hardtotal == True:
        # print("hardtotal = True")
        if score(Pand) == 9 and score([Dand[0]]) > 2 and score([Dand[0]]) < 7:
            var = double(Pand)
        elif score(Pand) == 10 and score([Dand[0]]) < 10:
            var = double(Pand)
        elif score(Pand) == 11 and score([Dand[0]]) < 11:
            var = double(Pand)
        elif score(Pand) < 12:
            hit(Pand)
        elif score(Pand) < 17 and score([Dand[0]]) > 6:
            hit(Pand)
        elif score(Pand) == 12 and score([Dand[0]]) < 4:
            hit(Pand)
        else:
            stay(Pand)
    return var


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
        if Pand[0] == 'Ace':
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



def get_wager(ccount):
    """
    Choose player wager
    Parameter(s): ccount
    ccount: Current Count. The current true count
    return var: The amount the player should bet
    """
    #The following if statements are self-explainatory
    if ccount >= 8:
        var = 5
    if ccount >= 6:
        var = 4
    if ccount >= 4:
        var = 3
    if ccount >= 2:
        var = 2
    else:
        var = 1
    return var

def keep_running_count(card):
    """
    Updates the running count
    Parameter(s): card
    card: The card updating the running count
    THIS FUNCTION CHANGES 2 global variables
    running_count and true_count
    """
    #Declare relevant globals
    global running_count
    global true_count
    #If score less than 7, add 1. if score between 7 and 9, no change and if score > 10, minus 1
    if score([card])< 7:
        running_count += 1
    elif score([card]) < 10:
        running_count += 0
    else:
        running_count -= 1
    #print("Decks currently in play:", int(len(Deck)/52))
    #Calculate true_count
    try:
        true_count = running_count/int(len(Deck)/52)
    except:
        true_count = running_count

def dealer(hand):
    """
    Dealer function:
    Parameter: hand
    hand: The dealer's hand for which the logic must be followed
    """
    while score(hand) < 17: #While the dealer's score is less than 17
        initial_hit(hand) #Invisibly hit the dealer's hand

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
    global running_count
    global true_count
    global Stay
    Stay = False
    #this global variable holds the deck
    #Create and set to zero score variables
    player_wins, dealer_wins, split_player_wins, split_dealer_wins = (0,)*4
    #Create an empty Deck variable
    Deck = new_deck()
    #Record start_time
    start_time = time.time()
    prehand_count, running_count, true_count = (0,)*3


    for _ in range(loop):
        #Loop for required number
        #Create empty arrays to hold the hands

        wager = get_wager(prehand_count)
        #Test code
        # print("Wager:", wager)
        # print("Running count", running_count)
        # print("Prehand count", prehand_count)
        # print("True count", true_count)
        Phand = []
        Phand2 = []
        Dhand = []
        #Create/reset a weight for the hand
        weight = 1
        #Deal to both hands
        deal(Phand, Dhand)
        #Play out the player hands
        weight *= perfect_strategy(Phand, Phand2, Dhand) #Times weight by whether the player doubled or not
        while Stay != True:
            #While the player hasn't stayed
            perfect_strategy(Phand, Phand2, Dhand)#Don't change weight to reflect that you can only double once
            # print("Strategied")
        Stay = False
        #Reset Stay for the dealer hand
        if len(Phand2) > 0:#If have split
            weight *= perfect_strategy(Phand2, Phand, Dhand)#Follow same logic for second hand. Change of Phand2 first
            while Stay != True:
                #While the player hasn't stayed
                perfect_strategy(Phand2, Phand, Dhand)#Don't change weight to reflect that you can only double once
                # print("Strategied")
        #Play out the dealer strategy
        dealer(Dhand)
        # Debug code. I was unsure whether a certain scenario was accounted for
        # if score(Phand) < 12 and strategy[-1:] != ['Double']:
        #     print(strategy[-1:])
        #     print("Phand",Phand)
        #     print("Phand2",Phand2)
        #     print(i)
        #     break
        #Begin comparison of hands and score
        if compare(Phand, Dhand) == 1:
            player_wins += 1*weight*wager
        elif compare(Phand, Dhand) == 1.5:
            player_wins += 1.5*weight*wager
        else:
            dealer_wins += 1*wager*weight
        if len(Phand2) > 0:
            if compare(Phand2, Dhand) == 1:
                split_player_wins += 1*wager*weight
            elif compare(Phand2, Dhand) == 1.5:
                split_player_wins += 1.5*wager*weight
            else:
                split_dealer_wins += 1*wager*weight
        if len(Deck) <= 52:
            Deck = new_deck()

        prehand_count = true_count #The prehand count for the next hand is the true count at the end of this hand
        Stay = False

    #Calculate time
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    #Calculate values about the game
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    total_games = total_dealer_wins + total_player_wins
    net_gain_abs = total_player_wins - total_dealer_wins  # abs is short for absolute

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
    "Time": elapsed_time,}
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

if __name__ == "__main__":
    sims = int(input("Please input the number of times you would like to loop "))
    dictionary = game(sims)
    print("Time taken: ", dictionary["Time"])
    print("Netgain: ", round(dictionary["Percentage netgain"], 2), "%")
    print("Winrate: ", dictionary["Percentage winrate"], "%")
    print("Times hit: ", dictionary["Strategy"].count("Hit"))
    # mean = np.mean(array)
    # print("Mean of true count:", mean)