from __future__ import division
import cv2
from cv2 import imshow
import numpy as np
import socket
import struct
import sys
import OCR
import Linguist
import time

font = cv2.FONT_HERSHEY_COMPLEX
MAX_DGRAM = 2**16

def tm():
    return time.time()

def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(len(seg))
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break

def main():
    """ Getting image udp frame &
    concate before decode and output image """
    # Set up socket
    print("MAIN")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 65003))
    
    dat = b''
    fail_count = 0
    print("START LOOP")
    img_container = []
    width = 479
    height = 841
    img_container = np.zeros([height,width,3],dtype=np.uint8)

    its = 0
    while True:
        its +=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Exiting...')
            break

        #print("receivning...")
        seg, addr = s.recvfrom(MAX_DGRAM)
        print("seg len:", len(seg))
        if (seg):
            dat = seg
            meta = dat[0:19]
            coords = np.frombuffer(meta[11:15], dtype=np.uint16)
            x_start = coords[0]
            y_start = coords[1]
            buff = np.frombuffer(dat[19:], dtype=np.uint8)
            img = cv2.imdecode(buff, 1)
            
            if img is not None:
                img_height = len(img)
                img_width = len(img[0])
                x_end = x_start + img_width
                y_end = y_start + img_height
                
                img_container[y_start:y_end, x_start:x_end] = img
                
                cv2.imshow("img_container", img_container)

            else:
                #pass
                print("received img is None")
        else:
            dat += seg
            if fail_count > 50:
                break
            print("FAIL: seg is none")
            fail_count += 1
        
    cv2.waitKey(5)
    print("destroy all")
    cv2.destroyAllWindows()
    s.close()


if __name__ == "__main__":
    main()