import enum
import constants
import csv

# define game variables
level = 1

# create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
print(world_data)

# load in level data and create world
with open("Game/levels/level1_data.CSV", newline="") as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in row:
            world_data[x][y] = int(tile)


