
import threading
import socket 
import select
import time
import sys


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

def video_capture():

    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT =  7000  # Port to listen on (non-privileged ports are > 1023) 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    hands_module = mediapipe.solutions.hands
    capture = cv2.VideoCapture(0)

    with hands_module.Hands(static_image_mode=False, min_detection_confidence=0.8,
                            min_tracking_confidence=0.4, max_num_hands=1) as hands:
        while (True):

            ready, w, e = select.select([s], [], [], 300)
            ss = ready[0]

            if(ss):
                data_in = ss.recv(1024).decode()
                if not data_in: sys.exit(0)
                data_in = int(data_in)
                print(data_in)




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
