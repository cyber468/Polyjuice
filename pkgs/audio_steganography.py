import os
import wave
from . import security


def Audio_steganography(file, n, key):
    def Encode():
        print("[INFO] Audio Steganography ENCODING")
        print("")
        song = wave.open(file, mode='rb')
        nframes = song.getnframes()
        frames = song.readframes(nframes)
        frame_list = list(frames)
        frame_byte = bytearray(frame_list)
        msg = input("[*] Enter the secret message:-")
        data= security.encrypt_text(key,msg)
        res = ''.join(format(i, '08b') for i in bytearray(data, encoding='utf-8'))
        print("[INFO] The String after binary conversion:-{}".format(res))
        length = len(res)
        print("[INFO] Length of binary after conversion:-{}".format(length))

        data = data + '*^*^*'

        results = []
        for j in data:
            bits = bin(ord(j))[2:].zfill(8)
            results.extend([int(b) for b in bits])

        k = 0
        for i in range(0, len(results), 1):
            res = bin(frame_byte[k])[2:].zfill(8)
            if res[len(res) - 4] == results[i]:
                frame_byte[k] = (frame_byte[k] & 253)
            else:
                frame_byte[k] = (frame_byte[k] & 253) | 2
                frame_byte[k] = (frame_byte[k] & 254) | results[i]
            k = k + 1
        frame_modified = bytes(frame_byte)
        os.remove(file)
        with wave.open(file, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        print("[INFO] ENCODING DATA Successful")
        print("[INFO] LOCATION:{}".format(file))
        song.close()
        

    def Decode():
        print("[INFO] Audio Steganography DECODING")
        print("")
        song = wave.open(file, mode='rb')
        nframes = song.getnframes()
        frames = song.readframes(nframes)
        frame_list = list(frames)
        frame_bytes = bytearray(frame_list)

        extracted = ""
        p = 0
        for i in range(len(frame_bytes)):
            if p == 1:
                break
            res = bin(frame_bytes[i])[2:].zfill(8)
            if res[len(res) - 2] == 0:
                extracted += res[len(res) - 4]
            else:
                extracted += res[len(res) - 1]

            all_bytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
            decode_data = ""
            for byte in all_bytes:
                decode_data += chr(int(byte, 2))
                if decode_data[-5:] == '*^*^*':
                    f=security.decrypt_text(key,decode_data[:-5])

                    print("[*] The Encoded data was: \u001b[38;5;129m{}".format(f))
                    p = 1
                    break
        

    if n == 0:
        Encode()
    else:
        Decode()