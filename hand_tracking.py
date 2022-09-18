import cv2
import mediapipe as mp
import time



class handDetecter():
    def __init__(self, mode=False, hands_max=2, model_complexity = 1,detection_con = 0.5, track_con = 0.5) -> None:
        self.mode = mode
        self.hands_max = hands_max
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.hands_max, self.model_complexity  ,self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hand(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if(self.results.multi_hand_landmarks):
            for hand_landmarks in self.results.multi_hand_landmarks:
                if (draw):
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
    def positions(self, img, id_h=0, draw = True):
        land_mk = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[id_h]
            for id_hand, landm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(landm.x*w), int(landm.y*h)
                land_mk.append([id_hand, cx,cy])

                if (draw):
                    cv2.circle(img, (cx,cy), 10, (0,255,0), cv2.FILLED)

        return land_mk


def main():
    video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    p_time = 0
    c_time = 0
    detector = handDetecter()

    while video_cap.isOpened():
        succes, img = video_cap.read()
        detector.find_hand(img)
        c_time = time.time()
        fps = 1//(c_time - p_time)
        p_time = c_time

        cv2.putText(img, f"FPS: {str(fps)}", (7,30), cv2.FONT_HERSHEY_PLAIN, 2, (0,250,0), 3)

        if (cv2.waitKey(10) == ord ('q')):
            break

        cv2.imshow("Detector de Mano", img)

    video_cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()