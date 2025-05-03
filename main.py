import os
import random
from PIL import Image

# https://github.com/jj30/Steganography/blob/master/app/src/main/java/stega/jj/bldg5/steganography/Encode.java

def encode(image, text):
    img = Image.open(image)
    (width, height) = img.size
    
    # Convert text to bytes
    text_bytes = text.encode('utf-8')
    
    # Convert bytes to hex string
    hex_string = text_bytes.hex()
    
    # Convert hex string to list of integers (0-15)
    int_list = [int(hex_string[i:i+1], 16) for i in range(0, len(hex_string))]
    
    counter = 0
    for h in range(0, height - 1):
        for w in range(0, width - 1):
            pixel = img.getpixel((w, h))
            r, g, b = pixel
            r, g, b = normalize(r, g, b)

            if counter < len(int_list):
                # Modify the pixel if it's part of our message
                if counter in int_list:
                    r = modify(r)
                    g = modify(g)
                    b = modify(b)
                    img.putpixel((w, h), (r, g, b))

            counter += 1
            counter = counter % 16

    img.save("encoded.png")

def normalize(r, g, b):
    if (r % 8) == 1 and (g % 8) == 1 and (b % 8) == 1:
        seed = random.randint(1, 3)
        if seed == 1:
            return (r - 1 if r >= 128 else r + 1, g, b)
        elif seed == 2:
            return (r, g - 1 if g >= 128 else g + 1, b)
        elif seed == 3:
            return (r, g, b - 1 if b >= 128 else b + 1)
        
    else:
        return (r, g, b)
    

def modify(value):
    for x in range(0, 9):
        if (value % 8) == 1:
            return value
        value = value - 1 if value >= 128 else value + 1

    return value

def decode(image):
    img = Image.open(image)
    (width, height) = img.size
    counter = 0

    print(f"width {width} height {height}")
    
    intMessage = []
    for h in range(0, height - 1):
        for w in range(0, width - 1):
            pixel = img.getpixel((w, h))
            r, g, b = pixel

            if (r % 8) == 1 and g % 8 == 1 and b % 8 == 1:
                intMessage.append(counter)

            counter += 1
            counter = counter % 16
            
    print(f"Collected integers: {intMessage}")
    
    # Convert integers to hex string
    hex_string = ''.join([format(i, 'x') for i in intMessage])
    print(f"Hex string: {hex_string}")
    
    try:
        # Convert hex string to bytes
        bytes_data = bytes.fromhex(hex_string)
        print(f"Bytes data: {bytes_data}")
        
        # Try to decode as UTF-8
        decoded_message = bytes_data.decode('utf-8')
        print(f"Decoded message: {decoded_message}")
    except (ValueError, UnicodeDecodeError) as e:
        print(f"Error decoding message: {e}")

if __name__ == "__main__":
    #encode("lolcat.webp", "Hello, world!")
    decode("encoded.png")
