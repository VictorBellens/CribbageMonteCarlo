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
            for suit in ["♣", "♦", "♥", "♠"]:
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
        cut = self.getLength() // 2
        deck1, deck2 = self.deck[:cut], self.deck[cut:]

        for index, item in enumerate(deck2):
            insert_index = index * 2 + 1
            deck1.insert(insert_index, item)

        self.deck = deck1

    def getDeck(self):
        for i in self.deck:
            print(i.getInfo())

    def reset(self):
        self.deck = []
        self.__populateDeck()
