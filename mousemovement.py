import cv2
import mediapipe as mp
import time
# import autopy
import pyautogui
class handDetector():
    def __init__(self, mode = False, maxHands = 2,modelC=1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (640-cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmlist

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    detector = handDetector()
    upperPointOfHands=[4,8,12,16,20]
    print(pyautogui.size())
    counters=0
    xStart = 100
    yStart=100
    xEnd = 500
    yEnd = 400
    beforeAfter=[0,0]
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        img = cv2.flip(img,1)
        lmlist = detector.findPosition(img)
        if len(lmlist)!=0:
            beforeAfter[counters%2]=lmlist[8][2]
            fingers=[]
            for id in range(1,5):
                if lmlist[upperPointOfHands[id]][2]<lmlist[upperPointOfHands[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if int("".join(str(x) for x in fingers), 2)==8:
                print(lmlist[8][1],lmlist[8][2])
                if (lmlist[8][1]>=xStart and lmlist[8][1]<=xEnd
                    and lmlist[8][2]>=yStart and lmlist[8][2]<=yEnd):
                        cv2.rectangle(img,(xStart,yStart),(xEnd,yEnd),(255,0,0),3)
                        pyautogui.moveTo(1920-((lmlist[8][1]-xStart)*4.8), (lmlist[8][2]-yStart)*3.6,duration=0)
            if int("".join(str(x) for x in fingers), 2)==12:
                print(lmlist[8][1],lmlist[8][2])
                if (lmlist[8][1]>=xStart and lmlist[8][1]<=xEnd
                    and lmlist[8][2]>=yStart and lmlist[8][2]<=yEnd):
                        cv2.rectangle(img,(xStart,yStart),(xEnd,yEnd),(255,0,0),3)
                        pyautogui.click(1920-((lmlist[8][1]-xStart)*4.8), (lmlist[8][2]-yStart)*3.6,duration=0)
        counters+=1
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()