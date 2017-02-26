import random
import time

#global hardtotal
global true_count
hardtotal = False
Deck=[]
strategy=[]


def new_deck():
    global running_count
    Deck = []
    one_suit=[2,3,4,5,6,7,8,9,10,"J", "Q", "K", "A"] #One suit
    q = 0
    while q < 24: #6 decks of 4 suits
        for i in one_suit:
            Deck.append(i)
        q +=1
    random.shuffle(Deck) #Randomly shuffle the hand
    running_count = 0
    return Deck

def obscure_hit(hand):
    card = Deck.pop(0)
    hand.append(card)

def initial_hit(hand):
    card = Deck.pop(0) #Set card to be first card in deck and remove it
    keep_running_count(card)
    hand.append(card)

def hit(hand):
    card = Deck.pop(0)
    keep_running_count(card)
    hand.append(card)
    strategy.append("Hit")

def split(hand, hand2):
    card = hand.pop(0)
    hand2.append(card)
    initial_hit(hand)
    initial_hit(hand2)
    strategy.append("Split")

def double(hand):
    initial_hit(hand)
    strategy.append("Double")
    #print("Double V")
    return 2

def stay(hand):
    strategy.append("Stay")
    return

def deal(Phand, Dhand):
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
    total = 0
    Aces = 0
    hardtotal = True
    for cards in hand:
        if cards == "J" or cards == "Q" or cards == "K":
            total += 10
        elif cards == "A":
            total += 11
            Aces += 1
            hardtotal = False
        else:
            total += cards

    while Aces > 0 and total > 21:
        total -= 10
        Aces -= 1
    if Aces == 0:
        hardtotal = True

    return total

def perfect_strategy(Pand, Pand2, Dand):
    """




    :param Pand:  Pand is the current player hand
    :param Pand2: Pand2 is the alternate player hand
    :param Dand:  Dand is the dealer hand
    :return: It returns whether the player has doubled or not
    """

    global true_count
    # print(hardtotal)
    var = 1
    #Count based logic

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
    elif Pand[0] == Pand[1] and score([Pand[0]]) == 10 and score([Pand[1]]) == 10 and score([Dand[0]]) == 5: #10 vs 5
        if true_count >= 5:
            #print("Splittable, score = 20, dealer = 6, true count 5+")
            split(Pand, Pand2)
        else:
            #print("Splittable, score = 20, dealer = 6, true count -5")
            stay(Pand)
    elif Pand[0] == Pand[1] and score([Pand[0]]) == 10 and 10 and score([Pand[1]]) == 10 and score([Dand[0]]) == 6: #10 vs 6
        if true_count >= 4:
            split(Pand, Pand2)
        else:
            stay(Pand)
    elif score(Pand) == 10 and score([Dand[0]]) == 10: #10 vs 10
        if true_count >= 4:
            var = double(Pand)
        else:
            hit(Pand)
    elif score(Pand) == 12 and score([Dand[0]]) == 3:#12 vs 3
        if true_count >= 2:
            if split_style(Pand, Pand2, Dand) == 1:
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
    elif hardtotal == False:
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
    global running_count
    global true_count

    if score([card])< 7:
        running_count += 1
    elif score([card]) < 10:
        running_count += 0
    else:
        running_count -= 1
    #print("Decks currently in play:", int(len(Deck)/52))
    try:
        true_count = running_count/int(len(Deck)/52)
    except:
        true_count = running_count

def dealer(Dhand):
    while score(Dhand) < 17:
        initial_hit(Dhand)

def game(loop):
    """
    Main Game Loop:
    This function takes 2 arguments.
    loop: int which controls how many simulations to do
    want: This controls to what value the simulations hit too

    This function controls all of the subfunctions that make up a game
    """
    global Deck
    global running_count
    global true_count
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
        # print("Wager:", wager)
        # print("Running count", running_count)
        # print("Prehand count", prehand_count)
        # print("True count", true_count)
        Phand = []
        Phand2 = []
        Dhand = []
        weight = 1
        #Deal to both hands
        deal(Phand, Dhand)
        #Play out the player hands
        weight *= perfect_strategy(Phand, Phand2, Dhand)
        if len(Phand2) > 0:
            weight *= perfect_strategy(Phand2, Phand, Dhand)
        #Play out the dealer strategy
        dealer(Dhand)
        #Begin comparison of hands and score
        if compare(Phand, Dhand) == 1:
            player_wins += 1*weight*wager
        elif compare(Phand, Dhand) == 1.5:
            player_wins += 1.5*weight*wager
        else:
            dealer_wins += 1*wager
        if len(Phand2) > 0:
            if compare(Phand2, Dhand) == 1:
                split_player_wins += 1*wager
            elif compare(Phand2, Dhand) == 1.5:
                split_player_wins += 1.5*wager
            else:
                split_dealer_wins += 1*wager
        if len(Deck) <= 52:
            Deck = new_deck()
        prehand_count = true_count

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

if __name__ == "__main__":
    sims = int(input("Please input the number of times you would like to loop "))
    dictionary = game(sims)
    print("Time taken: ", dictionary["Time Taken"])
    print("Netgain: ", round(dictionary["Percentage netgain"], 2), "%")
    print("Winrate: ", dictionary["Percentage winrate"], "%")
    print("Times hit: ", dictionary["Strategy"].count("Hit"))
    # mean = np.mean(array)
    # print("Mean of true count:", mean)