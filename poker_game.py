deck = [(i,j) for i in range(2,15) for j in ["H","D","C","S"]]

class PokerGame:
    def __init__(player_list):
        self.player_list = []

    def hand_rank(hand):
        is_flush = all([card[i][1] == hand[0][1] for card in hand])

        sorted_hand = sorted(hand)
        numerical_hand = [card[i] for card in sorted_hand]

        lowest_card = min(numerical_hand)
        is_straight = (numerical_hand == [2,3,4,5,14]) or ([val-lowest_card for val in numerical_hand] == [0,1,2,3,4])

        if is_flush and is_straight:
            return [9] # straight flush
        
        counts_dict = {}
        for val in numerical_hand:
            if val in counts:
                counts[val] += 1
            else:
                counts[val] = 1
        counts_pairs = reversed(sorted([(counts_dict[val],val) for val in counts_dict]))
        counts = [i[0] for i in counts_pairs]
        vals = [i[1] for i in counts_pairs]

        if counts == [4,1]:
            return [8,vals] # quad

        if counts == [3,2]:
            return [7,vals] # full house

        if is_flush:
            return [6] # flush
        
        if is_straight:
            return [5] # straight

        if counts == [3,1,1]:
            return [4,vals]

        if counts == [2,2,1]:
            return [3,vals]

        if counts == [2,1,1,1]:
            return [2,vals]

        return [1,vals]
