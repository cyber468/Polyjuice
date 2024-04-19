import sys
import argparse
from colorama import Fore

from pkgs import audio_steganography
from pkgs import image_steganography
from pkgs import text_steganography
from pkgs import video_steganography



class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self):
        # Custom help message
        symbols()
        print("""
        Usage:

        Encoding: Steganography.py <filetype> <mode> <Key> <filename>
        
        Decoding: Steganography.py -d <Key> <filename>
        
        Options:
        -a, --audio      : For audio file
        -t, --text       : For text file
        -v, --video      : For video file
        -i, --image      : For image file
        -e, --encode     : For encoding
        -d, --decode     : For decoding
        <Key>            : Key to encode or decode the data
        <filename>       : Location of the file
        """)




def symbols():
    
    print("")

    sym="""\u001b[38;5;129m
     ██▓███  ▒█████   ██▓   ▓██   ██▓ ▄▄▄██▀▀▀█    ██  ██▓ ▄████▄ ▓█████ 
    ▓██░  ██▒██▒  ██▒▓██▒    ▒██  ██▒   ▒██   ██  ▓██▒▓██▒▒██▀ ▀█ ▓█   ▀ 
    ▓██░ ██▓▒██░  ██▒▒██░     ▒██ ██░   ░██  ▓██  ▒██░▒██▒▒▓█    ▄▒███   
    ▒██▄█▓▒ ▒██   ██░▒██░     ░ ▐██▓░▓██▄██▓ ▓▓█  ░██░░██░▒▓▓▄ ▄██▒▓█  ▄ 
    ▒██▒ ░  ░ ████▓▒░░██████▒ ░ ██▒▓░ ▓███▒  ▒▒█████▓ ░██░▒ ▓███▀ ░▒████▒
    ▒▓▒░ ░  ░ ▒░▒░▒░ ░ ▒░▓  ░  ██▒▒▒  ▒▓▒▒░  ░▒▓▒ ▒ ▒ ░▓  ░ ░▒ ▒  ░░ ▒░ ░
    ░▒ ░      ░ ▒ ▒░ ░ ░ ▒  ░▓██ ░▒░  ▒ ░▒░  ░░▒░ ░ ░  ▒ ░  ░  ▒   ░ ░  ░
    ░░      ░ ░ ░ ▒    ░ ░   ▒ ▒ ░░   ░ ░ ░   ░░░ ░ ░  ▒ ░░          ░   
                ░ ░      ░  ░░ ░      ░   ░     ░      ░  ░ ░        ░  ░
                             ░ ░                          ░              
    """
    print(sym)
    print("\u001b[38;5;231m-----Done by βαδβμηηλ-----\n")

    


def main():
    parser = CustomArgumentParser()
    parser.add_argument('-a', '--audio', action='store_true', help="For audio file")
    parser.add_argument('-t', '--text', action='store_true', help="For text file")
    parser.add_argument('-v', '--video', action='store_true', help="For video file")
    parser.add_argument('-i', '--image', action='store_true', help="For image file")
    parser.add_argument('-e', '--encode', action='store_true', help="For encoding")
    parser.add_argument('-d', '--decode', action='store_true', help="For decoding")
    parser.add_argument('Key')
    parser.add_argument('filename')
    
    args = parser.parse_args()
    c = 0
    t = True
    if args.filename and args.Key:
        symbols()
        if args.audio and args.encode and t:
            audio_steganography.Audio_steganography(args.filename, 0,args.Key)
            t = False
        elif args.audio and args.decode and t:
            audio_steganography.Audio_steganography(args.filename, 1,args.Key)
            t = False
        elif args.text and args.encode and t:
            text_steganography.Text_steganography(args.filename, 0,args.Key)
            t = False
        elif args.text and args.decode and t:
            text_steganography.Text_steganography(args.filename, 1,args.Key)
            t = False
        elif args.video and args.encode and t:
            video_steganography.Video_Steganography(args.filename, 0,args.Key)
            t = False
        elif args.video and args.decode and t:
            video_steganography.Video_Steganography(args.filename, 1,args.Key)
            t = False
        elif args.image and args.encode and t:
            image_steganography.Image_steganography(args.filename, 0,args.Key)
            t = False
        elif args.image and args.decode and t:
            image_steganography.Image_steganography(args.filename, 1,args.Key)
            t = False
        else:
            c = 1
            
    else:
        symbols()
        parser.print_help()
        sys.exit(0)
    if c == 1:
        symbols()
        parser.print_help()
        sys.exit()


if __name__ == "__main__":
    main()
