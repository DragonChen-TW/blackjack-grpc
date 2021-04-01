import random

class Card:
    def __init__(self, flow, p):
        self.flow = flow
        self.point = p
    
    def __repr__(self):
        return f'C({self.flow} {self.point})'
    
    @classmethod
    def from_grpc(cls, response):
        return cls(response.flow, response.point)

def create_all_cards():
    def cards_gen_loop():
        for f in ['S', 'H', 'D', 'C']:
            for p in range(1, 14):
                yield Card(f, p)
    cards = list(cards_gen_loop())
    cards = random.sample(cards, len(cards))

    # print(cards)
    return cards

if __name__ == '__main__':
    create_all_cards()