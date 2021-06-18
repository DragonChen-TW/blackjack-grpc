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

def cal_points(stub, p_idx):
    res = stub.CheckStatus(blackjack_pb2.pIdx(p_idx=p_idx))
    return res.points

def get_status(stub, p_idx):
    res = stub.CheckStatus(blackjack_pb2.pIdx(p_idx=p_idx))
    # print('s', res.status_num)
    return res.status_num

def print_history(stub, p_idx):
    hist = stub.GetHistory(blackjack_pb2.pIdx(p_idx=p_idx))
    cards = [Card.from_grpc(h) for h in hist]
    
    print('-' * 20)
    # print(' '.join(['{:>2}'.format(c.flow) for c in cards]))
    # print(' '.join(['{:2}'.format(c.point) for c in cards]))
    print(' '.join([str(c) for c in cards]))
    print('-' * 20)

def run(p_idx=None):
    with grpc.insecure_channel('127.0.0.1:30051') as channel:
        stub = blackjack_pb2_grpc.BlackJackServiceStub(channel)

        print('Welcome to blackjack-grpc 2020 version')
        print('I am the creator DragonChen')
        print('You can input these action characters to play:')
        print('\t[d]: draw\t[s]: stand')
        print('=' * 20)

        if p_idx == None:
            p_idx = int(input('Please pick up player num: '))
        print(f'You are player {p_idx}')

        if get_status(stub, p_idx) == Status.WAIT:
            print('It is not your turn now.')
        while get_status(stub, p_idx) == Status.WAIT:
            time.sleep(1)

        # Your turn
        while get_status(stub, p_idx) == Status.OKAY and cal_points(stub, p_idx) <= 21:
            act = input('Please choose action: ')
            if act == 'D' or act == 'd':
                req = blackjack_pb2.Action(
                    action_num=Action.DRAW,
                    p_idx=p_idx
                )
                response = stub.SendAction(req)
                card = Card.from_grpc(response)

                print('\tYou got card', card)
                print_history(stub, p_idx)
                print(colored(f'\tTotal point is {cal_points(stub, p_idx)}', 'green'))
                print('=' * 20)
            elif act == 'S' or act == 's':
                req = blackjack_pb2.Action(
                    action_num=Action.STAND,
                    p_idx=p_idx
                )
                response = stub.SendAction(req)
                card = Card.from_grpc(response)
                break
        
        # Game End
        if get_status(stub, p_idx) != Status.END:
            print('Wait the game end')
        while get_status(stub, p_idx) != Status.END:
            time.sleep(1)
        total = stub.CheckStatus(
            blackjack_pb2.pIdx(p_idx=p_idx)
        )
        points, status = total.points, total.status_num
        print('=' * 10, 'You got', points, 'status:', status, '=' * 10)

if __name__ == "__main__":
    run(int(sys.argv[1]))
