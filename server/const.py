import blackjack_pb2

class Action:
    DRAW = blackjack_pb2.Action.ActionNum.DRAW
    STAND = blackjack_pb2.Action.ActionNum.STAND
class Status:
    WAIT = blackjack_pb2.Status.StatusNum.WAIT
    OKAY = blackjack_pb2.Status.StatusNum.OKAY
    BOOM = blackjack_pb2.Status.StatusNum.BOOM
    END = blackjack_pb2.Status.StatusNum.END