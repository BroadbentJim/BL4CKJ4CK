import random
import time
import numpy as np
import matplotlib.pyplot as plt
#import sys #Needed for debugging

global Stay
global Bust
global Split
Split = False
Bust = False
Bust_counter = 0
Stay = False
player_wins = 0
dealer_wins = 0
split_player_wins = 0
split_dealer_wins = 0
Results = []
Resultspos = []


Deck=[]
Phand=[]
Phand2=[]
Dhand=[]
strategy=[]
Total_Matrix = np.zeros((18,10))
Hit_Matrix = np.zeros((18,10))
Hit_Ratio_Matrix = np.zeros((18,10))

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
    global Split
    Split = True
    strategy.append("Split")
    card = hand.pop(0)
    Phand2.append(card)
    initial_hit(Phand)
    initial_hit(Phand2)

def double(hand):
    hit(hand)
    #wager = 2 * wager

def stay():
    global Stay
    Stay = True
    strategy.append("Stay")
    return

def deal():
    initial_hit(Phand)
    initial_hit(Dhand)
    initial_hit(Phand)
    initial_hit(Dhand)

def bust(hand):
    if score(hand) > 21:
        return True
        #strategy.append("Bust")
    else:
        return False

def score(hand):

    total = 0
    Aces = 0
    #print ("The length of hand is " + str(len(hand)))


    for cards in hand:
        #print("The card is " + str(cards))
        if cards == "J" or cards == "Q" or cards == "K":
            total += 10
        elif cards == "A":
            total += 11
            Aces += 1
        else:
            total += cards

    while Aces > 0 and total > 21:
        total -= 10
        Aces -= 1

    return total

def basic_playing():
    if Phand[0] == Phand[1]:
        split(Phand)
    while score(Phand) <= 14:
        hit(Phand)
    if len(Phand2) > 0:
        while score(Phand2) <= 14:
            hit(Phand2)

def split_style(hand1, hand2):
    if hand1[0] == hand1[1] and len(Phand2) == 0:
        if hand1[0] =="A":
            return 1
        elif hand1[0] == 8:
            return 1
        elif (hand1[0] == 2 or hand1[0] == 3 or hand1[0] == 7) and score([hand2[0]]) < 8:
            return 1
        elif hand1[0] == 6 and score([hand2][0]) < 7:
            return 1
        elif hand1[0] == 9 and score([hand2[0]]) < 10 and score([hand2][0]) != 7:
            return 1
        elif hand1[0] == 4 and score([hand2][0]) < 7 and score([hand2][0]) > 4:
            return 1
        else:
            return 0



def monte_carlo(hand1, hand2):
    global Stay
    global Bust_counter
    #Bust = False
    Stay = False
    #Bust = 0
    while Stay != True:
        pick_play(hand1, hand2)
        #print("Current Hand" + str(hand1))
        if bust(hand1) == True:
            update_matrices_hit(hand1, hand2, 0)
            Bust_counter += 1
            break
        else:
            update_matrices_hit(hand1, hand2, 1)
            #print("Hand midplay")
    #print("Escaped the while")

def pick_play(Pand, Dand):
    global Split
    if split_style(Pand, Dand) == True and len(Phand2) == 0:
        split(Pand)
        return
    #if score(Pand) > 21:
     #   print("The hand that failed" + str(Pand))
     #   print("Phand" + str(Phand))
      #  print("Phand2" + str(Phand2))
      #  print(Split)
     #   sys.exit("Hand too big")
    if score(Pand) == 21:
        stay()
    total = Total_Matrix[score(Pand) - 4][score([Dand[0]])-2]

    if score(Pand) > 17:
        stay()
    elif score(Pand) < 12:
        hit(Pand)
    else:
        if total < 1:
            random.choice([stay(), hit(Pand)])
        else:
            hits = Hit_Matrix[score(Pand)-4][score([Dand[0]])-2]
            r = float(hits)/float(total)
            x = random.random()
            if x < r:
                hit(Pand)
            else:
                stay()

    # if total < 1:
    #     random.choice([stay(), hit(Pand)])
    #     #print("First time in scenario")
    # else:
    #     hits = Hit_Matrix[score(Pand) - 4][score([Dand[0]]) - 2]
    #     r = float(hits) / float(total)
    #     x = random.random()
    #     if x < r:
    #         hit(Pand)
    #     else:
    #         stay()

