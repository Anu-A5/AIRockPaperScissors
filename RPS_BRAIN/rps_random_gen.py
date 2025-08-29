import random

#Randomly plays a move
class rps_random_gen:
    def __init__(self, Throw_Enum):
        self.output        = Throw_Enum
        self.throw_history = []
        self.win_history   = []
        self.name          = "RPS_RANDOM_GEN"

    def gen_output(self):
        throw              = self.output(random.randint(1,3))
        self.throw_history.append(throw)
        return throw

    def update_win_history(self, throw_outcome):
        if(len(self.throw_history) - 1 == len(self.win_history)):
            self.win_history.append(throw_outcome)
            return True

        else:
            print("ERROR: [RANDOM] THROWS AND WIN INCORRECT SIZE")
            return False

    def get_heuristic(self):
        sum = 0

        for i in range(len(self.win_history)):
            sum += self.win_history[i].value

        return sum/len(self.win_history)