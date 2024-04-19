import sys
import os 
from . import security

def Text_steganography(file, n,key):
    def text_to_binary(text):
        binary_data = ''.join(format(ord(char), '08b') for char in text)
        return binary_data

    def binary_to_text(binary_data):
        text = ''
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            text += chr(int(byte, 2))  # Convert 8-bit binary to character
        return text

    def embed_data(original_text, data_to_hide):
        binary_data_to_hide = text_to_binary(data_to_hide)
        modified_text = ''
        bit_count = 0

        for char in original_text:
            if char.isspace() and bit_count < len(binary_data_to_hide):
                # Embed data only if the current character is a space and there's data to embed
                if binary_data_to_hide[bit_count] == '0':
                    modified_text += '\u00A0'  # Unicode for non-breaking space
                elif binary_data_to_hide[bit_count] == '1':
                    modified_text += '\u200A'  # Unicode for en space
                bit_count += 1
            else:
                modified_text += char
        
        return modified_text

    def extract_data(modified_text):
        extracted_data = ''
        for char in modified_text:
            if char == '\u00A0':
                extracted_data += '0'  # Append '0' for non-breaking space
            elif char == '\u200A':
                extracted_data += '1'  # Append '1' for en space
        return extracted_data

    def Encode():
        # Encode mode
        # Read original text from output file
        with open(file, 'r') as f:
            original_text = f.read()
        lenlmt=[x for x in original_text]
        print("[INFO] Secret Message Limit", len(lenlmt))    
        ciph = input("[*] Enter Secret message: ")
        data_to_hide = security.encrypt_text(key,ciph)
        # Embed data into the original text
        print("[INFO] Performing Steganography")
        modified_text = embed_data(original_text, data_to_hide)

        # Write modified text back to the same output file
        with open(file, 'w') as f:
            f.write(modified_text)
        print("[*] Data written to: \u001b[38;5;129m", file)

    def Decode():
        print("[INFO] Reading File")
        with open(file, 'r') as f:
            modified_text = f.read()

        # Extract data from modified text
        extracted_data = extract_data(modified_text)
        ciph_text = binary_to_text(extracted_data)
        hidden_text=security.decrypt_text(key,ciph_text)
        print("[*] Extracted Data: \u001b[38;5;129m", hidden_text)

    if n == 0:
        Encode()
    elif n == 1:
        Decode()