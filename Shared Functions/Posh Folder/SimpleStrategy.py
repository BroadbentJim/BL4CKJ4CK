import random
import time


player_wins = 0
dealer_wins = 0
split_player_wins = 0
split_dealer_wins = 0

Deck=[]
Phand=[]
Phand2=[]
Dhand=[]
strategy=[]

dealer_strategy = 0
player_strategy = 0

#w, h = 11, 11
#Matrix = [[0 for x in range(w)] for y in range(h)]
"""def looping():
    global dealer_strategy, player_strategy
    for i in range(11):
        player_strategy = i + 10
        for j in range(11):
            dealer_strategy = j + 10
            game()"""

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
    total = 0
    Aces = 0
    hardtotal = True
    #print ("The length of hand is " + str(len(hand)))
    for cards in hand:
        #print("The card is " + str(cards))
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

def simple_strategy(want):
    if Phand[0] == Phand[1]:
        split(Phand)
    while score(Phand) <= want:
        hit(Phand)
    if len(Phand2) > 0:
        while score(Phand2) <= want:
            hit(Phand2)

def dealer(wanted):
    while score(Dhand) < wanted:
        hit(Dhand)

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
        #dealer_wins += 1
        #return "Dealer won"
        return 0

def game(loop, want):
    global Deck, Phand, Phand2, Dhand
    player_wins = dealer_wins = split_player_wins = split_dealer_wins = 0
    new_deck()
    start_time = time.time()
    for _ in range(loop):
        #Deck = []
        Phand = []
        Dhand = []
        Phand2 = []
        #new_deck()
        deal()
        simple_strategy(want)
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
    "Time": elapsed_time}
    return dictionary


#Debugging code

if __name__ == "__main__":
    sims = int(input("Please input the number of times you would like to loop "))
    wanted = int(input("Please input the number of you'd like to hit too "))
    dictionary = game(sims, wanted)
    print(dictionary["Percentage netgain"])
    print(dictionary["Percentage winrate"])