import random
import time



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

    if total > 21:
        bust = True

    return total


def basic_strategy(Pand, Dand): #Basic Strategy
    global hardtotal
    if split_style(Pand, Dand) == True:
        split(Pand)
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

def split_style(Pand, Dand):
    if Pand[0] == Pand[1] and len(Phand2) == 0:
        if Pand[0] == 'Ace':
            return True
        elif Pand[0] == 8:
            return True
        elif (Pand[0] == 2 or Pand[0] == 3 or Pand[0] == 7) and score([Dand[0]]) < 8:
            return True
        elif Pand[0] == 6 and score([Dand[0]]) < 7:
            return True
        elif Pand[0] == 9 and score([Dhand[0]]) < 10 and score([Dand[0]]) != 7:
            return True
        elif Phand[0] == 4 and score([Dand[0]]) < 7 and score([Dand[0]]) > 4:
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
    "Time": elapsed_time}
    return dictionary


#Debugging code

if __name__ == "__main__":
    ye = game(int(input("Please input the number of times you would like to loop ")))
    print(ye["Percentage netgain"])