from card import Card, create_all_cards

dash = '-' * 10

class Game:
    def __init__(self, n_players):
        self.cards = create_all_cards()
        self.all_len = len(self.cards)
        self.player_cards = [[] for _ in range(n_players)]
        self.points = [0 for _ in range(n_players)]

        self.n_players = n_players
        self.now_player = 0
        print(f'{dash}Turn of player {self.now_player} {dash}')
    
    def next_player(self):
        self.now_player += 1
        if self.now_player >= self.n_players:
            self.game_end()
        else:
            print(f'{dash}Turn of player {self.now_player} {dash}')

    def game_end(self):
        print(f'{dash} Game is end {dash}')
        winner = -1
        tie = []

        points = [self.cal_point(i) for i in range(self.n_players)]
        for i in range(self.n_players):
            p = points[i]
            print(f'Player {i} got {p} points')
            if p > 0 and p <= 21:
                if winner == -1:
                    winner = i
                elif p > points[winner]:
                    winner = i
                    tie = []
                elif p == points[winner]:
                    tie.append(i)
        
        if not tie:
            print(f'Winner is Player {winner}')
        else:
            print(' and '.join(['Player {t}' for t in tie]), end='')
            print(' Tie')

    def draw_one_card(self, p_idx):
        card = self.cards.pop()
        self.player_cards[p_idx].append(card)

        points = self.cal_point(p_idx)
        print('p {} get {} points'.format(
            p_idx, points
        ))
        if points > 21:
            print(f'Player {p_idx} is BOOM')
            self.next_player()

        return card
    
    def cal_point(self, p_idx):
        points = 0
        n_ace = 0     # number of ace cards
        for c in self.player_cards[p_idx]:
            if c.point == 1:
                points += 11
                n_ace += 1
            elif c.point < 10:
                points += c.point
            elif c.point >= 10:
                points += 10
        
        while points > 21 and n_ace > 0:
            n_ace -= 1
            points -= 10
        
        self.points[p_idx] = points
        
        return points

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