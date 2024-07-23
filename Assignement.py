from typing import Dict, List

class DCIPHER:
    def __init__(self, size: int =8):
        # size in bits
        self.size = size
        # Definition of the sbox  
        self.Sbox: Dict[int, int] = {
            0 : 14,
            1 : 4,
            2 : 13,
            3 : 1,
            4 : 2,
            5 : 15,
            6 : 11,
            7 : 8,
            8 : 3,
            9 : 10,
            10 : 6,
            11 : 12,
            12 : 5,
            13 : 9,
            14 : 0,
            15 : 7,
        }
        
    def set_size(self, size):
        self.size = size
        self.state = self.state

    def get_size(self):
        return self.size
    
    def get_Sbox(self):
        return self.Sbox.items()
    
    def plaintext_perms(self):
        """
        Returns:
        list: A list of integers representing all possible plaintext permutations.
        """
        list = range(0, 2**self.size)
        return list
    
    def int_list_to_binary(self, int_list):
        """
        Converts a list of integers into their binary representation.
        Args:
        int_list (List[int]): A list of integers to be converted to binary.
        Returns:
        List[str]: A list of strings representing binary values of the input integers.
        """
        binary_list: List = [format(num, '08b') for num in int_list]
        return binary_list
        
    
    def through_Sbox(self, input_bits):
        """
        Perform substitution through the S-box.
        Args:
        input_bits (int): An integer representing input bits to the S-box.
        Returns:
        int: An integer representing output bits after substitution through the S-box.
        """
        # Split the 8 bits into two 4-bit groups
        group1 = input_bits >> 4
        group2 = input_bits & 0b1111

        # Lookup values for each 4-bit group in the S-box
        output_group1 = self.Sbox[group1]
        output_group2 = self.Sbox[group2]

        # Rearrange the 4-bit outputs into an 8-bit output
        output_bits = (output_group1 << 4) | output_group2

        return output_bits
    
    def through_inverse_Sbox(self, input_bits):
        # Split the 8 bits into two 4-bit groups
        group1 = input_bits >> 4
        group2 = input_bits & 0b1111
        
        #inverse the Sbox
        inverted_Sbox = {value: key for key, value in self.Sbox.items()}
        
        # Lookup values for each 4-bit group in the S-box
        output_group1 = inverted_Sbox[group1]
        output_group2 = inverted_Sbox[group2]

        # Rearrange the 4-bit outputs into an 8-bit output
        output_bits = (output_group1 << 4) | output_group2

        return output_bits
    
    def rearrange_bits(self, input_bits):
        """
    Rearranges the 8 bits according to the described pattern/permutation after the s-box.
    Args:
    input_bits (int): An integer representing an 8-bit value.
    Returns:
    int: An integer representing the rearranged 8-bit pattern based on the described positions.
    """
    # Rearrange the 8 bits according to the described pattern
        output_bits =(((input_bits & 0b00000001)) |  # Bit 0 stayes at position 0
        ((input_bits & 0b00000010) << 1) |  # Bit 1 moves to position 2
        ((input_bits & 0b00000100) << 2) |  # Bit 2 moves to position 4
        ((input_bits & 0b00001000) << 3) |  # Bit 3 moves to position 6
        ((input_bits & 0b00010000) >> 3) |  # Bit 4 moves to position 1
        ((input_bits & 0b00100000) >> 2) |  # Bit 5 moves to position 3
        ((input_bits & 0b01000000) >> 1) |  # Bit 6 moves to position 5
        ((input_bits & 0b10000000)))        # Bit 7 stayes at position 7
        return output_bits
    
    def cipher_single_run(self, plaintext, key_1, key_2, key_3, key_4, in_binary, mapped):
        mapping_dic = {}
        result = None
        
        U_1 = plaintext ^ key_1
        V_1 = self.rearrange_bits(self.through_Sbox(U_1))
        U_2 = V_1 ^ key_2
        V_2 = self.rearrange_bits(self.through_Sbox(U_2))
        U_3 = V_2 ^ key_3
        V_3 = self.through_Sbox(U_3)
        U_4 = V_3 ^ key_4
        
        if in_binary == True:
            ciphertext = bin(U_4)
        else:
            ciphertext = U_4
            
        if mapped == True:
            # Combine the lists into a dictionary using zip() and a dictionary comprehension
            if  in_binary == True:
                mapping_dic = {bin(plaintext): ciphertext}
            else:
                mapping_dic = {plaintext: ciphertext}
                
            result = mapping_dic
            
        else:
            result =  ciphertext
            
        return result
    
    def cipher_all_perms(self, key_1, key_2, key_3, key_4, in_binary, mapped):
        """
    Generate ciphertext for all possible plaintext permutations using the given keys.
    in_binary: False && mapped: True, those values must be set like this when used to -
    produce the pairs for the de_cipher function.
    Args:
    key_1 (int): First key value.
    key_2 (int): Second key value.
    key_3 (int): Third key value.
    key_4 (int): Fourth key value.
    in_binary (bool): Boolean indicating whether the output should be in binary format.
    mapped (bool): Boolean indicating whether to return the results as a dictionary.
    Returns:
    Union[Dict, List]: Returns a dictionary mapping plaintext to ciphertext if mapped=True,
                       otherwise returns a list of ciphertext values.
    """
        plaintext_perms = self.plaintext_perms()
        ciphertext_list = []
        p_c_mapping = {}
        result = None
        
        # Encryption process for each plaintext permutation
        for plaintext in plaintext_perms:
            # First round encryption
            U_1 = plaintext ^ key_1
            V_1 = self.rearrange_bits(self.through_Sbox(U_1))
            # Second round encryption
            U_2 = V_1 ^ key_2
            V_2 = self.rearrange_bits(self.through_Sbox(U_2))
            # Third round encryption
            U_3 = V_2 ^ key_3
            V_3 = self.through_Sbox(U_3)
            # Final round encryption
            U_4 = V_3 ^ key_4
            
            # Format ciphertext based on the 'in_binary' argument
            if in_binary == True:
                ciphertext = format(U_4, '08b')
            else:
                ciphertext = U_4
            ciphertext_list.append(ciphertext)
            
            # Format result as a dictionary if 'mapped' is True
            if mapped == True:
                # Combine the lists into a dictionary using zip() and a dictionary comprehension
                if in_binary == True:
                    p_c_mapping = {k: v for k, v in zip(self.int_list_to_binary(plaintext_perms), ciphertext_list)}
                else:
                     p_c_mapping = {k: v for k, v in zip(plaintext_perms, ciphertext_list)}
                result = p_c_mapping
            else:
                result =  ciphertext_list  
        return result
    
    def input_output_diff_pairs(self, plain_cipher_pairs, target_input_diff):
        """
        Extracts pairs of plaintexts and corresponding ciphertexts that produce a specific input difference.
        Args:
        - plain_cipher_pairs (dict): A dictionary with plaintext-ciphertext pairs.
        - target_input_diff (int): The desired input difference to search for obtained from cipher approximation.
        Returns:
        - dict: A dictionary containing pairs of plaintexts matching 
        the desired input differences along with their pairs of ciphertexts.
        """
        input_output_diffs = {}
        # Iterate through each plaintext pair and their corresponding ciphertext pair
        for plain1, cipher1 in plain_cipher_pairs.items():
            for plain2, cipher2 in plain_cipher_pairs.items():
                    # Calculate input difference by XORing the pair of plaintexts
                    input_diff = plain1 ^ plain2
                    # Check if the input difference matches the target input difference
                    if input_diff == target_input_diff:
                        # Store plaintext pair with matching the target input differences along 
                        # with their corresponding ciphertext pair
                        input_output_diffs[(plain1, plain2)] = (cipher1, cipher2) 
        return input_output_diffs
    
    
    def de_cipher(self, P_C_pairs, target_key_bits_perms, target_intermediate_value, in_binary):
        """
        Decipher function to recover a subkey based on the given pairs of plaintext and ciphertext.
        Args:
        P_C_pairs (Dict[Tuple[int, int], Tuple[int, int]]): Dictionary of plaintext-ciphertext pairs.
        target_key_bits_perms (range): Range of possible subkey values.
        target_intermediate_value (int): Expected intermediate value for the differential characteristic.
        in_binary (bool): Boolean indicating whether the output should be in binary format.
        Returns:
        Union[Dict, int]: Returns a dictionary mapping probability to the recovered subkey if in_binary=True,
                        otherwise returns the recovered subkey as an integer.
        """
        # Initialize variables and dictionaries
        count = 0
        key_prob_dic: Dict[int, float] = {}
        prob_recovered_key_dic = {}
        length = len(P_C_pairs)
        max_prob_subkey = 0
        result = None
        
        # Iterate through possible subkey values
        for subkey in target_key_bits_perms:
            # For each subkey, check against all plaintext-ciphertext pairs
            for plaintext, ciphertext in P_C_pairs.items():
                # Decrypt the ciphertext using the subkey and compute intermediate value
                ciphertext1, ciphertext2 = ciphertext
                Vi_ciphertext_1 = ciphertext1 ^ subkey
                Vi_ciphertext_2 = ciphertext2 ^ subkey
                Ui_ciphertext_1 = self.through_inverse_Sbox(Vi_ciphertext_1)
                Ui_ciphertext_2 = self.through_inverse_Sbox(Vi_ciphertext_2)
                delta_Ui = Ui_ciphertext_1 ^ Ui_ciphertext_2
                # Check if the computed intermediate value matches the expected value
                if delta_Ui == target_intermediate_value:
                    count += 1
                    
            # Calculate probability of the subkey being correct based on count
            key_prob_dic[subkey] = (count/length)
            #print(f"Subkey: {subkey}, Count: {count}, Probability: {key_prob_dic[subkey]}")
            count = 0
        # Find the subkey with the highest probability
        max_prob = max(key_prob_dic.values())  # Get the maximum value in the dictionary
        
        for key, prob in key_prob_dic.items():  
            if prob == max_prob:
                max_prob_subkey = key  # Get the key corresponding to the maximum value     
        
        # Format the result based on the 'in_binary' argument
        if in_binary == True:
            prob_recovered_key_dic[max_prob] = format(max_prob_subkey, '08b')
            result = prob_recovered_key_dic
        else:
            prob_recovered_key_dic[max_prob] = max_prob_subkey
            result = prob_recovered_key_dic   
        return result
    
    
        
