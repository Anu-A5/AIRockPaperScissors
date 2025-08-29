import tensorflow as tf
import numpy as np
import random

#USE INHERITENCE
class rps_5BHNN_gen:
    def __init__(self, Throw_Enum, Throw_State):
        self.output        = Throw_Enum
        self.throw_history = []
        self.win_history   = []
        self.name          = "RPS_5BHNN"
        self.input_size    = 5
        self.curr_inputs   = []
        self.weights       = []
        self.num_hidden    = self.input_size 
        self.throw_state   = Throw_State

        tf.keras.utils.disable_interactive_logging()

        tf.random.set_seed(88)#change to systm time

        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(self.input_size, activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(3, activation = 'softmax')) #determines what the user will play next

        opt = tf.keras.optimizers.Adam(learning_rate=0.1)
            
        self.model.compile(optimizer=opt,loss=tf.keras.losses.SparseCategoricalCrossentropy())

    def update_inputs(self, input_array):
        if(len(input_array) != self.input_size):
            print("ERROR: INPUT ARRAY INCORRECT SIZE")
            return False
        else:
            self.curr_inputs = input_array
            for i in range(len(self.curr_inputs)):
                self.curr_inputs[i] = self.curr_inputs[i] - 1

    def winning_move(self, next_throw):
        if(next_throw == self.output.ROCK):
            return self.output.PAPER
        elif(next_throw == self.output.PAPER):
            return self.output.SCISSORS
        elif(next_throw == self.output.SCISSORS):
            return self.output.ROCK


    def gen_output(self):
        prediction = self.model.predict([self.curr_inputs])
        
        next_move = []
        max_val   = prediction[0].max()

        for i in range(len(prediction[0])):
            if(prediction[0][i] == max_val):
                next_move.append(i)
   
        selected_move = random.choice(next_move)

        throw = self.winning_move(self.output(selected_move + 1))
        
        self.throw_history.append(throw)
        return throw

    def update_win_history(self, throw_outcome, next_move):
        if(len(self.throw_history) - 1 == len(self.win_history)):
            self.win_history.append(throw_outcome)

            self.model.fit([self.curr_inputs], [next_move.value - 1], epochs=1)

            return True

        else:
            print("ERROR: [5BHPNN] THROWS AND WIN INCORRECT SIZE")
            return False

    def get_heuristic(self):
        sum = 0

        for i in range(len(self.win_history)):
            sum += self.win_history[i].value

        return sum/len(self.win_history)



class rps_5BH_P_NN_gen:
    def __init__(self, Throw_Enum, Throw_State):
        self.output        = Throw_Enum
        self.throw_history = []
        self.win_history   = []
        self.name          = "RPS_5BH_P_NN"
        self.input_size    = 5
        self.curr_inputs   = []
        self.weights       = []
        self.num_hidden    = self.input_size - 1
        self.throw_state   = Throw_State

        tf.keras.utils.disable_interactive_logging()

        tf.random.set_seed(88)#change to systm time

        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(self.input_size, activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(self.input_size-1, activation=tf.nn.relu)) #CLEAN UP , USE INHERITENCE AND GLOBAL LEARNING RATE SETTING
        self.model.add(tf.keras.layers.Dense(3, activation = 'softmax')) #determines what the user will play next

        opt = tf.keras.optimizers.Adam(learning_rate=0.1)
            
        self.model.compile(optimizer=opt,loss=tf.keras.losses.SparseCategoricalCrossentropy())

    def update_inputs(self, input_array):
        if(len(input_array) != self.input_size):
            print("ERROR: INPUT ARRAY INCORRECT SIZE")
            return False
        else:
            self.curr_inputs = input_array
            for i in range(len(self.curr_inputs)):
                self.curr_inputs[i] = self.curr_inputs[i] - 1

    def winning_move(self, next_throw):
        if(next_throw == self.output.ROCK):
            return self.output.PAPER
        elif(next_throw == self.output.PAPER):
            return self.output.SCISSORS
        elif(next_throw == self.output.SCISSORS):
            return self.output.ROCK


    def gen_output(self):
        prediction = self.model.predict([self.curr_inputs])
        
        next_move = []
        max_val   = prediction[0].max()

        for i in range(len(prediction[0])):
            if(prediction[0][i] == max_val):
                next_move.append(i)
   
        selected_move = random.choice(next_move)

        throw = self.winning_move(self.output(selected_move + 1))

        self.throw_history.append(throw)
        return throw

    def update_win_history(self, throw_outcome, next_move):
        if(len(self.throw_history) - 1 == len(self.win_history)):
            self.win_history.append(throw_outcome)

            self.model.fit([self.curr_inputs], [next_move.value - 1], epochs=1)

            return True

        else:
            print("ERROR: [5BHPNN] THROWS AND WIN INCORRECT SIZE")
            return False

    def get_heuristic(self):
        sum = 0

        for i in range(len(self.win_history)):
            sum += self.win_history[i].value

        return sum/len(self.win_history)

