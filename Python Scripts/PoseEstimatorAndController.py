"""
UAV Controller Script.

Implements head pose estimation using 68 facial landmark detection.
The roll pitch and yaw data calculated is used to simulate key presses
using pynput for controlling any UAV in any simulator.
"""

import time
import cv2
import dlib
import numpy as np
import math
from pynput.keyboard import Key,Controller

keyboard=Controller()
DEBUG = True


def main():
    cap = cv2.VideoCapture(0)
    time.sleep(1.0)

    if not cap.isOpened():
        print("Error: Camera is unavailable.")
    else:
        print("Camera Found! Starting feed...")

    #Create Main Window
    cv2.namedWindow('Video')
    cv2.moveWindow('Video', 875, 40)

    # Declaring the face detector and landmark detector
    face_detector = dlib.get_frontal_face_detector()
    landmark_detector = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    estimated_pitch = 0.0
    estimated_roll = 0.0
    estimated_yaw = 0.0

    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Search for faces
        faces = face_detector(gray, 0)

        #Is face detected?
        if len(faces) > 0:
            text = "{} face(s) found".format(len(faces))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)

        # loop over the face detections
        for face in faces:
            left = face.left()
            top = face.top()
            right = face.right()
            bottom = face.bottom()

            # Drawing a green rectangle (and text) around the face.
            label_x = left
            label_y = top - 3
            if label_y < 0:
                label_y = 0
            cv2.putText(frame, "FACE", (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 0), 1)

            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = landmark_detector(gray, face)
            landmark_coords = np.zeros((shape.num_parts, 2), dtype="int")

            # 2D model points
            image_points = np.float32([
                (shape.part(30).x, shape.part(30).y),  # nose
                (shape.part(8).x, shape.part(8).y),  # Chin
                (shape.part(36).x, shape.part(36).y),  # Left eye left corner
                (shape.part(45).x, shape.part(45).y),  # Right eye right corner
                (shape.part(48).x, shape.part(48).y),  # Left Mouth corner
                (shape.part(54).x, shape.part(54).y),  # Right mouth corner
                (shape.part(27).x, shape.part(27).y)
            ])

            print(image_points)

            # 3D model points
            model_points = np.float32([
                (0.0, 0.0, 0.0),  # Nose tip
                (0.0, -330.0, -65.0),  # Chin
                (225.0, 170.0, -135.0),  # Left eye left corner
                (-225.0, 170.0, -135.0),  # Right eye right corner
                (150.0, -150.0, -125.0),  # Left Mouth corner
                (-150.0, -150.0, -125.0),  # Right mouth corner
                (0.0, 140.0, 0.0)
            ])

            
            height, width, _ = frame.shape

            # Camera internals
            focal_length = width
            center = np.float32([width / 2, height / 2])
            camera_matrix = np.float32([[focal_length, 0.0, center[0]],
                                           [0.0, focal_length, center[1]],
                                           [0.0, 0.0, 1.0]])
            dist_coeffs = np.zeros((4, 1), dtype="float32") #Assuming no lens distortion

            retval, rvec, tvec = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)

            nose_end_point3D = np.float32([[50, 0, 0],
                                      [0, 50, 0],
                                      [0, 0, 50]])

            nose_end_point2D, jacobian = cv2.projectPoints(nose_end_point3D, rvec, tvec, camera_matrix, dist_coeffs)

            rotCamerMatrix, _ = cv2.Rodrigues(rvec)

            euler_angles = getEulerAngles(rotCamerMatrix)

            # Filter angle
            estimated_pitch = (0.5 * euler_angles[0]) + (1.0 - 0.5) * estimated_pitch
            estimated_yaw = (0.5 * euler_angles[1]) + (1.0 - 0.5) * estimated_yaw
            estimated_roll = (0.5 * euler_angles[2]) + (1.0 - 0.5) * estimated_roll

            euler_angles[0] = estimated_pitch
            euler_angles[1] = estimated_yaw
            euler_angles[2] = estimated_roll

            # Draw used points for head pose estimation
            for point in image_points:
                print(point[0])
                cv2.circle(frame, (point[0], point[1]), 3, (255, 0, 255), -1)
            
            MouthIndex=Mouth(shape)
            # Draw face angles
            pitch = "EPitch: {}".format(estimated_pitch)
            yaw = "EYaw: {}".format(estimated_yaw)
            roll = "ERoll: {}".format(estimated_roll)
            MouthInd="MI: {}".format(MouthIndex)

            cv2.putText(frame, pitch, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 2)
            cv2.putText(frame, yaw, (left, bottom + 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            cv2.putText(frame, roll, (left, bottom + 60), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            cv2.putText(frame, MouthInd, (left, bottom + 80), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 255), 2)
            
            
            '''The four if blocks below are used to specify key presses
            and releases which are to be simulated when specific estimated values
            for roll, pitch, yaw as well as mouth index cross a 
            specified threshold value. Change them as per the controls of
            the game/simulator being used.'''
            
            pitch_threshold_neg=7
            pitch_threshold_pos=20
            roll_threshold_neg=-10
            roll_threshold_pos=10
            yaw_threshold_neg=-20
            yaw_threshold_pos=20
            MouthInd_threshold=0.37
            
            s=''
            
            #Simulates input for pitch control of drone
            if estimated_pitch<pitch_threshold_neg:
                keyboard.release('s')
                keyboard.press('w')
                cv2.putText(frame, "Pitch(W)", (10, 75), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
                s='U'
            elif estimated_pitch>pitch_threshold_pos:
                keyboard.release('w')
                keyboard.press('s')
                cv2.putText(frame, "Pitch(S)", (10, 75), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
                s='D'
            else:
                keyboard.release('w')
                keyboard.release('s')
                s='N'
                
            
            #Simulates input for roll control of drone
            if estimated_roll<roll_threshold_neg:
                keyboard.release('d')
                keyboard.press('a')
                cv2.putText(frame, "Roll(A)", (10, 95), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
                s+='L'
            elif estimated_roll>roll_threshold_pos:
                keyboard.release('a')
                keyboard.press('d')
                cv2.putText(frame, "Roll(D)", (10, 95), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
                s+='R'
            else:
                keyboard.release('a')
                keyboard.release('d')
                s+='N'
            
            #Simulates input for yaw control of drone
            if estimated_yaw<yaw_threshold_neg:
                keyboard.release(Key.right)
                keyboard.press(Key.left)
                cv2.putText(frame, "Yaw(<-)", (10, 115), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
                s+='L'
            elif estimated_yaw>yaw_threshold_pos:
                keyboard.release(Key.left)
                keyboard.press(Key.right)
                cv2.putText(frame, "Yaw(->)", (10, 115), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
                s+='R'
            else:
                keyboard.release(Key.left)
                keyboard.release(Key.right)
                s+='N'
              
            #Used to simulate input for upward thrust
            if MouthIndex>MouthInd_threshold:
                keyboard.press(Key.up)
                cv2.putText(frame, "Lift Up", (10, 135), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            else:
                keyboard.release(Key.up)
            
            
            for i in range(0, shape.num_parts):
                landmark_coords[i] = (shape.part(i).x, shape.part(i).y)

            
            for (i, (x, y)) in enumerate(landmark_coords):
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                

        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            keyboard.release(Key.left)
            keyboard.release(Key.right)
            keyboard.release('w')
            keyboard.release('s')
            keyboard.release('a')
            keyboard.release('d')
            keyboard.release(Key.up)
            break

    
    cap.release()
    cv2.destroyAllWindows()
    print("Exiting...")



#Calculate pitch, roll and yaw from rotation matrix
def getEulerAngles(camera_rot_matrix):
    rt = cv2.transpose(camera_rot_matrix)
    shouldBeIdentity = np.matmul(rt, camera_rot_matrix)
    identity_mat = np.eye(3,3)#, #dtype="float32")
    
    isSingularMatrix = cv2.norm(identity_mat, shouldBeIdentity) < 1e-6

    euler_angles = np.float32([0.0, 0.0, 0.0])
    if not isSingularMatrix:
        return euler_angles

    sy = math.sqrt(camera_rot_matrix[0,0] * camera_rot_matrix[0,0] +  camera_rot_matrix[1,0] * camera_rot_matrix[1,0]);

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(camera_rot_matrix[2,1] , camera_rot_matrix[2,2])
        y = math.atan2(-camera_rot_matrix[2,0], sy)
        z = math.atan2(camera_rot_matrix[1,0], camera_rot_matrix[0,0])
    else:
        x = math.atan2(-camera_rot_matrix[1,2], camera_rot_matrix[1,1])
        y = math.atan2(-camera_rot_matrix[2,0], sy)
        z = 0

    x = x * 180.0 / math.pi
    y = y * 180.0 / math.pi
    z = z * 180.0 / math.pi

    euler_angles[0] = -x
    euler_angles[1] = y
    euler_angles[2] = z

    return euler_angles

#Calculte Mouth Index
def Mouth(shape):
    vert=abs(shape.part(51).y-shape.part(57).y)
    horiz=abs(shape.part(48).x-shape.part(54).x)
    return vert/horiz
    


if __name__ == "__main__":
    main()