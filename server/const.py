import blackjack_pb2

class Action:
    DRAW = blackjack_pb2.Action.ActionNum.DRAW
    STAND = blackjack_pb2.Action.ActionNum.STAND
class Status:
    OKAY = blackjack_pb2.Points.StatusNum.OKAY
    BOOM = blackjack_pb2.Points.StatusNum.BOOM