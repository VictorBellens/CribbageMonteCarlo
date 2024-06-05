import random


class Card:
    def __init__(self, name, suit, value):
        self.value = value
        self.suit = suit
        self.name = name

    def getInfo(self):
        return self.name, self.suit, self.value

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name


class Deck:
    def __init__(self):
        self.deck = []
        self.__populateDeck()

    def __populateDeck(self):
        for value in range(1, 14):
            if value == 1:
                name = "Ace"
            elif value == 11:
                name = "Jack"
            elif value == 12:
                name = "Queen"
            elif value == 13:
                name = "King"
            else:
                name = ""
            for suit in ["Spades", "Diamonds", "Hearts", "Clubs"]:
                self.deck.append(Card(name, suit, value))

    def getLength(self):
        return len(self.deck)

    def getTop(self):
        return self.deck.pop(0)

    def getRandom(self):
        index = random.randint(0, len(self.deck))
        return self.deck.pop(index)

    def getCut(self):
        index = random.randint(int(len(self.deck) * 0.25), int(len(self.deck) * 0.75))
        return self.deck.pop(index)

    def shuffle(self):
        # Get the length of the deck
        n = self.getLength()

        # Loop over the deck in reverse order
        for i in range(n - 1, 0, -1):
            # Pick a random index from 0 to i
            j = random.randint(0, i)

            # Swap the current card with the randomly selected card
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]

    def getDeck(self):
        for i in self.deck:
            print(i.getInfo())

    def reset(self):
        self.deck = []
        self.__populateDeck()
