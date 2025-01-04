import cv2
import mediapipe as mp
import random
import time
import pyttsx3

 



# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

# Function to detect gestures
def detect_gesture(landmarks):
    if len(landmarks) < 21:  # Mediapipe hands provide 21 landmarks
        return "Unknown"

    thumb_up = landmarks[4][1] < landmarks[3][1]  # Thumb tip left of IP
    index_up = landmarks[8][2] < landmarks[6][2]  # Index tip above PIP
    middle_up = landmarks[12][2] < landmarks[10][2]  # Middle tip above PIP
    ring_up = landmarks[16][2] < landmarks[14][2]  # Ring tip above PIP
    pinky_up = landmarks[20][2] < landmarks[18][2]  # Pinky tip above PIP

    if thumb_up and index_up and not middle_up and not ring_up and not pinky_up:
        return "Gun"
    elif index_up and middle_up and not thumb_up and not ring_up and not pinky_up:
        return "Snake"
    elif thumb_up and index_up and middle_up and ring_up and pinky_up:
        return "Water"
    else:
        return "Unknown"

# Initialize the game choices and mapping
inputdic = {
    "g": -1,  # Gun
    "w": 0,   # Water
    "s": 1 ,   # Snake
    "u" : 2     # unknown
          
}

reverseinputdic = {
    -1: "Gun", 0: "Water", 1: "Snake"
}

# Start Video Capture
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Camera not accessible! Check permissions or connection.")
else:
    print("Initializing Snake-Water-Gun game...\nShow your hand to play!")

    start_time = time.time()  # Track time for 5 seconds
    user_choice = "Unknown"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        # Convert frame to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Convert landmarks to a list of (x, y, z)
                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

                # Call the gesture detection function
                user_choice = detect_gesture(landmarks)

        # Show the frame and the detected gesture
        cv2.putText(frame, f"Your Gesture: {user_choice}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Snake-Water-Gun Game", frame)

        # Check if 5 seconds have passed
        if time.time() - start_time >= 4:
            print(f"Game Result: {user_choice}")
            cv2.putText(frame, f"Game Result: {user_choice}", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Computer random choice (1 = Snake, 0 = Water, -1 = Gun)
            computer = random.choice([1, 0, -1])
            print(f"COMPUTER CHOOSE: {reverseinputdic[computer]}")

            # Display the computer choice
            cv2.putText(frame, f"Computer Choice: {reverseinputdic[computer]}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Game result calculation
            finput = inputdic.get(user_choice[0].lower())  # Convert user input to the corresponding value
            if (finput==2):
                engine = pyttsx3.init() 
                rate = engine.getProperty('rate')
                engine.setProperty('rate', rate - 50)
                # time.sleep(0.1)
                engine.say("Invalid input. Please choose 'g' for Gun, 'w' for Water, or 's' for Snake.") 
                engine.runAndWait()
                print("Invalid input. Please choose 'g' for Gun, 'w' for Water, or 's' for Snake.")
            else:
                if computer == finput:
                    
                    engine = pyttsx3.init() 
                    rate = engine.getProperty('rate')
                    engine.setProperty('rate', rate - 50)
                    # time.sleep(0.1)
                    engine.say("It's a draw") 
                    engine.runAndWait()
                    print("It's a draw")
                else:
                    if computer == 1 and finput == 0:
                        engine = pyttsx3.init() 
                        rate = engine.getProperty('rate')
                        engine.setProperty('rate', rate - 50)
                        # time.sleep(0.1)
                        engine.say("You Lose.......Better luck next time") 
                        engine.runAndWait()
                        print("You Lose.......Better luck next time")
                    elif computer == 1 and finput == -1:
                        engine = pyttsx3.init() 
                        rate = engine.getProperty('rate')
                        engine.setProperty('rate', rate - 50)
                        # time.sleep(0.1)
                        engine.say("You Win.......One more match??") 
                        engine.runAndWait()
                        print("You Win.......One more match??")
                    elif computer == 0 and finput == -1:
                        engine = pyttsx3.init()
                        rate = engine.getProperty('rate')
                        engine.setProperty('rate', rate - 50) 
                        # time.sleep(0.1)
                        engine.say("You Lose.......Better luck next time") 
                        engine.runAndWait()
                        print("You Lose.......Better luck next time")
                    elif computer == 0 and finput == 1:
                        engine = pyttsx3.init()
                        rate = engine.getProperty('rate')
                        engine.setProperty('rate', rate - 50) 
                        # time.sleep(0.1)
                        engine.say("You Win.......One more match??") 
                        engine.runAndWait()
                        print("You Win.......One more match??")
                    elif computer == -1 and finput == 0:
                        engine = pyttsx3.init()
                        rate = engine.getProperty('rate')
                        engine.setProperty('rate', rate - 50)
                        # time.sleep(0.1) 
                        engine.say("You Win.......One more match??") 
                        engine.runAndWait()
                        print("You Win.......One more match??")
                    elif computer == -1 and finput == 1:
                        engine = pyttsx3.init()
                        rate = engine.getProperty('rate')
                        engine.setProperty('rate', rate - 50)
                        # time.sleep(0.1) 
                        engine.say("You Lose.......Better luck next time") 
                        engine.runAndWait()
                        print("You Lose.......Better luck next time")
            
            cv2.imshow("Snake-Water-Gun Game", frame)
            break

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Game exited by user.")
            break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
