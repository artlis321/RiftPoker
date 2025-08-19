from itertools import combinations

deck = [(i,j) for i in range(2,15) for j in ["H","D","C","S"]]

class PokerGame:
    def __init__(self,player_classes,starting_pot):
        self.num_players = len(player_classes)
        self.players = [p(self.num_players) for p in player_classes]
        self.banks = [starting_pot for i in range(self.num_players)]

    def hand_rank(hand):
        is_flush = all([card[i][1] == hand[0][1] for card in hand])

        sorted_hand = sorted(hand)
        numerical_hand = [card[i] for card in sorted_hand]

        lowest_card = min(numerical_hand)
        is_straight = (numerical_hand == [2,3,4,5,14]) or ([val-lowest_card for val in numerical_hand] == [0,1,2,3,4])

        counts_dict = {}
        for val in numerical_hand:
            if val in counts:
                counts[val] += 1
            else:
                counts[val] = 1
        counts_pairs = reversed(sorted([(counts_dict[val],val) for val in counts_dict]))
        counts = [i[0] for i in counts_pairs]
        vals = [i[1] for i in counts_pairs]

        if is_flush and is_straight:
            return [9,vals] # straight flush

        if counts == [4,1]:
            return [8,vals] # quad

        if counts == [3,2]:
            return [7,vals] # full house

        if is_flush:
            return [6,vals] # flush
        
        if is_straight:
            return [5,vals] # straight

        if counts == [3,1,1]:
            return [4,vals]

        if counts == [2,2,1]:
            return [3,vals]

        if counts == [2,1,1,1]:
            return [2,vals]

        return [1,vals]

    def best_rank(cards):
        best_rank = [0]
        for hand in combinations(cards,5):
            lhand = list(hand)
            rank = PokerGame.hand_rank(lhand)
            if rank > best_rank:
                best_rank = rank

    def determine_winner(shared,private):
        hand_ranks = []
        for p in private:
            hand_ranks.append( PokerGame.best_rank(shared+p) )
        best_rank = max(hand_ranks)
        return [i for i in range(len(hand_ranks)) if hand_ranks[i]==best_rank]

# to be extended by players
class PokerBot:
    def __init__(self,num_players):
        self.num_players = num_players

    def receive_game_update(self):
        return

    def next_play(self):
        return ["Fold"]