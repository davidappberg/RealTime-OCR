from __future__ import division
import cv2
from cv2 import imshow
import numpy as np
import socket
import struct
import sys
import OCR
import Linguist

font = cv2.FONT_HERSHEY_COMPLEX
MAX_DGRAM = 2**16

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
    host = socket.gethostname()
    print("host: ", host)
    print("AF_NET", socket.AF_INET)
    print("SOCK_DGRAM", socket.SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.bind(('94.254.42.75', 65001))
    s.bind(('127.0.0.1', 65003))
    #s.bind(('94.254.42.75', 6667))
    #s.bind(('127.0.0.1', 27015))
    print("s: ", s)
    #dump_buffer(s)
    #s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s2.bind(('127.0.0.1', 6666))
    #print("s2: ", s2)

    dat = b''
    fail_count = 0
    print("START LOOP")
    img_container = []
    width = 479
    height = 841
    #width = 0 ## set these dynamically later
    #height = 0
    img_container = np.zeros([height,width,3],dtype=np.uint8)
    img_blank = np.zeros([height,width,3],dtype=np.uint8)
    #cv2.imshow("blank", img_blank)
    its = 0
    while True:
        its +=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Exiting...')
            break

        #print("receivning...")
        seg, addr = s.recvfrom(MAX_DGRAM)
        #print("seg len:", len(seg))
        if (seg):
            if (dat != b''):
                #print("type of seg", type(seg))
                #print("dat len: ", len(dat))
                meta = dat[0:19]
                #x_start = struct.unpack("H", meta[11:13])[0]
                #y_start = struct.unpack("H", meta[13:15])[0]
                #print("x_start=", x_start, "  y_start=", y_start)
                coords = np.frombuffer(meta[11:15], dtype=np.uint16)
                x_start = coords[0]
                y_start = coords[1]
                buff = np.frombuffer(dat[19:], dtype=np.uint8)
                buff_len = len(buff)
                #print("buff first: ", buff[0:30])
                #print("buff last: ", buff[buff_len-30:buff_len])
                img = cv2.imdecode(buff, 1)
                
                '''if buff_len > largest_size:
                    largest_size = buff_len
                    img_container = buff
                else:
                    img_container[0:buff_len] = buff'''
                
                if img is not None:
                    img_height = len(img)
                    img_width = len(img[0])
                    x_end = x_start + img_width
                    y_end = y_start + img_height
                    #print("x_start =", x_start, "  y_start =", y_start)
                    #print("x_end =", x_end, "  y_end =", y_end)
                    #print("width =", img_width, "  height =", img_height)
                    '''if img_height+y_start > height:
                        height = img_height+y_start
                        print("test resize")
                        img_container[height:img_height+y_start] = img
                        print("resize success")
                    if img_width+x_start> width:
                        width = img_width+x_start'''
                    
                    img_container[y_start:y_end, x_start:x_end] = img
                    #ocr: OCR, frame, x_start, y_start, x_end, y_end
                    #OCR.custom_process_frame(ocr, img_container, x_start, y_start, x_end, y_end)
                    
                    if its == 1:
                        img_container = OCR.custom_process_frame(ocr, img_container, 0, 0, 479, 841)
                    elif its % 10 == 0:
                        #pass
                        img_container = OCR.custom_process_frame(ocr, img_container, x_start, y_start, x_end, y_end)
                    
                    
                    cv2.imshow("img_container", img_container)

                    #cv2.imshow('frame', img_container)
                    #cv2.putText(img_blank, "x", (x_start, y_start), font, 0.5, (255,0,0), 2)
                    #cv2.imshow("img_container", img_container)
                    #break
                    #print('success')
                else:
                    pass
                    print("fail")
                '''try:
                    #img = cv2.imdecode(buff, 1)
                    #imgRot = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
                    #cv2.imshow('frame', img)
                    #print(img.shape)
                    #cam.send(img)
                    #cam.sleep_until_next_frame()
                    print("success")
                except:
                    print("fail")
                    pass'''

            dat = b''
            dat += seg
        else:
            dat += seg
            if fail_count > 50:
                break
            print("FAIL: seg is none")
            fail_count += 1
        
        #img_container = np.zeros(largest_size, dtype=np.uint8)
        #img_container = np.zeros([height,width,3],dtype=np.uint8)
        
    cv2.waitKey(0)
    print("destroy all")
    cv2.destroyAllWindows()
    s.close()


if __name__ == "__main__":
    OCR.tesseract_location()
    ocr = OCR.custom_stream()
    main()
'''
dat len:  792
buff first:  [255 216 255 224   0  16  74  70  73  70   0   1   2   0   0   1   0   1
   0   0 255 219   0  67   0  27  18  20  23  20]
buff last:  [ 89 190 131 104 162 138 208 200 116 146  60 174  94  70  46 199 169  39
  36 211 104 162   0   0   0   0   0   0   0   0]


frame_index: 177  chunk_index: 0  chunk_count: 1  size: 792  offset: 0  final_offset: 784  x: 416  y: 736
final img len: 792

'''