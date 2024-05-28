from PIL import Image

def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')  # Convert to RGB to handle JPG
    encoded = img.copy()
    width, height = img.size
    message += '###'  # Terminator to indicate end of message

    bin_message = ''.join([format(ord(i), "08b") for i in message])
    pixel_count = width * height
    if len(bin_message) > pixel_count * 3:
        raise ValueError("Message is too long to hide in the image")

    data_index = 0
    for row in range(height):
        for col in range(width):
            if data_index < len(bin_message):
                pixel = list(img.getpixel((col, row)))
                for n in range(3):  # Only modify the RGB channels
                    if data_index < len(bin_message):
                        pixel[n] = (pixel[n] & ~1) | int(bin_message[data_index])
                        data_index += 1
                encoded.putpixel((col, row), tuple(pixel))
            else:
                break

    encoded.save(output_path, format='PNG')  # Save as PNG to prevent data loss

def reveal_message(image_path):
    img = Image.open(image_path).convert('RGB')  # Ensure it's in RGB mode
    width, height = img.size
    bin_message = ''
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for n in range(3):  # Only read the RGB channels
                bin_message += str(pixel[n] & 1)

    bin_message = [bin_message[i: i + 8] for i in range(0, len(bin_message), 8)]
    message = ''.join([chr(int(b, 2)) for b in bin_message])
    terminator_index = message.find('###')
    if terminator_index != -1:
        message = message[:terminator_index]
    else:
        raise ValueError("Terminator not found, message may be corrupted")
    return message
