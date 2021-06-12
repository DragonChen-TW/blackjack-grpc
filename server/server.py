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
        self.game = Game(1)
    
    def SendAction(self, request, context):
        print('send action')
        p_idx = request.p_idx

        # hello_grpc_pb2.HelloReply(msg=f'Hello, {request.name}')
        # sample one card out
        if request.action_num == Action.DRAW:
            card = self.game.draw_one_card(p_idx)
        else:
            card = Card('N', 0)
        
        # calculate
        print('p {} get {} points'.format(
            p_idx, self.game.cal_point(p_idx)
        ))

        return blackjack_pb2.Card(flow=card.flow, point=card.point)
    
    def CalPoint(self, request, context):
        p_idx = request.p_idx

        points = self.game.cal_point(p_idx)
        if points <= 21:
            status = Status.OKAY
        else:
            status = Status.BOOM
        return blackjack_pb2.Points(points=points, status_num=status)

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
