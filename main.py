import random
from game import Game

if __name__ == "__main__":
    import os
    csv_files = [file for file in os.listdir() if '.csv' in file]
    if len(csv_files) < 1:
        print("No .csv files found")
        exit()
    else:
        g = Game(random.choice(csv_files))
        g.start()