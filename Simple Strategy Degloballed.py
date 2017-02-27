import random
import time


hardtotal = False
Deck=[]
strategy=[]

def new_deck():
    Deck = []
    one_suit=[2,3,4,5,6,7,8,9,10,"J", "Q", "K", "A"] #One suit
    q = 0
    while q < 24: #6 decks of 4 suits
        for i in one_suit:
            Deck.append(i)
        q +=1
    random.shuffle(Deck) #Randomly shuffle the hand
    return Deck

def initial_hit(hand):
    card = Deck.pop(0) #Set card to be first card in deck and remove it
    hand.append(card)

def hit(hand):
    card = Deck.pop(0)
    hand.append(card)
    strategy.append("Hit")

def split(hand, hand2):
    card = hand.pop(0)
    hand2.append(card)
    hit(hand)
    hit(hand2)

def double(hand):
    hit(hand)
    #wager = 2 * wager

def stay():
    strategy.append("Stay")
    return

def deal(Phand, Dhand):
    initial_hit(Phand)
    initial_hit(Dhand)
    initial_hit(Phand)
    initial_hit(Dhand)

def score(hand):
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

def simple_strategy(want, Phand, Phand2):
    if Phand[0] == Phand[1]:
        split(Phand, Phand2)
    while score(Phand) <= want:
        hit(Phand)
    if len(Phand2) > 0:
        while score(Phand2) <= want:
            hit(Phand2)

def dealer(Dhand):
    while score(Dhand) < 17:
        initial_hit(Dhand)

def compare(hand1, hand2): #True means Hand1 has won, False means hand2 has won.
    global player_wins
    global dealer_wins

    if score(hand1) == 21 and len(hand1) == 2:
        if score(hand2) == 21 and len(hand2) == 2:
            return 1
        else:
            return 1.5

    if score(hand1) <= 21 and score(hand2) > 21:
        #player_wins += 1
        #return "Player won."
        return 1
    elif score(hand1) > 21 and score(hand2) <= 21:
        #dealer_wins += 1
        return 0
    elif score(hand1) > score(hand2) and score(hand1)<= 21:
        #player_wins += 1
        #return "Player won."
        return 1
    else:

        return 0

def game(loop, want):
    """
    Main Game Loop:
    This function takes 2 arguments.
    loop: int which controls how many simulations to do
    want: This controls to what value the simulations hit too

    This function controls all of the subfunctions that make up a game
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
        simple_strategy(want, Phand, Phand2)
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
    "Time Taken": elapsed_time}
    return dictionary


#Debugging code

if __name__ == "__main__":
##    sims = int(input("Please input the number of times you would like to loop "))
##    wanted = int(input("Please input the number of you'd like to hit too "))
    sims = 1000
    wanted = 17
    dictionary = game(sims, wanted)
    print("Time taken: ", dictionary["Time Taken"])
    print("Netgain: ", dictionary["Percentage netgain"])
    print("Winrate: ", dictionary["Percentage winrate"], "%")
    print("Times hit: ", dictionary["Strategy"].count("Hit"))