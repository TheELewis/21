
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

    def rank(self):
        return self._rank

    def suit(self):
        return self._suit

    def value(self):
        ''' Return the integer value of the card '''

        value = 0
        rank = ord(self._rank)

        if rank == 65: # Ace
            value = 1

        elif rank in range(50,58): # Non face card or ten
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
        self._bet = 0
        self._isBust = False

    def bet(self):
        return self._bet

    def isBust(self):
        return self._isBust

    def setBust(self,is_bust):
        self._isBust = is_bust

    def add(self,card):
        ''' Place a card in the hand '''

        self._hand.append(card)

    def placeBet(self, wager):
        ''' Place a bet on the hand '''

        self._bet += wager


    def handValue(self, for_ai=False):
        ''' Returns the cummulative value of all the cards in the hand '''
        values = [0,0]
        had_eleven = False
        for card in self._hand:
            new_value = card.value()
            if new_value == 1 and not had_eleven:
                values[0] += new_value
                values[1] += new_value + 10

                had_eleven = True
            else:
                for i in range(len(values)):
                    values[i] += new_value
        values_to_keep = []
        for v in values:
            if v <= 21:
                values_to_keep.append(v)

        if not values_to_keep:
            return None
        if for_ai:
            return values_to_keep
        else:
            return max(values_to_keep)

    def cards(self):
        ''' Returns a list of the cards in the hand (returns a list of Card classes) '''

        return self._hand

    def canSplit(self, player):
        ''' Checks to see if the hand can be split, will only split
        if the hand contains 2 cards of identical rank '''

        if len(self._hand) != 2:
            return False

        elif player._wallet < self._bet:
            return False

        else:
            if self._hand[0].value() == self._hand[1].value():
                return True
            else:
                return False

    def discardHand(self):
        ''' Discards all cards in the hand. Currently only useful for testing.
        May need later '''

        del self._hand[:]

    def discardCard(self,card):
        ''' Method for discarding a single specific card from the hand. '''

        self._hand.remove(card)

    def displayHand(self):
        ''' Displays the cards in the hand as a read friendly string '''

        display = list()
        for card in self._hand:
            display.append(card.display())

        return display

class Deck:

    suit = "schd"
    rank = "23456789TJQKA"

    def __init__(self,num_decks):
        self._deck = list()
        self._numDecks = num_decks
        while(num_decks):
            self._deck += [Card(j,i) for i in self.suit for j in self.rank]
            num_decks -= 1
        # high low counter demonstrates the player advantage.
        # Positive counter means the player has the advantage.
        # Negative counter means the dealer has the advantage.
        # increase by 1 for every low card (2,3,4,5,6)
        # decrease by 1 for every high card (10,J,Q,K,A)
        # else do nothing
        # high low AI will use this for determining bet amount
        self._hi_lo_counter = 0

    def highLowCounter(self):
        return self._hi_lo_counter

    def modHighLowCounter(self, mod):
        ''' add mod to the hi_lo_counter '''
        self._hi_lo_counter += mod

    def needShuffle(self):
        ''' returns true if less than 25% of deck left '''
        if self.cardsLeft() < int(52*self._numDecks*0.25):
            self.__init__(self._numDecks)
            self.shuffle()

    def trueCountHiLo(self):
        '''
            Outputs the number of betting units based off count
            according
        '''
        true_count = int(self._hi_lo_counter//(self.cardsLeft()/52))
        return max(0, true_count-1)

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
            result.append( self.draw() )

        return result

    def draw(self):
        ''' Draw one card from the top of the deck'''
        if self.cardsLeft() == 0:
            self.__init__(self._numDecks)
            self.shuffle()
        # print(self._hi_lo_counter)
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

    def reset(self):
        self._deck = [Card(j,i) for i in self.suit for j in self.rank]


class Player:

    def __init__(self,name,wallet,ai=False, betting_unit=10):
        self._name = name
        self._wallet = wallet
        self._prev_wallet = wallet
        self._hands = list()
        self._ai = ai
        self._betting_unit = betting_unit

    def hands(self):
        return self._hands

    def wallet(self):
        return self._wallet

    def prevWallet(self):
        return self._prev_wallet

    def name(self):
        return self._name

    def isAi(self):
        return self._ai

    def bettingUnit(self):
        return self._betting_unit

    def addHand(self,hand):
        self._hands.append(hand)

    def delHand(self,hand):
        hand.discardHand()
        hand._isBust = False
        self._hands.remove(hand)

    def addWallet(self, gain):
        self._wallet += gain

    def updatePrevWallet(self):
        self._prev_wallet = self._wallet

    def dealerUpcard(self):
        '''
            Returns the first card of the first hand,
            used for displaying the upcard of the dealer
        '''
        return self.hands()[0].cards()[0]

    def play(self,choice,deck,hand):
        ''' Exectute the players choice for this hand

            (1)Hit: Add a card to the current hand
            (2)Stay: Do nothing
            (3)DoubleDown: Double the bet on the current hand
            (4)Split: Create another hand and add the starting bet to it
        '''
        # Hit
        if choice == 1:
            card = deck.draw()
            hand.add(card)
            value = hand.handValue()
            if value is None:
                hand.setBust(True)
            # for counting purposes need return card
            return card

        # Stay
        elif choice == 2:
            pass

        # DoubleDown
        elif choice == 3:
            if self.canDouble(hand):
                self.getBet(hand,0,True)
                return self.play(1,deck,hand)
            else:
                input("I'm sorry you do not have enough money to double down")

        # Split
        elif choice == 4:
            # Make two seperate hands out of the cards currently in hand if
            # allowed (i.e cards_in_hand < 3, card[0] == card[1])

            if hand.canSplit(self):
                (card1, card2) = hand.cards()
                hand.discardCard(card2)

                new_hand = Hand()
                new_hand.add(card2)
                new_card1 = deck.draw()
                new_hand.add(new_card1)
                self.getBet(new_hand,hand._bet)
                self.addHand(new_hand)

                new_card2 = deck.draw()
                hand.add(new_card2)
                return (new_card1, new_card2)

        # Surrender
        elif choice == 5:
            self._wallet += hand.bet()//2
            hand.setBust(True)


    def getBet(self,hand, wager, doubleDown = False):
        ''' Place a bet on a hand and remove the amount wagered from the player's
        wallet '''

        if wager <= self._wallet:
            if doubleDown:
                self._wallet -= hand._bet
                hand.placeBet(hand._bet)
            else:
                self._wallet -= wager
                hand.placeBet(wager)
            return True
        else:
            # To make it easier for the counting AI it may be better to make the
            # above is return TRUE and this one Return FALSE.
            return False

    def canDouble(self,hand):
        ''' Determines whether a player has enough money to double down '''

        if (self._wallet - hand._bet) <= 0:
            return False
        else:
            return True

    def printHandsHeld(self,index,full = False):
        ''' Display all or one of the hands the player is currently holding '''

        if full:
            for hand in self._hands:
                print(hand.displayHand())

        else:
            print(self._hands[index].displayHand())

    def returnHandsHeld(self,index=0,full = False):
        ''' Returns all or one of the hands the player is currently holding '''

        if full:
            for hand in self._hands:
                return hand.displayHand()

        else:
            return self._hands[index].displayHand()

    def reset(self):
        # Do not touch, it is magic and necessary and I don't know why
        for hand in self._hands:
            hand.discardHand()
            hand._isBust = False
        del self._hands[:]
