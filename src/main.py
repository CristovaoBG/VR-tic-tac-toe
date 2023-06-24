from cv2 import cv2
from matplotlib import pyplot as plt
import numpy as np
from imutils import rotate
import math
from tictactoe import Board
from copy import deepcopy


xTemplate = cv2.imread('../X.png',0)
#xTemplate = cv2.cvtColor(cv2.imread('X.png',0), cv2.COLOR_BGR2GRAY)
xTemplate90 = rotate(xTemplate, 90)
xTemplate7 = rotate(xTemplate, 7)
templateHeight, templateWidth = xTemplate.shape


#%%

board = Board("O","X")

templateThreshold = 0.45

hasX = [[False,False,False],[False,False,False],[False,False,False]]

captura = cv2.VideoCapture(0)
cap = captura.read()
orb = cv2.ORB_create()

camHeight, camWidth, camDepth = cap[1].shape

sift = cv2.SIFT_create()

#def draw_keypoint()
refTaken = False
freak = cv2.xfeatures2d.FREAK_create()

bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
lastQuadrants = []

circles = []

while(True):
    ret, frame = captura.read()
    kp = orb.detect(frame,None)
    outFrame = frame.copy()
    
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.medianBlur(frame,5)
    kp = sift.detect(frame,None) 
    
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

    if chr(k) == 'p':
        shot = frame.copy();
        keyPointsRef, descriptorRef = sift.detectAndCompute(frame,None)
        #kp = sift.detect(frame,None)
        refTaken = True
        
    if chr(k) == 'r':
        board = Board("O","X")
        hasX = [[False,False,False],[False,False,False],[False,False,False]]
        lastQuadrants = []
        circles = []
    
    if not refTaken:
        img = cv2.drawKeypoints(frame,kp,outFrame)
        cv2.imshow("Video", outFrame)   
        continue
    
    keyPoints, descriptor = sift.detectAndCompute(frame,None)
    matches = bf.match(descriptorRef,descriptor)

    if (len(matches) < 30):
        cv2.imshow("Video", frame)
        continue
    
    list_kp1 = np.float32([keyPointsRef[m.queryIdx].pt for m in matches]).reshape([-1,1,2])
    list_kp2 = np.float32([keyPoints[m.trainIdx].pt for m in matches]).reshape([-1,1,2])
    H, status = cv2.findHomography(list_kp2,list_kp1,cv2.RANSAC,7.0)
    
    #frameWarped = frame.copy()
    frameWarped = cv2.warpPerspective(frame,H,(len(frame[0]),len(frame)))
    Hinv, statusInv = cv2.findHomography(list_kp1,list_kp2,cv2.RANSAC,7.0)
    wrapedGray = cv2.cvtColor(frameWarped, cv2.COLOR_BGR2GRAY)



    #procura X na imagemp
    res = cv2.matchTemplate(wrapedGray, xTemplate,cv2.TM_CCOEFF_NORMED)
    res90 = cv2.matchTemplate(wrapedGray, xTemplate90,cv2.TM_CCOEFF_NORMED)
    res7 = cv2.matchTemplate(wrapedGray, xTemplate7,cv2.TM_CCOEFF_NORMED)
    cv2.imshow("window2",res)
    
    possibleLocations = np.column_stack(np.where(res>=templateThreshold))
    possibleLocations90 = np.column_stack(np.where(res90>=templateThreshold))
    possibleLocations7 = np.column_stack(np.where(res7>=templateThreshold))
    
    pl = np.concatenate((possibleLocations,possibleLocations7,possibleLocations90)) + (templateHeight/2,templateWidth/2)
    
    #transforma de posicao para quadrante
    quadrants = np.unique([(math.floor(y*3/camHeight),math.floor(x*3/camWidth)) for y,x in pl],axis=0)
    #filtra
    lastQuadrants.append(quadrants)
    if len(lastQuadrants) > 3:
        lastQuadrants = lastQuadrants[-3:]
        if (np.all(lastQuadrants==lastQuadrants[0])):
            #quadrante valido. verifica se ha mudanca
            changed = False
            for quady,quadx in quadrants:
                if hasX[quady][quadx] == False:
                    print(quady)
                    print(quadx)
                    changed == True
                    hasX[quady][quadx] = True
                    if board.isFree(quadx,quady):
                        board.place("X", quady, quadx)
                        print("placed x: {}, y: {}".format(quadx,quady))
                        state, posY, posX = board.nextMove()
                        print(posY,posX,state)
                        circles.append((posX,posY))
                        board.print()
                    break            

    #desenha circulos
    circlesImg = frameWarped.copy()
    circlesImg[True] = 1 #make all 1
    for p in circles:
        cv2.circle(circlesImg,(int((2*p[0]+1)*camWidth/6),int((2*p[1]+1)*camHeight/6)),40,(2,2,2),15)
    
    frameWarped = frameWarped*circlesImg

    #resolve inverso do inverso da imagem
    circlesImg = cv2.warpPerspective(circlesImg,np.linalg.pinv(H),(len(frame[0]),len(frame)))
    #remove parte preta criada pelo warped
    circlesImg[circlesImg == 0] = 1
    circlesImg[circlesImg == 2] = 0 # faz o circulos ficarem pretos
    cv2.imshow("window3",frame*(circlesImg))
    
    #desenha frame na tela
    cv2.imshow("Video", frameWarped)
    
captura.release()
cv2.destroyAllWindows()

#%%
cv2.imshow("Frame", frameWarped)
#%%
captura.release()
cv2.destroyAllWindows()
