class BCIPHER:
    def __init__(self, plainText, size, K1=0, K2=0, K3=0):
            self.plainText = plainText & ((1 << size) - 1)
            self.size = size
            self.K1 = K1 & ((1 << size) - 1)
            self.K2 = K2 & ((1 << size) - 1)
            self.K3 = K3 & ((1 << size) - 1)
            self.cipherText = 0
            self.sBoxInput = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            self.sBoxOutput = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size
    
    def set_plainText(self, plainText):
        self.plainText = plainText

    def get_plainText(self):
        return self.plainText

    def get_cipherText(self):
        return self.cipherText
    
    def get_sBoxOutput(self):
        return self.sBoxOutput
    
    def get_sBoxInput(self):
        return self.sBoxInput
    
    def set_K1(self, K1):
        self.K1 = K1

    def get_K1(self):
        return self.K1
    
    def set_K2(self, K2):
        self.K2 = K2

    def get_K2(self):
        return self.K2
    
    def set_K3(self, K3):
        self.K3 = K3

    def get_K3(self):
        return self.K3
    
    def sBoxToBinary(self, sBox, size):
        sBoxBinary = []
        for i in sBox:
            i = i & ((1 << size) - 1)
            sBoxBinary.append(i)
        return sBoxBinary
    
    def bitWiseXOR(self, plainText, K, size):
        cipherText = 0
        for i in range(size):
            bit_plain = (plainText >> i) & 1
            print(bit_plain)
            bit_K = (K >> i) & 1
            print(bit_K)
            bit_cipher = (bit_plain ^ bit_K)
            cipherText |= (bit_cipher << i)
        return cipherText
    
    def permsOfKey(n):
        if not n:
            return
        for i in range(1, 2**n):
            yield i

    def produceCipherText(self, plainText, size, K1, K2, K3):
        inputBox = self.sBoxToBinary(self.get_sBoxInput(), size)
        outputBox = self.sBoxToBinary(self.get_sBoxOutput(), size)
        cipherText = 0 
        bitWiseK1 = self.bitWiseXOR(plainText, K1, size)
        index1 = inputBox.index(int(bitWiseK1)) 
        value1 = outputBox[index1]
        print("The result of XORing:", int(plainText ^ K1))
        print("The result of XORing:", bin(int(plainText ^ K1)))
        print("U1:", value1)
        print("U1:", bin(value1))
        bitWiseK2 = self.bitWiseXOR(value1, K2, size)
        index2 = inputBox.index(int(bitWiseK2))
        value2 = outputBox[index2]
        print("The result of XORing:", int(value1 ^ K2))
        print("The result of XORing:", bin(int(value1 ^ K2)))
        print("U2:", value2)
        print("U2:", bin(value2))
        bitWiseK3 = self.bitWiseXOR(value2, K3, size)
        value3 = int(bitWiseK3)
        print("The result of XORing:", int(value2 ^ K3))
        print("The result of XORing:", bin(int(value2 ^ K3)))
        print("Cipher Text:", value3)
        print("Cipher Text:", bin(value3))
        
        cipherText = value3
        return cipherText
    
    def inverseCipherText(self, cypherText, size):
        inverseInputBox = self.sBoxToBinary(self.get_sBoxOutput(), size)
        inverseOutputBox = self.sBoxToBinary(self.get_sBoxInput(), size)
        possibleKeys = self.permsOfkey(15)
        plainText = self.permsOfkey(15)
        agreement = 0
        
        for perm in possibleKeys:
            U3 = perm ^ cypherText
            index = inverseInputBox.index(U3) 
            U2 = inverseOutputBox[index]
            # Convert U2 to a 4-bit binary string
            binary_string = format(U2, '04b')  # '04b' formats as 4-bit binary string
            # Extract the last 3 bits and perform XOR
            last_three_bits = int(binary_string[-3:], 2)  # Extract last 3 bits as an integer
            xor_value = 0b111  # Replace with the value you want to XOR
            y2y3y4 = last_three_bits ^ xor_value  # XOR operation
            for perms in plainText:
            # Convert the number to a binary string
                x4 = format(plainText[perms], '04b')  # 4-bit binary string
            # Extract the fourth bit (indexing starts from 0)
                fourth_bit = int(x4[3])
                if y2y3y4 == fourth_bit:
                    agreement += 1

            



        cipherText = 0 
       
        print("The result of XORing:", int(plainText ^ K1))
        print("The result of XORing:", bin(int(plainText ^ K1)))
        print("U1:", value1)
        print("U1:", bin(value1))
        
        print("The result of XORing:", int(value1 ^ K2))
        print("The result of XORing:", bin(int(value1 ^ K2)))
        print("U2:", value2)
        print("U2:", bin(value2))
        
        print("The result of XORing:", int(value2 ^ K3))
        print("The result of XORing:", bin(int(value2 ^ K3)))
        print("Cipher Text:", value3)
        print("Cipher Text:", bin(value3))
        
        cipherText = value3
        return cipherText
    
k1 = 3
k2 = 5
k3 = 8
plainText = 11
size = 4
blockCipher = BCIPHER(plainText, size, k1, k2, k3)
cipher = blockCipher.produceCipherText(plainText, size, k1, k2, k3)
print(cipher)



    


 
