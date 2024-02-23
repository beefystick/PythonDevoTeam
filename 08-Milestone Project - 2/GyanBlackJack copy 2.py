# import random module to shuffle deck
import random

#creation of cards deck with values for blackjack
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
#ranks = ('Ten', 'Jack', 'Queen', 'King')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#global variable for if the game is going to continue or not
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

#save chips after game ends   
def save_chips_total(chips):
    with open("chips_total.txt", "w") as file:
        file.write(str(chips.total))

#load players chips from last saved session
def load_chips_total():
    try:
        with open("chips_total.txt", "r") as file:
            balance = int(file.read())
            return balance
    except (FileNotFoundError, ValueError):
        return 200

#take bet function to allow player to input howmany chips they want to bet
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? : '))
        except ValueError:
            print('Sorry, a bet must be a whole number!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total," chips")
            else:
                break

# hitting means adding card for player, and adjust ace if nessesary
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# hit or stand function allowing player to choose between hitting or standing
def hit_or_stand(deck,hand):
    # make sure players game is running
    global playing
    # while loop to continue asking unless given a valid answer
    while True:
        x = input("Would you like to Hit or Stand? (H/S): ")
        
        if x != "":
            if x[0].lower() == 'h':
                print("You've chosen to hit!")
                # if player hits run hit function
                hit(deck,hand)

            elif x[0].lower() == 's':
                print("Player stands. Dealer is playing.")
                playing = False

            else:
                print("The only options are hit (h) or stand (s).")
                continue
            break

# function to enable chips to be doubled if player has enough, upon double hit player once more.
def double_bet(deck,hand,chips):
    #check to see if player is not poor
    if chips.total >= chips.bet * 2:
        while True:
            x = input("Would you like to double your bet? (Y/N): ")
            # check for valid inputs
            if x != "":
                if x[0].lower() == "y":
                    # double player bet and hit
                    chips.bet = chips.bet * 2
                    print("You have doubled your bet! You have received one card.")
                    hit(deck,hand)
                    
                    break
                elif x[0].lower() == "n":
                    break
                else:
                    print("Please enter Y or N: ")
                    continue
    else:
        print("You don't have enough chips to double your bet!")

# function to enable player to split deck IF there are two cards of the same rank(value)
def split(deck,player_hand):
    # check if the deck has two of the same cards and is also 2 cards
    if len(player_hand.cards) == 2 and player_hand.cards[0].rank == player_hand.cards[1].rank:
        while True:
            x = input("Would you like to split? (Y/N): ")
            # make a new hand object, add one of the two cards to this new hand and give both old and new hand one card 
            if x != "":
                if x.lower() == "y":
                    # make left hand
                    new_hand = Hand()

                    # pop out one of the doubles from right hand and add into left hand
                    new_card = player_hand.cards.pop()
                    new_hand.add_card(new_card)

                    # readjust right hand value since card was taken out
                    player_hand.value -= new_hand.value
                    
                    # add cards to both hands due to split
                    new_hand.add_card(deck.deal())
                    player_hand.add_card(deck.deal())

                    # print(player_hand.value)
                    # add something to check value of right hand (original hand) because old value sticks when calculating wins/losses

                    print("You have split your hand, right hand will play first. Both hands have received a card.")
                    return new_hand, player_hand
                elif x.lower() == "n":
                    print("Player did/can not split their hand")
                    return None, player_hand
                else:
                    print("Please enter Y or N: ")
                    continue
    
    


def show_some(player,dealer):
    
    print("--------------------------")
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("--------------------------")

def show_all(player,dealer):
    
    print("--------------------------")
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)
    print("--------------------------")

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
    
    # Create & shuffle the deck, deal two cards to each players hand
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
    
    # Ask for double bet or not
    double_bet(deck, player_hand, player_chips)

    # check and see if possible to split
    new_hand, player_hand = split(deck,player_hand)

    # create different hands in list
    hands_to_play = [player_hand]

    # if the new hand returns anything but None add it to hands, making you have two hands
    if new_hand is not None:
        hands_to_play.append(new_hand)
    else:
        hands_to_play = [player_hand]
    
    # right hand plays first, thus first hand player had (original hand) will play first
    for current_hand in hands_to_play:
        while playing:  # recall this variable from our hit_or_stand function
            
            # Prompt for Player to Hit or Stand
            hit_or_stand(deck,current_hand)
            show_some(current_hand,dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if current_hand.value > 21:
                show_all(current_hand,dealer_hand)
                player_busts(current_hand,dealer_hand,player_chips)
                break


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    for current_hand in hands_to_play:
        if current_hand.value <= 21:
            
            while dealer_hand.value < 17:
                hit(deck,dealer_hand)
        
            # Show all cards
            show_all(current_hand,dealer_hand)
            
            # Run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(current_hand,dealer_hand,player_chips)
            
            else:
                for current_hand in hands_to_play:
                    if current_hand.value <= 21:

                        if dealer_hand.value > current_hand.value:
                            dealer_wins(current_hand,dealer_hand,player_chips)

                        elif dealer_hand.value < current_hand.value:
                            player_wins(current_hand,dealer_hand,player_chips)

                        else:
                            push(current_hand,dealer_hand,player_chips)        
    
    # Inform Player of their total chips which are saved 
    print("\nPlayer's winnings stand at",player_chips.total)
    
    # Ask to play again if no exit while loop, if true restart from top
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