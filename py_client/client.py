import sys
sys.path.append('../server')
import grpc
import time

import blackjack_pb2
import blackjack_pb2_grpc
# 
from card import Card
from const import Action, Status

def run():
    # with grpc.insecure_channel('localhost:50051') as channel:
    with grpc.insecure_channel('127.0.0.1:30051') as channel:
        stub = blackjack_pb2_grpc.BlackJackServiceStub(channel)

        # print(ActionNum.DRAW)
        
        for _ in range(2):
            req = blackjack_pb2.Action(
                action_num=Action.DRAW,
                p_idx=0
            )
            response = stub.SendAction(req)

            card = Card.from_grpc(response)
            print('card', card)
    
        req = blackjack_pb2.Action(
            action_num=Action.STAND,
            p_idx=0
        )
        response = stub.SendAction(req)
        print('f', Card.from_grpc(response))

        total = stub.CalPoint(
            blackjack_pb2.pIdx(p_idx=0)
        )
        print('success')
        points, status = total.points, total.status_num
        print('-' * 10, points, status, '-' * 10)
        

if __name__ == "__main__":
    run()
