def encrypt_message(message, shift):
    encrypted = ''
    for char in message:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            encrypted += chr((ord(char) + shift - shift_amount) % 26 + shift_amount)
        else:
            encrypted += char
    return encrypted

def decrypt_message(encrypted_message, shift):
    return encrypt_message(encrypted_message, -shift)
