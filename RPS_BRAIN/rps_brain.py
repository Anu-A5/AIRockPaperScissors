from rps_random_gen import rps_random_gen
from rps_freq_gen   import rps_freq_gen
from rps_3BH_NN_gen import *
from rps_5BH_NN_gen import *
from rps_NETWORK    import rps_network

from enum import Enum
import random

import cv2
import mediapipe

import threading
import multiprocessing
import socket 
import select
import time
import sys


class Throw(Enum):
    UNDEFINED = 0
    ROCK      = 1
    PAPER     = 2
    SCISSORS  = 3

class Throw_State(Enum):
    UNDEFINED = -10
    LOSE      = -1
    DRAW      = 0
    WIN       = 1

class Game:

    def __init__(self):
        #Available Models:6
        #1.Random Number Generator
        #2.Most Frequent Play
        #3.Neural Network Looking 3 moves behind
        #4.Neural Network Looking 3 moves behind with hidden layer
        #4.Neural Network Looking 5 moves behind
        #5.Neural Network Looking 5 moves behind with hidden layer
        #6. -Neural Network Looking 7 moves behind-
        #8. -Recurrent Neural Network looking 5 moves behind-
        #9. -Recurrent Neural Network looking 7 moves behind-

        #Are Convolutional Neural Networks appropriate? We are looking at patterns in pattern history over a fixed history
        #Outline the benefits and draw backs of each model. 

        #IMPORTANT TO NOTE: DATA IS NOT INDEPENDENT, MEANING GAUSSIAN OR LINEAR MODELS MAY NOT BE APPROPRIATE.

        random.seed(88)

        #Add a parent class to these models, include hyper parameter values that can be overwritten

        self.random_gen = rps_random_gen(Throw)
        self.freq_gen   = rps_freq_gen(Throw, History_Depth=6)
        self.nn3bh      = rps_3BHNN_gen(Throw, Throw_State)
        self.nn3bh_p    = rps_3BH_P_NN_gen(Throw, Throw_State)
        self.nn5bh      = rps_5BHNN_gen(Throw, Throw_State)
        self.nn5bh_p    = rps_5BH_P_NN_gen(Throw, Throw_State)

        self.user_history     = []

        self.Throws           = {}
        self.available_model_heuristics = {}
        self.model_heuristics = {self.random_gen:-1, self.freq_gen:-1, self.nn3bh:-1, self.nn5bh:-1, self.nn3bh_p:-1, self.nn5bh_p:-1}  
        

        self.game_no    = 0
        self.wins       = 0

    def game_logic(self, user_throw, comp_throw):
        if(user_throw == comp_throw):
            return Throw_State.DRAW
        elif((user_throw == Throw.ROCK) and (comp_throw == Throw.PAPER)):
            return Throw_State.WIN
        elif((user_throw == Throw.PAPER) and (comp_throw == Throw.SCISSORS)):
            return Throw_State.WIN
        elif((user_throw == Throw.SCISSORS) and (comp_throw == Throw.ROCK)):
            return Throw_State.WIN
        elif((comp_throw == Throw.ROCK) and (user_throw == Throw.PAPER)):
            return Throw_State.LOSE
        elif((comp_throw == Throw.PAPER) and (user_throw == Throw.SCISSORS)):
            return Throw_State.LOSE
        elif((comp_throw == Throw.SCISSORS) and (user_throw == Throw.ROCK)):
            return Throw_State.LOSE
        else:
            return Throw_State.UNDEFINED

    def winning_move(self, user_throw):
        #[ROCK, PAPER, SCISSORS]
        if(user_throw == Throw.ROCK):
            return [0,1,0]
        elif(user_throw == Throw.PAPER):
            return [0,0,1]
        elif(user_throw == Throw.SCISSORS):
            return [1,0,0]

    #Convert an array of enumerated types to an array of integers 
    def convert_state_to_int(self, throw_states):
        int_states = []

        for i in throw_states:
            int_states.append(i.value)

        return int_states

    #Generate the computers throw
    def gen_comp_output(self):

        #computer throws depending on the model used
        self.Throws = {}
        self.available_model_heuristics = {}
        
        #First throw is always random
        #RPS_RANDOM_GEN
        self.Throws[self.random_gen] = self.random_gen.gen_output()
        self.available_model_heuristics[self.random_gen]     = self.model_heuristics[self.random_gen]

        #Second throw we can emply more intuition
        if(self.game_no >= 1):
            #updates appropriate inputs for necessary models - Freq_model
            self.freq_gen.update_user_history(self.user_history[(-1*self.freq_gen.history_depth):])
            self.Throws[self.freq_gen]   = self.freq_gen.gen_output()
            self.available_model_heuristics[self.freq_gen]   = self.model_heuristics[self.freq_gen]

        if(self.game_no >= 4): # enable 3BHNNs
            self.nn3bh.update_inputs(self.convert_state_to_int(self.user_history[-3:]))
            self.Throws[self.nn3bh] = self.nn3bh.gen_output()
            self.available_model_heuristics[self.nn3bh]      = self.model_heuristics[self.nn3bh]

            self.nn3bh_p.update_inputs(self.convert_state_to_int(self.user_history[-3:]))
            self.Throws[self.nn3bh_p] = self.nn3bh_p.gen_output()
            self.available_model_heuristics[self.nn3bh_p]      = self.model_heuristics[self.nn3bh_p]
            
        if(self.game_no >= 6):# enable 5BHNNs
            self.nn5bh.update_inputs(self.convert_state_to_int(self.user_history[-5:]))
            self.Throws[self.nn5bh] = self.nn5bh.gen_output()
            self.available_model_heuristics[self.nn5bh]      = self.model_heuristics[self.nn5bh]

            self.nn5bh_p.update_inputs(self.convert_state_to_int(self.user_history[-5:]))
            self.Throws[self.nn5bh_p] = self.nn5bh_p.gen_output()
            self.available_model_heuristics[self.nn5bh_p]      = self.model_heuristics[self.nn5bh_p]

        if(self.game_no >= 8):# enable 7BHNNs
            pass

        #decide which model to pick based on heuristics, if the same, pick randomly -------------------------------
        best_models = []

        #get heuristics of available models
        max_val     = max(set(self.available_model_heuristics.values()))

        for key,value in self.available_model_heuristics.items():
            if(value == max_val):
                best_models.append(key)
        
        selected_model = random.choice(best_models)

        print(f"game_no: {self.game_no} selected_model: {selected_model.name}")

        return Throw(self.Throws[selected_model]).value

    def set_user_throw(self, user_throw):
        user_throw = Throw(user_throw)
        self.user_history.append(user_throw)

        #run through all available models and check whether they won drew or lost ---------------------------------
        for model, throw in self.Throws.items():
            if((model.name == "RPS_3BHNN") or (model.name == "RPS_5BHNN") or (model.name == "RPS_3BH_P_NN") or (model.name == "RPS_5BH_P_NN")):
                model.update_win_history(self.game_logic(user_throw, throw), user_throw)
            else:
                model.update_win_history(self.game_logic(user_throw, throw))

        #update heuristics
        for models in self.Throws.keys():
            self.model_heuristics[models] = models.get_heuristic()

        print(self.model_heuristics)

    def update_game_num(self):
        self.game_no += 1


    def run_game(self, num_games):
        # Available Model Theory

        #In order
        #1. RANDOM                          (0 history)
        #2. RANDOM + FREQUENCY              (1 history)
        #3. RANDOM + FREQUENCY              (2 history)
        #4. RANDOM + FREQUENCY              (3 history) -> 3BH NN train and predict for move #4
        #5. RANDOM + FREQUENCY + 3BHNN      (4 history) 
        #6. RANDOM + FREQUENCY + 3BHNN      (5 history) -> 5BH NN train and predict for move #6
        # .
        # .
        # .

        pass

            
    def reset(self):
        self.game_no = 0
        self.wins    = 0
        self.user_history     = []
        self.model_heuristics = {self.random_gen:-1, self.freq_gen:-1, self.nn3bh:-1, self.nn5bh:-1, self.nn3bh_p:-1, self.nn5bh_p:-1}  



