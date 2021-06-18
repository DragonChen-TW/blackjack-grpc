import grpc

import blackjack_pb2
import blackjack_pb2_grpc

from concurrent.futures import ThreadPoolExecutor
# 
from game import Game
from card import Card
from const import Action, Status

class BlackJackService(blackjack_pb2_grpc.BlackJackService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game(n_players=2)
    
    def SendAction(self, request, context):
        print('send action')
        p_idx = request.p_idx

        # sample one card out
        if request.action_num == Action.DRAW:
            card = self.game.draw_one_card(p_idx)
        else:
            print(f'Player {p_idx} draw')
            card = Card('N', 0)
            self.game.next_player()

        return blackjack_pb2.Card(flow=card.flow, point=card.point)
    
    def CheckStatus(self, request, context):
        p_idx = request.p_idx

        points = self.game.cal_point(p_idx)
        if self.game.now_player >= self.game.n_players:
            status = Status.END
        elif p_idx != self.game.now_player:
            status = Status.WAIT
        else:
            if points <= 21:
                status = Status.OKAY
            else:
                status = Status.BOOM
        return blackjack_pb2.Status(points=points, status_num=status)
    
    def GetHistory(self, request, context):
        p_idx = request.p_idx

        history = self.game.player_cards[p_idx]
        for c in history:
            yield blackjack_pb2.Card(flow=c.flow, point=c.point)

def serve():
    # using ThreadPool to build server
    server = grpc.server(ThreadPoolExecutor(5))
    # add service(protocol) into server
    blackjack_pb2_grpc.add_BlackJackServiceServicer_to_server(
        BlackJackService(), server)
    server.add_insecure_port('[::]:30051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
