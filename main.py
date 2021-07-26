import cv2
import pyrealsense2
import mediapipe as mp
import tw
import toggle

tog = toggle.Toggle()

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(2)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False

        result = holistic.process(img)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img.flags.writeable = True

        try:
            landmarks = result.pose_landmarks.landmark
            if (tog.patient_left == False):
                # tw.send_message("The patient has come back to the room!")
                print("Patient has to the room")
                tog.patient_left = True

            if landmarks[0].y > 0.68 and tog.patient_off_bed == True:
                tog.patient_off_bed = False
                # tw.send_message("EMERGENCY! The Patient has felt off the bed !!! SOS")
                print(landmarks[0])

        except:
            pass

        if result.pose_landmarks == None and tog.patient_left == True:
            tog.patient_left = False
            # tw.send_message("The patient has left the room!")
            print("Patient left the room")
        #     tw.send_message("Your left hand is missing")
            # tog.let_switch()

        # mp_drawing.draw_landmarks(img, result.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        # mp_drawing.draw_landmarks(img, result.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        # mp_drawing.draw_landmarks(img, result.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(img, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        cv2.imshow('MediaPipe Feed', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
