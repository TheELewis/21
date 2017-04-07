#TODO: -Implement handling for two aces in hand at once,
#      -Implement being able to play on a hand that you have split
#      -Move betting to the hand class. Maybe make the keep the class for getBet
#         but just use it as a vehicle to add bets to hands and adjust wallet
#         values.
import itertools
import random

# Two dictionary of more verbose card suits and ranks for readable output purposes
suit_verbose = {"s":"Spades", "c":"Clubs", "h":"Hearts", "d":"Diamonds"}
rank_verbose = {"2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9", "T": "10",
                    "J":"Jack", "Q":"Queen", "K":"King", "A":"Ace"}


class Card:
    ''' Data class that handles all the things you could determine by
    looking at a physical card in ones hand. '''

    def __init__(self,rank,suit):
        self._rank = rank
        self._suit = suit

    def value(self):
        ''' Return the integer value of the card '''
        #TODO doesn't properly handle aces yet

        value = 0
        ace = 0
        rank = ord(self._rank)

        if rank == 65: # Ace
            value = 1
            # As of right now aces are only worth one because I need to decide how
            # to deal with multiple aces in one hand

        elif rank in range(50,57): # Non face card or ten
            value = int(chr(rank))

        else: # All remaining cards are worth 10
            value = 10

        return value

    def isAce(self):
        ''' Returns true if the card is an Ace '''
        #NOTE This method might not actually be necessary, I thought it might
        # make code more readable in the end? I don't know; if we never use it
        # I'll remove it.

        if self._rank == "A":
            return True
        else:
            return False

    def display(self):
        ''' Returns a more readable string that describes the card in conventional
        human terms '''

        return "{} of {}".format(rank_verbose[self._rank], suit_verbose[self._suit])

class Hand:

    def __init__(self):
        self._hand = []

    def add(self,card):
        ''' Place a card in the hand '''

        self._hand.append(card)

    def handValue(self):
        ''' Returns the cummulative value of all the cards in the hand '''

        value = 0
        for card in self._hand:
            value += card.value()

        return value

    def cards(self):
        ''' Returns a list of the cards in the hand (returns a list of Card classes) '''

        return self._hand

    def canSplit(self):
        ''' Checks to see if the hand can be split, will only split
        if the hand contains 2 cards of identical rank '''

        if len(self._hand) != 2:
            return False
        else:
            if self._hand[0]._rank == self._hand[1]._rank:
                return True
            else:
                return False

    def discard(self):
        ''' Discards all cards in the hand. Currently only useful for testing.
        May need later '''

        self._hand = []

    def displayHand(self):
        ''' Displays the cards in the hand as a read friendly string '''

        display = list()
        for card in self._hand:
            display.append(card.display())

        return display


class Deck:

    suit = "schd"
    rank = "23456789TJQKA"

    def __init__(self):
        # self._deck = [''.join(card) for card in itertools.product(Deck.suit,Deck.rank)] # list of versions of cards
        self._deck = [Card(j,i) for i in self.suit for j in self.rank]


    def shuffle(self):
        ''' Shuffles the current deck '''
        random.shuffle(self._deck)

    def drawMultiple(self,num_todraw):
        ''' Draws a select number of cards from the current deck and returns them
        as a list
        '''
        result = list()

        for i in range(num_todraw):
            #Draw off the top of the deck
            result.append( self._deck.pop(0) )

        return result

    def draw(self):
        ''' Draw one card from the top of the deck'''

        return self._deck.pop(0)

    def isEmpty(self):
        ''' Checks if the deck is empty '''

        if len(self._deck) > 0:
            return False
        else:
            return True

    def cardsLeft(self):
        ''' Returns the number of cards left in the deck. This is mostly
        to improve readability
         '''
        return len(self._deck)

    def displayDeck(self):
        display = list()
        for card in self._deck:
            display.append(card.display())

        return display

class Player:

    def __init__(self,name,wallet):
        self._name = name
        self._wallet = wallet
        self._hand = Hand()
        self._bet = 0
        self._isBust = False

    def play(self,deck,choice):
        ''' Exectute the players choice for this hand

            (1)Hit: Add a card to the current hand
            (2)Stay: Do nothing
            (3)DoubleDown: Double the bet on the current hand
            (4)Split: Create another hand and add the starting bet to it
        '''
        # Hit
        if choice == 1:
            if deck.cardsLeft() >= 1:
                self._hand.add(deck.draw())
                if self._hand.handValue() > 21:
                    self._isBust = True

        # Stay
        elif choice == 2:
            pass

        # DoubleDown
        elif choice == 3:
            self._hand.getBet(0,True)

        # Split
        elif choice == 4:
            # Make two seperate hands out of the cards currently in hand if
            # allowed (i.e cards_in_hand < 3, card[0] == card[1])

            pass

    def getBet(self, wager, doubleDown = False):
        ''' Place a bet on a hand and remove the amount wagered from the player's
        wallet'''
        
        if wager <= self._wallet:
            if doubleDown:
                self._wallet -= self._bet
                self._bet += self._bet
            else:
                self._wallet -= wager
                self._bet += wager

    def canDouble(self):
        ''' Determines whether a player has enough money to double down '''

        if (self._wallet - (2*self._bet)) < 0:
            return False
        else:
            return True

    def reset(self):
        self._hand.discard()
        self._bet = 0
        self._isBust = False
