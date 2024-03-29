import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n '+card.__str__()
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self, total=200):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
    
def save_chips_total(chips):
    with open("chips_total.txt", "w") as file:
        file.write(str(chips.total))

def load_chips_total():
    try:
        with open("chips_total.txt", "r") as file:
            balance = int(file.read())
            return balance
    except (FileNotFoundError, ValueError):
        return 200

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be a whole number!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total," chips")
            else:
                break

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    
    global playing
    
    while True:
        x = input("Would you like to Hit or Stand? Input: (H/S)")
        
        if x != "":
            if x[0].lower() == 'h':
                print("Player hits.")
                hit(deck,hand)

            elif x[0].lower() == 's':
                print("Player stands. Dealer is playing.")
                playing = False

            else:
                print("The only options are hit (h) or stand (s).")
                continue
            break

def double_bet(deck,hand,chips):
    
    if chips.total >= chips.bet * 2:
        while True:
            x = input("Would you like to double your bet? Input: (Y/N): ")

            if x != "":
                if x[0].lower() == "y":
                    
                    chips.bet = chips.bet * 2
                    print("Player doubled their bet!")
                    hit(deck,hand)
                    
                    break
                elif x[0].lower() == "n":
                    break
                else:
                    print("Please enter Y or N: ")
                    continue
    else:
        print("You don't have enough chips to double your bet!")
                

def show_some(player,dealer):
    
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    
    print("Player busts!")
    chips.lose_bet()
    save_chips_total(chips)

def dealer_wins(player,dealer,chips):
    
    print("Dealer wins!")
    chips.lose_bet()
    save_chips_total(chips)

def player_wins(player,dealer,chips):
    
    print("Player wins!")
    chips.win_bet()
    save_chips_total(chips)

def dealer_busts(player,dealer,chips):
    
    print("Dealer busts!")
    chips.win_bet()
    save_chips_total(chips)
        
def push(player,dealer,chips):
    print("Dealer and Player tie! It's a push.")
    save_chips_total(chips)

while playing==True:
    # Welcome
    player_chips = Chips(load_chips_total())
    print('\n\
            Welcome to BlackJack!\n\
            Get as close to 21 as you can without going over!\n\
            Dealer hits until it reaches 17.\n\
            Aces count as 1 or 11.\n\
            It is possible to double your bet after first two cards are dealt.\n\
            You have :::',player_chips.total, '::: chips available.\n\
                ')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    # Set up the Player's chips
    player_chips = Chips(load_chips_total())
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Ask for double bet or not
        double_bet(deck, player_hand, player_chips)
        show_some(player_hand,dealer_hand)  
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)

        
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            show_all(player_hand,dealer_hand)
            player_busts(player_hand,dealer_hand,player_chips)
            break


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand,player_chips)        
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)
    
    # Ask to play again
    while True:
        new_game = input("Would you like to play another hand? Input (Y/N)")
        if new_game != "":
            if new_game[0].lower()=='y':
                playing=True
                break
            elif new_game[0].lower()=="n":
                print("Thanks for playing! All earnings/losses have been saved.")
                playing=False
                break
            else:
                print("Not a valid answer.")
                continue

    #double-bet
    #split 
            
#from collections import Counter
''' def split(deck, hand):
        if card.count() >= 2 and ...
            x = input("Would you like to split)

            if x != "":
                if x[0].lower() == "y":
                    
                    new_hand = Hand()
                    new_hand.add_card(player_hand.pop())
                    new_hand.add_card(deck.deal())
                    player_hand.add_card(deck.deal())

                    print("Player split")
                    return new_hand, player_hand
                
                else:
                print("Player did not split")
                return player_hand


in de while loop voor eerste hit or stand en dan na elke hit om te checken



wat is blackjack - 
comments -> code -> result





'''
