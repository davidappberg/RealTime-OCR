import argparse

import OCR
import Linguist
import sys

def main():
    """
    Handles command line arguments and begins the real-time OCR by calling ocr_stream().
    A path to the Tesseract cmd root is required, but all other params are optional.

    Example command-line use: python3 Main.py -t /usr/local/Cellar/tesseract/4.1.1/bin/tesseract

    optional arguments:
      -h, --help         show this help message and exit
      -c  , --crop       crop OCR area in pixels (two vals required): width height
      -v , --view_mode   view mode for OCR boxes display (default=1)
      -sv, --show_views  show the available view modes and descriptions
      -l , --language    code for tesseract language, use + to add multiple (ex: chi_sim+chi_tra)
      -sl, --show_langs  show list of tesseract (4.0+) supported langs

    required named arguments:
      -t , --tess_path   path to the cmd root of tesseract install (see docs for further help)
    """
    parser = argparse.ArgumentParser()

    # Required:
    requiredNamed = parser.add_argument_group('required named arguments')

    requiredNamed.add_argument('-t', '--tess_path',
                               help="path to the cmd root of tesseract install (see docs for further help)",
                               metavar='', default=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    # Optional:
    parser.add_argument('-c', '--crop', help="crop OCR area in pixels (two vals required): width height",
                        nargs=2, type=int, metavar='')

    parser.add_argument('-v', '--view_mode', help="view mode for OCR boxes display (default=1)",
                        default=1, type=int, metavar='')
    parser.add_argument('-sv', '--show_views', help="show the available view modes and descriptions",
                        action="store_true")

    parser.add_argument("-l", "--language",
                        help="code for tesseract language, use + to add multiple (ex: chi_sim+chi_tra)",
                        metavar='', default=None)
    parser.add_argument("-sl", "--show_langs", help="show list of tesseract (4.0+) supported langs",
                        action="store_true")
    parser.add_argument("-s", "--src", help="SRC video source for video capture",
                        default=0, type=int) # --src ../text_from_images/video_test.mp4
    #parser.add_argument("-s", "--src", help="SRC video source for video capture",
    #                    default=0) # --src ../text_from_images/video_test.mp4

    args = parser.parse_args()

    if args.show_langs:
        Linguist.show_codes()

    if args.show_views:
        print(OCR.views.__doc__)

    # This is where OCR is started...
    OCR.tesseract_location(args.tess_path)
    OCR.ocr_stream(view_mode=args.view_mode, source=args.src, crop=args.crop, language=args.language)


if __name__ == '__main__':
  try:
    main()  # '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
  except:
    print("EXIT")
    sys.exit(1)
  ''' str = "42.560"
  f = float(str)
  i = int(f)
  print(type(i))
  if type(f) == float:
    print("float")
  
  if type(float) != int:
    print("not int")'''