def update_matrices_stay(hand1, hand2, Result):
    global Total_Matrix
    global Hit_Matrix

    row = score(hand1) -4
    col = score([hand2[0]]) -2

    Total_Matrix[row][col] += 1
    Hit_Matrix[row][col] += Result
    #print("Update_Matrices_Hit")

def random_playing(hand):
    random.choice([stay(), hit(hand)])



def update_matrices_hit(Phand, Dhand, Result):
    global Total_Matrix
    global Hit_Matrix

    row = score(Phand[:-1]) - 4
    col = score([Dhand[0]]) - 2

    Total_Matrix[row][col] += 1
    Hit_Matrix[row][col] += Result
    #print("Update_Matrices_Stay")

def dealer():
    while score(Dhand) < 17:
        hit(Dhand)

def compare(hand1, hand2):


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

def create_results(loop):
    #calculate some nice numbers
    split_games = split_player_wins + split_dealer_wins
    total_games = loop + split_games
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    net_gain_abs = total_player_wins - total_dealer_wins #abs is short for absolute
    net_gain_per = net_gain_abs/total_dealer_wins
    win_rate = round(total_player_wins / total_games * 100, 2)
    #Calculate how many times the player did each move
    hits = strategy.count("Hit")
    stays = strategy.count("Stay")
    splits = strategy.count("Split")
    doubles = strategy.count("Doubles")

    #Calculate the ratios between Hit Matrix and Total matrix
    Hit_Ratio_Matrix = Hit_Matrix / Total_Matrix
    dictionary = {'Total Games': total_games,
    'Total player wins': total_player_wins,
    'Total dealer wins': total_dealer_wins,
    'Percentage netgain': net_gain_per,
    'Percentage winrate': win_rate,
    "Strategy" : strategy}
    return dictionary, Hit_Ratio_Matrix