def get_finger_status(hands_module, hand_landmarks, finger_name):
    finger_id_map = {'INDEX': 8, 'MIDDLE': 12, 'RING': 16, 'PINKY': 20}

    finger_tip_y = hand_landmarks.landmark[finger_id_map[finger_name]].y
    finger_dip_y = hand_landmarks.landmark[finger_id_map[finger_name] - 1].y
    finger_mcp_y = hand_landmarks.landmark[finger_id_map[finger_name] - 2].y

    return finger_tip_y < finger_mcp_y


def get_thumb_status(hands_module, hand_landmarks):
    thumb_tip_x = hand_landmarks.landmark[hands_module.HandLandmark.THUMB_TIP].x
    thumb_mcp_x = hand_landmarks.landmark[hands_module.HandLandmark.THUMB_TIP - 2].x
    thumb_ip_x = hand_landmarks.landmark[hands_module.HandLandmark.THUMB_TIP - 1].x

    return thumb_tip_x > thumb_ip_x > thumb_mcp_x

def video_capture():#Turn to class
    
    hands_module = mediapipe.solutions.hands
    capture = cv2.VideoCapture(1)

    with hands_module.Hands(static_image_mode=False, min_detection_confidence=0.65,
                            min_tracking_confidence=0.4, max_num_hands=1) as hands:
        while (True):
            ret, frame = capture.read()
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            move = 0
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    current_state = ""
                    thumb_status = get_thumb_status(hands_module, hand_landmarks)
                    current_state += "1" if thumb_status else "0"

                    index_status = get_finger_status(hands_module, hand_landmarks, 'INDEX')
                    current_state += "1" if index_status else "0"

                    middle_status = get_finger_status(hands_module, hand_landmarks, 'MIDDLE')
                    current_state += "1" if middle_status else "0"

                    ring_status = get_finger_status(hands_module, hand_landmarks, 'RING')
                    current_state += "1" if ring_status else "0"

                    pinky_status = get_finger_status(hands_module, hand_landmarks, 'PINKY')
                    current_state += "1" if pinky_status else "0"

                    if current_state == "00000":
                        move = 1
                        captured_move = move
                    elif current_state == "11111":
                        move = 2
                        captured_move = move
                    elif current_state == "01100":
                        move = 3
                        captured_move = move
                    else:
                        move = 0
            
            cv2.waitKey(500)



  

