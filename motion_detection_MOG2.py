from picamera2 import Picamera2
import cv2 as cv
import time
import os

picam2 = Picamera2()
# For Arducam OV5647 camera module, mode[0] is 10 bit, 640x480 resolution, 58.92fps
mode = picam2.sensor_modes[0]
config = picam2.create_preview_configuration(
    sensor={'output_size': mode['size'], 'bit_depth': mode['bit_depth']})
picam2.configure(config)
picam2.start()
time.sleep(2)
# disable auto white balance and exposure control to prevent unintended image changes
picam2.set_controls({"AwbEnable": 0, "AeEnable": 0})

backSub = cv.createBackgroundSubtractorMOG2()
cv.BackgroundSubtractorMOG2.setDetectShadows(backSub, False)

try:
    while True:
        frame = picam2.capture_array()
        fgMask = backSub.apply(frame)
        # perform image thresholding on the foreground mask frame to remove noises
        ret, threshold = cv.threshold(fgMask.copy(), 127, 255, cv.THRESH_BINARY)
        # perform dilation on the frame to fill in any small gaps in the foreground mask frame
        erosion_size = 1
        element = cv.getStructuringElement(cv.MORPH_ELLIPSE,
                                           (2*erosion_size+1, 2*erosion_size+1))
        dilation = cv.dilate(threshold, element)
        # finding contours to determine the position of the motions
        contours, hierarchy = cv.findContours(dilation,
                                              cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        # draw the rectangles over each detections
        for contour in contours:
            if cv.contourArea(contour) > 250:
                (x,y,w,h) = cv.boundingRect(contour)
                cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        
        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', dilation)
        
        # end the loop when Esc is pressed
        k = cv.waitKey(10) & 0xff
        if k == 27:
            break
        # save a screenshot when Space is pressed
        elif k == 32:
            cv.imwrite(os.path.dirname(__file__) + "/frame.png", frame)
    
except Exception as e:
    print(e)
    
finally:
    cv.destroyAllWindows()
    picam2.close()
