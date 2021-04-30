from card import Card, create_all_cards

class Game:
    def __init__(self, n_players):
        self.cards = create_all_cards()
        self.all_len = len(self.cards)
        self.player_cards = [[] for _ in range(n_players)]
    
    def draw_one_card(self, p_idx):
        card = self.cards.pop()
        self.player_cards[p_idx].append(card)
        return card
    
    def cal_point(self, p_idx):
        point = 0
        n_ace = 0     # number of ace cards
        for c in self.player_cards[p_idx]:
            if c.point == 1:
                point += 11
                n_ace += 1
            elif c.point < 10:
                point += c.point
            elif c.point >= 10:
                point += 10
        
        while point > 21 and n_ace > 0:
            n_ace -= 1
            point -= 10
        
        return point

if __name__ == '__main__':
    g = Game(2)

    # p1 draw
    c = g.draw_one_card(0)
    print('p1 get', c)
    c = g.draw_one_card(0)
    print('p1 get', c)
    print('P1 Total:', g.cal_point(0))

    # p2 draw
    c = g.draw_one_card(1)
    print('p2 get', c)
    c = g.draw_one_card(1)
    print('p2 get', c)
    print('P2 Total:', g.cal_point(1))