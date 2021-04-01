import sys
sys.path.append('../server')
import grpc
import time

import blackjack_pb2
import blackjack_pb2_grpc
# 
from card import Card

class ActionNum:
    DRAW = blackjack_pb2.Action.ActionNum.DRAW
    STAND = blackjack_pb2.Action.ActionNum.STAND

def run():
    # with grpc.insecure_channel('localhost:50051') as channel:
    with grpc.insecure_channel('127.0.0.1:30051') as channel:
        stub = blackjack_pb2_grpc.BlackJackServiceStub(channel)

        # print(ActionNum.DRAW)
        
        req = blackjack_pb2.Action(action_num=ActionNum.DRAW)
        response = stub.SendAction(req)
        # print(response, response.point)
        print('f', response.flow, response.point)

        card = Card.from_grpc(response)
        print('card', card)
    
        req = blackjack_pb2.Action(action_num=ActionNum.STAND)
        response = stub.SendAction(req)
        print('f', response.flow, response.point)
        

if __name__ == "__main__":
    run()
