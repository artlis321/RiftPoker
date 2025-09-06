from itertools import combinations
import random

base_deck = [(i,j) for i in range(2,15) for j in ["H","D","C","S"]]

class PokerGame:
    def __init__(self,player_classes,starting_pot):
        self.num_players = len(player_classes)
        self.players = [player_classes[i](self.num_players,i) for i in range(self.num_players)]
        self.banks = [starting_pot for i in range(self.num_players)]

    def hand_rank(hand):
        is_flush = all([card[1] == hand[0][1] for card in hand])

        sorted_hand = sorted(hand)
        numerical_hand = [card[0] for card in sorted_hand]

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

    def run_hand(self,small_index):
        """
        update_dict = {
            cur_phase : in ["Preflop","Flop","Turn","River","Reveal"],
            your_position : in [0(small blind),...,num_players-1(dealer)],
            cur_actor : in [0,...,num_players-1],
            last_actor : in [0,...,num_players-1]
            folded_players : subset [0,...,num_players-1]
            your_hand : [(val,suit),(val,suit)],
            all_hands: [[(val,suit),(val,suit)],...] # this value is None unless in Reveal
            public_hand : [(val,suit),...],
            pots : [(###,[players with access to full pot]),(###,[players with access to this sidepot]),...]
            required_bid : ###,
            cur_bids : [###,###,###,###],
            your_bank : ###,
            all_banks : [###,###,###,###]
        }
        """

        position_to_player_index = [i % self.num_players for i in range(small_index,small_index+self.num_players)]
        cur_deck = random.shuffle(base_deck)
        hands = [[cur_deck.pop(),cur_deck.pop()] for _ in range(self.num_players)]

        cur_phase = "Preflop"
        cur_actor = 0
        last_actor = 0
        folded_players = []
        all_hands = None
        public_hand = []
        pots = [(0,[i for i in range(self.num_players)])]
        required_bid = 2
        cur_bids = [0 for _ in range(self.num_players)]
        all_banks = self.banks

        def send_updates():
            for i in range(self.num_players):
                player_index = position_to_player_index[i]
                update_dict = {
                    "cur_phase" : cur_phase,
                    "cur_actor" : cur_actor,
                    "last_actor" : last_actor,
                    "folded_players" : folded_players,
                    "your_hand" : hands[i],
                    "all_hands" : all_hands,
                    "public_hand" : public_hand,
                    "pots" : pots,
                    "required_bit" : required_bid,
                    "cur_bids" : cur_bids,
                    "your_bank" : self.banks[player_index],
                    "all_banks" : all_banks
                }
                self.players[player_index].receive_game_update(update_dict)

        ### Preflop
        self.banks[position_to_player_index[0]] -= 1
        cur_bids[0] = 1
        self.banks[position_to_player_index[1]] -= 2
        cur_bids[1] = 2
        cur_actor = 2 % self.num_players
        last_actor = 1

        send_updates()

        while cur_actor <= last_actor:
            if cur_actor in folded_players:
                cur_actor += 1
            else:
                actor_index = position_to_player_index[cur_actor]
                next_play = self.players[actor_index].next_play()

                if next_play[0] == "Fold":
                    folded_players.append(cur_actor)
                    folded_players = sorted(folded_players)
                if next_play[0] == "Check":
                    #####


# to be extended by players
class PokerBot:
    def __init__(self,num_players,my_index):
        self.num_players = num_players
        self.my_index = my_index

    def receive_game_update(self,update_dict):
        return

    def next_play(self):
        """
        return ["Fold"]
        return ["Check"] # automatically folds if cannot check
        return ["Call"] # automatically raises to required_bid
        return ["Raise",###] # raises below required_bid automatically raise to it, raises above your_bank automatically go all in
        an error automatically folds
        """
        return ["Fold"]