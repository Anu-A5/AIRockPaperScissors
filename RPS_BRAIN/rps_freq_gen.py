#Plays against the users most frequent choice o last x moves

class rps_freq_gen:
    def __init__(self, Throw_Enum, History_Depth):
        self.output             = Throw_Enum
        self.throw_history      = []
        self.win_history        = []
        self.user_history       = []
        self.history_depth      = History_Depth 
        self.name               = "RPS_FREQ_GEN"

    def gen_output(self):
        freq_user_throw = max(set(self.user_history), key=self.user_history.count)

        if(freq_user_throw   == self.output.ROCK):
            throw = self.output.PAPER
        elif(freq_user_throw == self.output.PAPER):
            throw = self.output.SCISSORS
        elif(freq_user_throw == self.output.SCISSORS):
            throw = self.output.ROCK
        else:
            throw = self.output.UNDEFINED

        self.throw_history.append(throw)
        return throw

    def update_win_history(self, throw_outcome):
        if(len(self.throw_history) - 1 == len(self.win_history)):
            self.win_history.append(throw_outcome)
            return True

        else:
            print("ERROR: THROWS AND WIN INCORRECT SIZE")
            return False

    def update_user_history(self, User_History):
        if(len(User_History) <= self.history_depth):
            self.user_history   = User_History
            return True

        else:
            print("ERROR: [FREQ] USER HISTORY INCORRECT SIZE")
            return False

    
    def get_heuristic(self):
        sum = 0

        for i in range(len(self.win_history)):
            sum += self.win_history[i].value

        return sum/len(self.win_history)