cipher_class = DCIPHER(8) # Create an instance of the DCIPHER class

# Generate plaintext-ciphertext pairs for all permutations
plain_cipher_pairs = cipher_class.cipher_all_perms(84, 50, 35, 69, False, True)

# Find input-output difference pairs with a target input difference of 11
input_output_pairs = cipher_class.input_output_diff_pairs(plain_cipher_pairs, 11)

# Decrypt the ciphertexts using the found input-output difference pairs
de_cipher_result = cipher_class.de_cipher(input_output_pairs, range(0, 2**8), 20, True)

# Extract the key and its associated probability from the result
key = next(iter(de_cipher_result))
# Display the recovered key along with its probability
print("Actual Key = 69\n")
print(f"Highest probability: {key:<2} ==> Recovered Key: {de_cipher_result[key]:<7}")




"""
#Code to neatly print the first 64 plaintext_ciphertext pairs
counter = 1
items = list(plain_cipher_pairs.items())[:64]
for i in range(32):
    key1, value1 = items[i]
    key2, value2 = items[i + 32] if i + 32 < len(items) else ('', '')  # Handling the case where the last pair is incomplete
    
    output_line = f"Num: {counter:<2}, plaintext: {str(key1):<7} ==> ciphertext: {str(value1):<12} | " \
                  f"Num: {counter + 32:<2}, plaintext: {str(key2):<7} ==> ciphertext: {str(value2):<12}"
    print(output_line)
    counter += 1
"""



    


