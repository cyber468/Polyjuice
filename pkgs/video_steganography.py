import math
import os
import shutil
import subprocess
import cv2
from stegano import lsb
from . import security

def Video_Steganography(file, n, key):
    temp_dir = os.path.abspath("./temp")

    def split_string(split_str, count=10):
        per_c = math.ceil(len(split_str) / count)
        c_cout = 0
        out_str = ''
        split_list = []
        for s in split_str:
            out_str += s
            c_cout += 1
            if c_cout == per_c:
                split_list.append(out_str)
                out_str = ''
                c_cout = 0
        if c_cout != 0:
            split_list.append(out_str)
        return split_list

    def frame_extraction(video):
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            print("[INFO] temp directory is created")
        temp_folder = temp_dir
        vidcap = cv2.VideoCapture(video)
        count = 0
        while True:
            success, image = vidcap.read()
            if not success:
                break
            cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
            count += 1

    def encode_string(input_string):
        split_string_list = split_string(input_string)
        for i in range(len(split_string_list)):
            f_name = os.path.join(temp_dir, "{}.png".format(i))
            secret_enc = lsb.hide(f_name, split_string_list[i])
            secret_enc.save(f_name)
            print("[INFO] frame {} holds {}".format(f_name, lsb.reveal(f_name)))
        print("[INFO] The message is stored in the Embedded_Video.mp4 file")
    
    def clean_temp():
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("\u001b[38;5;231m[INFO] temp files are cleaned up")

    def Decode():
        print("[INFO] Video Steganography DECODING")
        print("")
        frame_extraction(file)
        secret = []
        try:
            for i in range(len(os.listdir(temp_dir))):
                f_name = os.path.join(temp_dir, "{}.png".format(i))
                secret_dec = lsb.reveal(f_name)
                if secret_dec is None:
                    break
                secret.append(secret_dec)
        except IndexError:
            pass
        a = ''.join(secret)
        deciph = security.decrypt_text(key, a)
        print("[*] The Encoded data was: \u001b[38;5;129m{}".format(deciph))
        print("")
        clean_temp()

    def Encode():
        print("[INFO] Video Steganography ENCODING")
        print("")
        ciph = input("[*] Enter the message :")
        input_string = security.encrypt_text(key, ciph)
        frame_extraction(file)
        # Check if frame extraction was successful
        if not os.path.exists(temp_dir):
            print("[ERROR] Frame extraction failed.")
            clean_temp()
            return

        try:
            # Encode audio stream
            subprocess.run(["ffmpeg", "-i", file, "-q:a", "0", "-map", "a", os.path.join(temp_dir, "audio.mp3"), "-y"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)

            # Encode video stream
            encode_string(input_string)

            # Combine audio and video streams
            subprocess.run(["ffmpeg", "-i", os.path.join(temp_dir, "%d.png"), "-c:v", "png", "-preset", "ultrafast",
                        "-crf", "0", "-pix_fmt", "yuv420p", os.path.join(temp_dir, "Embedded_Video.mp4"), "-y"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
                        
            subprocess.run(["ffmpeg", "-i", os.path.join(temp_dir, "Embedded_Video.mp4"), "-i", os.path.join(temp_dir, "audio.mp3"),
                            "-codec", "copy", os.path.join(temp_dir, "Embedded_Video_Final.mp4"), "-y"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)

            # Remove original file
            os.remove(file)

            # Move final video file to original file name
            shutil.move(os.path.join(temp_dir, "Embedded_Video_Final.mp4"), file)
            print("[INFO] FILE LOCATION:{}".format(file))
            clean_temp()

        except subprocess.CalledProcessError as e:
            print("[ERROR] Encoding failed with error code:", e.returncode)
            clean_temp()

        except Exception as e:
            print("[ERROR] An unexpected error occurred during encoding:", e)
            clean_temp()

    if n == 0:
        try:
            Encode()
        except Exception as e:
            print("[ERROR] Encoding Failed")
            print(e)
    else:
        try:
            Decode()
        except Exception as e:
            print("[ERROR] Decoding Failed")
            print(e)

