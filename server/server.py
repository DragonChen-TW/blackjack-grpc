import grpc

import blackjack_pb2
import blackjack_pb2_grpc

from concurrent.futures import ThreadPoolExecutor
# 
from card import Card, create_all_cards

class ActionNum:
    DRAW = blackjack_pb2.Action.ActionNum.DRAW
    STAND = blackjack_pb2.Action.ActionNum.STAND

class BlackJackService(blackjack_pb2_grpc.BlackJackService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards = create_all_cards()
    
    def SendAction(self, request, context):
        # hello_grpc_pb2.HelloReply(msg=f'Hello, {request.name}')
        # sample one card out
        if request.action_num == ActionNum.DRAW:
            card = self.cards[0]
            self.cards = self.cards[1:]
        else:
            card = Card('N', 0)

        return blackjack_pb2.Card(flow=card.flow, point=card.point)

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
