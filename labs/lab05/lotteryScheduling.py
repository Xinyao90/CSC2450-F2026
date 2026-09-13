import random

wins = {"A": 0, "B": 0}
for i in range(20):
    ticket = random.randrange(100)
    if ticket < 80:
        wins["A"] += 1
    else:
        wins["B"] += 1

print(wins)
