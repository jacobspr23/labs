class Caesar:
    def __init__(self, shift=0):
        self._shift = shift

    @property
    def key(self):
        return self._shift

    @key.setter
    def key(self, shift):
        self._shift = shift

    def set_key(self, shift):
        self._shift = shift

    def encrypt(self, plaintext):
        result = ""
        for char in plaintext:
            if char == ' ':
                result += char
            elif 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') + self._shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') + self._shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) + self._shift) % 256)
        return result

    def decrypt(self, ciphertext):
        result = ""
        for char in ciphertext:
            if char == ' ':
                result += char
            elif 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') - self._shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') - self._shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - self._shift) % 256)
        return result


cipher = Caesar()
cipher.set_key(3)
print(cipher.encrypt("Hello World!")) 
print(cipher.decrypt("Khoor Zruog$")) 

cipher.set_key(6)
print(cipher.encrypt("zzz")) 
print(cipher.decrypt("fff")) 

cipher.set_key(-6)
print(cipher.encrypt("FFF"))
print(cipher.decrypt("zzz")) 
