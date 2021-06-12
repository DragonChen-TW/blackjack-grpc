import sys
sys.path.append('../server')
import grpc
import time
from termcolor import colored

import blackjack_pb2
import blackjack_pb2_grpc
# 
from card import Card
from const import Action, Status

def test():
    with grpc.insecure_channel('127.0.0.1:30051') as channel:
        stub = blackjack_pb2_grpc.BlackJackServiceStub(channel)
        
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


def cal_points(stub, p_idx):
    cal = stub.CalPoint(blackjack_pb2.pIdx(p_idx=p_idx))
    return cal.points

def run():
    with grpc.insecure_channel('127.0.0.1:30051') as channel:
        stub = blackjack_pb2_grpc.BlackJackServiceStub(channel)

        print('Welcome to blackjack-grpc 2020 version')
        print('I am the creator DragonChen')
        print('Please input action character:')
        print('\t[d]: draw\t[s]: stand')
        print('-' * 20)

        # p_idx = int(input('Please pick up player num: '))
        p_idx = 0

        while cal_points(stub, p_idx) <= 21:
            act = input('Please choose action: ')
            if act == 'D' or act == 'd':
                req = blackjack_pb2.Action(
                    action_num=Action.DRAW,
                    p_idx=0
                )
                response = stub.SendAction(req)

                card = Card.from_grpc(response)
                print('\tYou got card', card)
                print(colored(f'\tTotal point is {cal_points(stub, p_idx)}', 'green'))
                print('-' * 20)
            elif act == 'S' or act == 's':
                req = blackjack_pb2.Action(
                    action_num=Action.STAND,
                    p_idx=0
                )
                response = stub.SendAction(req)
                print('f', Card.from_grpc(response))
                break

        total = stub.CalPoint(
            blackjack_pb2.pIdx(p_idx=0)
        )
        points, status = total.points, total.status_num
        print('-' * 10, points, status, '-' * 10)

if __name__ == "__main__":
    run()