if __name__ == "__main__":
    #write to serial port
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT =  7000  # Port to listen on (non-privileged ports are > 1023) 
    
    game = Game()

    #video_capture()
    capture = cv2.VideoCapture(0)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data_in = None

    # packet format
    # mode(1-4) - Throw/Result

    print("Waiting...")
    while True:
        ready, w, e = select.select([s], [], [], 3600)
        ss = ready[0]

        if(ss):
            data_in = ss.recv(1024).decode()
            if not data_in: sys.exit(0)
            data_in = int(data_in)
            print(data_in)

            if(data_in == 1): #send user motion stream
                ss.settimeout(0.5)
     
                #get user hand
                hands_module = mediapipe.solutions.hands

                user_hands = []

                with hands_module.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.4, max_num_hands=1) as hands:

                    while (True):
                        ret, frame = capture.read()
                        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        cv2.imshow("test", frame)#-> maybe draw landmarks open simage at bottom right of screen
                        move = 0
                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:

                                current_state = ""
                                thumb_status = get_thumb_status(hands_module, hand_landmarks)
                                current_state += "1" if thumb_status else "0"

                                index_status = get_finger_status(hands_module, hand_landmarks, 'INDEX')
                                current_state += "1" if index_status else "0"

                                middle_status = get_finger_status(hands_module, hand_landmarks, 'MIDDLE')
                                current_state += "1" if middle_status else "0"

                                ring_status = get_finger_status(hands_module, hand_landmarks, 'RING')
                                current_state += "1" if ring_status else "0"

                                pinky_status = get_finger_status(hands_module, hand_landmarks, 'PINKY')
                                current_state += "1" if pinky_status else "0"

                                if current_state == "00000":
                                    move = 1
                                    user_hands.append(move)
                                elif current_state == "11111":
                                    move = 2
                                    user_hands.append(move)
                                elif current_state == "01100":
                                    move = 3
                                    user_hands.append(move)
                                else:
                                    move = 0

                        user_motion_pred = move
                        print(user_motion_pred)
                        ss.send((f"1{user_motion_pred}" + "\n").encode("utf-8"))

                        if cv2.waitKey(10) & 0xFF==ord('q'):
                            break
                        try:
                            if(int(ss.recv(1024).decode()) == 2):
                                print("okay")
                                s.settimeout(3600)

                                #get max of last 3 entries
                                user_throw_pred = max(set(user_hands[-3:]), key=user_hands.count)
                                print(user_hands)
                                print(user_throw_pred)
                                game.set_user_throw(user_throw_pred)
                                game.update_game_num()
                                ss.send((f"2{user_throw_pred}"  + "\n").encode("utf-8"))

                                break
                        except:
                            pass


            elif(data_in == 2): #send user throw
                ss.send((f"2{9}"  + "\n").encode("utf-8"))
                
            elif(data_in == 3): #send comp throw ->must happen first

                #RPS GAME COMP OUT
                #comp_throw:       1->rock, 2->paper, 3->scissors
                comp_throw = game.gen_comp_output()
                ss.send((f"3{comp_throw}"       + "\n").encode("utf-8"))
                
            elif(data_in == 4): #reset game
                game.reset()
            
            else:
                pass
    
    capture.release()
    s.close()