def shift_character(char, shift):
    if char == ' ':
        return char
    elif 'a' <= char <= 'z':
        return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
    elif 'A' <= char <= 'Z':
        return chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
    else:
        return chr((ord(char) + shift) % 256)
    
def encrypt(plaintext, shift):
    return ''.join([shift_character(char, shift) for char in plaintext])

def decrypt(ciphertext, shift):
    return ''.join([shift_character(char, -shift) for char in ciphertext])

if __name__ == '__main__':
    print(encrypt("Hello World!", 3))  # Output: Khoor Zruog$
    print(decrypt("Khoor Zruog$", 3))  # Output: Hello World!

    print(encrypt("zzz", 6))           # Output: fff
    print(decrypt("fff", 6))           # Output: zzz

    print(encrypt("FFF", -6))          # Output: ZZZ
    print(decrypt("ZZZ", -6))          # Output: FFF