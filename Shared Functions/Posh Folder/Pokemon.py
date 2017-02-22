import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os
global PokeMatrix
#global frame_size
frame_size = 100
idMatrix = np.zeros([frame_size, frame_size])

fig = plt.figure()

class Pokemon:

    def __init__(self, i, j):
        i_ = i*i
        j_ = j*j
        self.id = i_+j_ #* np.random.randint(0, 10)
        total = 255
        self.health = 100 + np.random.randint(0, 255)
        total -= (self.health-100)
        self.attack = np.random.randint(0, total)
        total -= (self.attack - 100)
        self.defense = np.random.randint(0, total)
        total -= (self.defense- 100)
        self.speed = total
        self.age = False

def setup():
    global PokeMatrix
    PokeMatrix = np.array([[Pokemon(i, j) for i in range(frame_size)] for j in range(frame_size)], dtype=object)


def damage(player, enemy):
    dealt = int(player.attack-(enemy.defense/2))
    enemy.health -= dealt
    if enemy.health <= 0:
        player.health += 100
        enemy.health = player.health
        enemy.speed = player.speed
        enemy.defense = player.defense
        enemy.attack = player.attack
        enemy.id = player.id
        enemy.age = True

def getWeakest(x, y):
    NESW = [0, 0, 0, 0]
    Origin = PokeMatrix[x][y].speed

    #Check North and wrap

    if y+1 == frame_size:
        if PokeMatrix[x][0].id != PokeMatrix[x][y].id:
            NESW[0] = PokeMatrix[x][0].speed
        else:
            NESW[0] = 100000
    else:
        if PokeMatrix[x][y+1].id != PokeMatrix[x][y].id:
            NESW[0] = PokeMatrix[x][y+1].speed
        else:
            NESW[0] = 100000
    if y-1 == -1:
        if PokeMatrix[x][frame_size-1].id != PokeMatrix[x][y].id:
            NESW[1] = PokeMatrix[x][frame_size-1].speed
        else:
            NESW[1] = 100000
    else:
        if PokeMatrix[x][y-1].id != PokeMatrix[x][y].id:
            NESW[1] = PokeMatrix[x][y-1].speed
        else:
            NESW[1] = 100000

    if x+1 == frame_size:
        if PokeMatrix[0][y].id != PokeMatrix[x][y].id:
            NESW[2] = PokeMatrix[0][y].speed
        else:
            NESW[2] = 100000
    else:
        if PokeMatrix[x+1][y].id != PokeMatrix[x][y].id:
            NESW[2] = PokeMatrix[x+1][y].speed
        else:
            NESW[2] = 100000


    if x-1 == -1:
        if PokeMatrix[frame_size-1][y].id != PokeMatrix[x][y].id:
            NESW[3] = PokeMatrix[frame_size-1][y].speed
        else:
            NESW[3] = 100000
    else:
        if PokeMatrix[x-1][y].id != PokeMatrix[x][y].id:
            NESW[3] = PokeMatrix[x - 1][y].speed
        else:
            NESW[3] = 100000


    #print(NESW)
    least = (NESW.index(min(NESW)))
    if Origin > NESW[least]:
        if least == 0:
            if y + 1 == frame_size:
                return x, 0
            else:
                return x, y+1

        if least == 1:
            if y-1 == -1:
                return x, frame_size-1
            else:
                return x, y-1
        if least == 2:
            if x + 1 == frame_size:
                return 0, y
            else:
                return x+1, y
        if least == 3:
            if x - 1 == -1:
                return frame_size-1, y
            else:
                return x-1, y
    else:
        return -1, -1


im = plt.imshow(idMatrix, animated=True)
def print_results():
    os.system('cls')
    for i in range(frame_size):
        print()
        for j in range(frame_size):
            print("{:4d}".format(PokeMatrix[i][j].id), end=' ')

def draw():
    refreshid()
    im.set_array(idMatrix)
    return im,

def compare(matrixa, matrixb):
    total = frame_size**2
    c = 0
    for i in range(frame_size):
        for j in range(frame_size):
            print(matrixa[i][j])
            for k in range(min(len(matrixa[i][j]), len(matrixb[i][j]))):
                if matrixa[i][j][k] == matrixb[i][j][k]:
                    c += 1
    if c == total:
        return 1
    else:
        return 0



def refreshid():
    local = np.zeros([frame_size, frame_size])
    for i in range(frame_size):
        for j in range(frame_size):
            local[i][j] = PokeMatrix[i][j].id
    return local

def sim(loop):
    start_time = time.time()
    setup()
    array = []
    for counter in range(loop):
        #print_results()
        # if counter % 100 == 0:
        #     array.append(refreshid())
        #     if len(array) == 1:
        #         pass
        #     elif compare(array[:-1], array[-2:-1]) == 1:
        #         print(counter)
        #         break
        for i in range(frame_size):
            for j in range(frame_size):
                if PokeMatrix[i][j].age == True:
                    PokeMatrix[i][j].age == False
                    pass
                x, y = getWeakest(i, j)
                if x == -1:
                    pass
                else:
                    damage(PokeMatrix[i][j], PokeMatrix[x][y])
    finish_time = time.time()
    elapsed_time = finish_time - start_time
    print(elapsed_time)
loops = int(input("How many frames would you like to do? "))

sim(loops)
print(idMatrix)
idMatrix = refreshid()
print(idMatrix)
plt.imshow(idMatrix)
plt.title(loops)
plt.show()

