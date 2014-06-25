import random
import itertools

def deck():
    deck = [(n, suit) for n in range(1,14) for suit in 'HCDS']
    random.shuffle(deck)
    return deck

assert(len(deck()) == 52)

def quantify(card):
    """map a card to a scalar number"""
    n, suit = card
    return n + 13*('HCDS'.index(suit))

assert(quantify((5, 'H')) == 5)
assert(quantify((13, 'S')) == 52)

def number_to_add(hand):
    """returns a number from 1 to 6 to add to the base card"""
    numeric_hand = map(quantify, hand)
    ordered_hand = sorted(numeric_hand)
    rank_order = tuple(ordered_hand.index(n) for n in numeric_hand)
    return 1 + list(itertools.permutations([0,1,2])).index(rank_order)

assert(number_to_add([(5, 'H'), (6, 'H'), (7, 'H')]) == 1)
assert(number_to_add([(7, 'S'), (8, 'C'), (9, 'H')]) == 6)

def bob(hand):
    """determine mystery card from four card hand"""
    base, card1, card2, card3 = hand
    base_number, mystery_suit = base
    mystery_number = (base_number + number_to_add([card1, card2, card3])) % 13
    return mystery_number, mystery_suit

assert(bob([(3, 'C'), (5, 'H'), (6, 'H'), (7, 'H')]) == (4, 'C'))
assert(bob([(10, 'C'), (7, 'H'), (6, 'H'), (5, 'H')]) == (3, 'C'))

def alice(hand):
    """determine the four cards to send to bob, given five"""
    for suit in 'HCDS':
        cards = filter(lambda card: card[1] == suit, hand)
        if len(cards) >= 2:
            card1, card2 = cards[0], cards[1]
            difference = abs(card1[0] - card2[0])
            if difference < 6:
                base = min(card1, card2)
            else:
                difference = 13 - difference
                base = max(card1, card2)
            rest = filter(lambda card: card not in cards[0:1], hand)
            break
    order = list(itertools.permutations([0,1,2]))[difference - 1]
    return [base, rest[order[0]], rest[order[1]], rest[order[2]]]
    print suit

assert(alice([(3, 'C'), (5, 'H'), (6, 'D'), (7, 'S'), (4, 'C')]) == [(3, 'C'), (5, 'H'), (6, 'D'), (7, 'S')])

print 'tests pass'
