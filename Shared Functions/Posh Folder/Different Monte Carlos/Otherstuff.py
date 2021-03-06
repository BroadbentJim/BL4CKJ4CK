import random
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#import sys #Needed for debugging

global Stay
global Bust
global Bust_counter
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
hardtotal = False


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

def basic_strategy(Pand, Dand): #Basic Strategy
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


def pick_play(Pand, Dand):
    global Total_Matrix
    global Hit_Matrix
    global Split
    #if split_style(Phand, Phand2) == 1:
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
    #
    # if score(Pand) > 17:
    #     stay()
    # elif score(Pand) < 12:
    #     hit(Pand)
    # else:
    #     if total < 1:
    #         random.choice([stay(), hit(Pand)])
    #     else:
    #         hits = Hit_Matrix[score(Pand)-4][score([Dand[0]])-2]
    #         r = float(hits)/float(total)
    #         x = random.random()
    #         if x < r:
    #             hit(Pand)
    #         else:
    #             stay()

    if total < 1:
        random.choice([stay(), hit(Pand)])
        #print("First time in scenario")
    else:
        hits = Hit_Matrix[score(Pand) - 4][score([Dand[0]]) - 2]
        r = float(hits) / float(total)
        x = random.random()
        if x < r:
            hit(Pand)
        else:
            stay()

def update_matrices_stay(hand1, hand2, Result):

    row = score(hand1) -4
    col = score([hand2[0]]) -2

    Total_Matrix[row][col] += 1
    Hit_Matrix[row][col] += Result
    #print("Update_Matrices_Hit")

def random_playing(hand):
    random.choice([stay(), hit(hand)])

def update_matrices_hit(Phand, Dhand, Result):

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


def game(loop):
    global Deck, Phand, Phand2, Dhand, Split
    player_wins = 0
    dealer_wins = 0
    split_player_wins = 0
    split_dealer_wins = 0
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

        monte_carlo(Phand, Dhand)
        if len(Phand2) > 0:
            monte_carlo(Phand2, Dhand)

        # basic_strategy(Phand, Dhand)
        # if len(Phand2) > 0:
        #     basic_strategy(Phand2, Dhand)

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


        if i % 500 == 0:
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
            Results_container.insert(0, win_rate)
            Results_container.pop()
            # print(Results_container)
            # print("Manages to get into if")

            moving_average = 0
            for j in range(len(Results_container)):
                moving_average += Results_container[j] * a_weights[j]

            Results.append(moving_average)
            Resultspos.append(i)
            Results_coarse.append(win_rate)
            Results_coarse_pos.append(i)
            # print(Results_container)
            player_wins = 0
            dealer_wins = 0
            split_dealer_wins = 0
            split_player_wins = 0
            total_player_wins = 0
            total_dealer_wins = 0




    finish_time = time.time()
    time_elapsed = finish_time - start_time
    split_games = split_player_wins + split_dealer_wins
    total_games = loop + split_games
    total_player_wins = player_wins + split_player_wins
    total_dealer_wins = dealer_wins + split_dealer_wins
    net_gain_abs = total_player_wins - total_dealer_wins  # abs means absolute
    net_gain_per = 100*net_gain_abs/total_dealer_wins  # per means percent
    win_rate = round(total_player_wins / total_games * 100, 2)

    print("The player won " + str(player_wins) + " and the dealer won " + str(dealer_wins) + " of " + str(loop) + " games.")
    print("The simulation took " + str(time_elapsed) + " seconds for " + str(loop) + " simulations.")
    print("The player won " + str(split_player_wins) + " and the dealer won " + str(split_dealer_wins) + " of "+ str(split_games) + " split games.")
    print("In total, the player won " + str(total_player_wins) + " and the dealer won " + str(total_dealer_wins) + " of " + str(total_games) + " games.")
    print("This means the player had a " + str(win_rate) + "% win rate.")
    print("This also means that the player's gain percentage was " + str(net_gain_per) + "%")
    print("The program hit " + str(strategy.count("Hit")) + " times.")
    print("The program stayed " + str(strategy.count("Stay")) + " times.")
    print("The program split " + str(strategy.count("Split")) + " times.")
    print("The program bust " + str(Bust_counter) + " times.")
    print(Results)
    print(Hit_Matrix)
    print(Total_Matrix)
    Hit_Ratio_Matrix = Hit_Matrix / Total_Matrix
    print(Hit_Ratio_Matrix)
    np.savetxt("HRM.csv", Hit_Ratio_Matrix, delimiter=",")

    # return np.array(Resultspos), np.array(Results), np.array(Results_coarse), np.array(Results_coarse_pos)
    return Hit_Ratio_Matrix



if __name__ == "__main__":
    # numberofsims = int(input("Please input the number of times you would like to loop "))
    # tenthousand = 10000
    # hundredthousand = 100000
    # x, y, z, aa = game(hundredthousand)
    # for i in range(numberofsims):
    #     a, b, c, d = game(hundredthousand)
    #     y += b
    #     z += c
    #
    #
    # #game(100000)
    # plt.xlabel("Simulations")
    # plt.ylabel("Win Rate")
    # #plt.plot(aa, z/(numberofsims + 1), color = 'black')
    # plt.plot(x, y/(numberofsims + 1), color = 'cyan')
    # plt.show()
    HRM = game(100000)
    cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                                         ['blue', 'black', 'red'],
                                                         256)

    img2 = plt.imshow(HRM, interpolation='nearest',
                         cmap=cmap2,
                         origin='lower')
    plt.xlabel("Score of Dealer Hand")
    plt.ylabel("Score of Player Hand")
    # plt.xlim([2,11])
    # plt.ylim([4,21])
    plt.colorbar(img2, cmap=cmap2)
    plt.grid(True, color='white')
    plt.show()


