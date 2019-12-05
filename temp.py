values = ["a", "b", 'c', 'd', 'e', 'f', 'g']




with open("./temp.txt", "w") as f:
    for value in values:
        f.write(value + "\n")