def game(loop):
    player_wins = dealer_wins = split_player_wins = split_dealer_wins = 0
    global Deck, Phand, Phand2, Dhand, Split
    global Bust_counter
    start_time = time.time()
    new_deck()
    Results = []
    Results_container = []
    Resultspos = []
    for i in range(loop):
        #Deck = []
        Split = False
        Phand = []
        Dhand = []
        Phand2 = []
        #new_deck()
        deal()
        if len(Phand2) > 0:
            monte_carlo(Phand2, Dhand)
        #random_playing(Phand)
        dealer()
        if compare(Phand, Dhand) == 1:
            player_wins += 1
            update_matrices_stay(Phand, Dhand, 0)
        elif compare(Phand, Dhand) == 1.5:
            player_wins += 1.5
        else:
            dealer_wins += 1
            if bust(Phand) != True:
                update_matrices_stay(Phand, Dhand, 1)
        if len(Phand2) > 0:
            if compare(Phand2, Dhand) == 1:
                split_player_wins += 1
                update_matrices_stay(Phand2, Dhand, 0)
            elif compare(Phand2, Dhand) == 1.5:
                split_player_wins += 1.5
            else:
                split_dealer_wins += 1
                if bust(Phand2) != True:
                    update_matrices_hit(Phand2, Dhand, 1)
        if len(Deck) <= 52:
            new_deck()
        # if i % 1000 == 0 and i != 0:
        #
        #
        #
        #     split_games = split_player_wins + split_dealer_wins
        #     total_player_wins = player_wins + split_player_wins
        #     total_dealer_wins = dealer_wins + split_dealer_wins
        #     total_games = split_games + player_wins + dealer_wins
        #     net_gain_abs = total_player_wins - total_dealer_wins  # abs means absolute
        #     net_gain_per = 100 * net_gain_abs / total_dealer_wins  # per means percent
        #     #win_rate = round(total_player_wins / total_games * 100, 2)
        #     Results_container.append(net_gain_per)
        #     #print(Results_container)
        #     if len(Results_container) == 10:
        #         #print("Manages to get into if")
        #         moving_average = np.mean(Results_container)
        #         Results.append(moving_average)
        #         Resultspos.append(i)
        #         Results_container = []
        #         #print(Results_container)
        #     player_wins = 0
        #     dealer_wins = 0
        #     split_dealer_wins = 0
        #     split_player_wins = 0

        if i % 50 == 0:
            if i == 0:
                Results_coarse = []
                Results_coarse_pos = []
                Results_container = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                a_weights = [0.000001, 0.00001, 0.000078, 0.000489, 0.002403, 0.009245, 0.027835, 0.065591, 0.120978, 0.174666, 0.197413, 0.174666, 0.120978, 0.065591, 0.027835, 0.009245, 0.002403, 0.000489, 0.000078, 0.00001, 0.000001]

            split_games = split_player_wins + split_dealer_wins
            total_player_wins = player_wins + split_player_wins
            total_dealer_wins = dealer_wins + split_dealer_wins
            total_games = split_games + player_wins + dealer_wins
            net_gain_abs = total_player_wins - total_dealer_wins  # abs means absolute
            win_rate = round(total_player_wins / total_games * 100, 2)
            try:
                net_gain_per = 100 * net_gain_abs / total_dealer_wins  # per means percent
            except:
                net_gain_per = 0
            Results_container.insert(0, net_gain_per)
            Results_container.pop()
            # print(Results_container)
            # print("Manages to get into if")

            moving_average = 0
            for j in range(len(Results_container)):
                moving_average += Results_container[j] * a_weights[j]

            Results.append(moving_average)
            #Resultspos.append(i)
            Results_coarse.append(net_gain_per)
            #Results_coarse_pos.append(i)
            # print(Results_container)
            player_wins = 0
            dealer_wins = 0
            split_dealer_wins = 0
            split_player_wins = 0


    Resultspos = np.linspace(50, loop, loop/50)

    # calculate some nice numbers
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    split_games = split_player_wins + split_dealer_wins
    total_games = loop + split_games
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    net_gain_abs = total_player_wins - total_dealer_wins  # abs is short for absolute
    net_gain_per = net_gain_abs / total_dealer_wins
    win_rate = round(total_player_wins / total_games * 100, 2)
    # Calculate how many times the player did each move
    hits = strategy.count("Hit")
    stays = strategy.count("Stay")
    splits = strategy.count("Split")
    doubles = strategy.count("Doubles")

    # Calculate the ratios between Hit Matrix and Total matrix
    Hit_Ratio_Matrix = Hit_Matrix / Total_Matrix
    print(Results)
    dictionary = {'Total Games': total_games,
                  'Total player wins': total_player_wins,
                  'Total dealer wins': total_dealer_wins,
                  'Percentage netgain': net_gain_per,
                  'Percentage winrate': win_rate,
                  "Strategy": strategy,
                  "Time": elapsed_time,
                  "Netgain over time": Results}
    return dictionary, Hit_Ratio_Matrix

def simulations(loop):
    gains = []
    start_time = time.time()
    for i in range(99):
        gains.append(game(loop)["Percentage netgain"])
    dictionary, Hit_Ratio_Matrix = game(loop)
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    dictionary["Time"] = elapsed_time
    gains.append(dictionary["Percentage netgain"])

    dictionary["Gainz"] = gains
    #print(dictionary)
    return dictionary, Hit_Ratio_Matrix

# if __name__ == "__main__":
#     numberofsims = int(input("Please input the number of times you would like to loop "))
#     tenthousand = 10000
#     hundredthousand = 100000
#     x, y = game(hundredthousand)
#     for i in range(numberofsims):
#         a, b = game(hundredthousand)
#         y += b
#
#
#     #game(100000)
#     plt.xlabel("Simulations")
#     plt.ylabel("Net Gain")
#     plt.plot(x, y/numberofsims + 1)
#     plt.show()


