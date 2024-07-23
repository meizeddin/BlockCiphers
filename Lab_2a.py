class LFSR:
    def __init__(self, size=0, initial_state=0, tap_sequence=[]):
        self.size = size
        self.state = initial_state & ((1 << size) - 1)
        self.tap_sequence = tap_sequence
        self.initialState = initial_state & ((1 << size) - 1)

    def set_size(self, size):
        self.size = size
        self.state = self.state & ((1 << size) - 1)

    def get_size(self):
        return self.size

    def set_initial_state(self, initial_state):
        self.state = initial_state & ((1 << self.size) - 1)

    def get_initial_state(self):
        return self.state
    
    def get_State(self):
        return self.initialState

    def set_tap_sequence(self, tap_sequence):
        self.tap_sequence = tap_sequence

    def get_tap_sequence(self):
        return self.tap_sequence

    def get_next_bit(self):
        feedback_bit = 0
        for tap_bit in self.tap_sequence:
            feedback_bit ^= (self.state >> tap_bit) & 1

        # Right shift the state, and set the leftmost bit to the feedback bit
        rightmost_bit = self.state & 1
        self.state = (self.state >> 1) | (feedback_bit << (self.size - 1))
        return rightmost_bit

    def generate_stream(self, length):
        stream = []
        for _ in range(length):
            stream.append(self.get_next_bit())
        return stream

def perms(n):
    if not n:
      return
    for i in range(1, 2**n):
      yield i

def finalReg(x1, x2, x3):
    list = []
    for i in range(2000):
        if x1[i]:
            list.append(x2[i])
        else:
            list.append(x3[i])
    return list


# Example:
def lfsrAttack(filePath, streamSize, lfsrLength, tapSequence):

    agreement = 0
    highestAgreement= 0
    permutations = list(perms(lfsrLength))
    best_lfsr = None
    result = ""
    
    with open(filePath, "r") as file:
        known_keystream = [int(bit) for bit in file.read().split()]

    for state in permutations:
        agreement = 0
        lfsr = LFSR(size= lfsrLength, initial_state = int(state), tap_sequence= tapSequence)
        stream = lfsr.generate_stream(streamSize)
        for j in range(streamSize):
            if stream[j] == known_keystream[j]:
                        agreement += 1
        if (highestAgreement < agreement):
            highestAgreement = agreement            
            best_lfsr = lfsr
        
    if best_lfsr:

        result = (f"Highest Agreement: {highestAgreement}\n"
    f"Percentage Match: {(highestAgreement / streamSize) * 100:.2f}%\n"
    f"Tap Sequence: {best_lfsr.get_tap_sequence()}\n"
    f"Initial State: {format(best_lfsr.get_State(), f'0{best_lfsr.get_size()}b')}\n"
    f"Initial State Int: {best_lfsr.get_State()}")

    return result


print(lfsrAttack("StreamFile.txt", 2000, 11, {0,9}))
#Highest Agreement: 1498
#Percentage Match: 74.9
#Tap Sequence: {0, 9}
#Initial State: 00101101101
#Initial State Int: 365
print(lfsrAttack("StreamFile.txt", 2000, 13, {0,9,10,12}))
#Highest Agreement: 1504
#Percentage Match: 75.2
#Tap Sequence: {0, 9, 10, 12}
#Initial State: 1110011110101
#Initial State Int: 7413

lfsr2 = LFSR(size=11, initial_state = 365, tap_sequence={0, 9})
stream2 = lfsr2.generate_stream(2000)

lfsr3 = LFSR(size=13, initial_state = 7413, tap_sequence={0, 9, 10, 12})
stream3 = lfsr3.generate_stream(2000)

def finalLfsrAttck(filePath, streamSize, lfsrLength, tapSequence, stream2, stream3):

    agreement = 0
    highestAgreement= 0
    permutations = list(perms(lfsrLength))
    best_lfsr1 = None
    result = ""

    with open(filePath, "r") as file:
        known_keystream = [int(bit) for bit in file.read().split()]

    for state in permutations:
        agreement = 0
        lfsr1 = LFSR(size= lfsrLength, initial_state = int(state), tap_sequence= tapSequence)
        stream1 = lfsr1.generate_stream(streamSize)
        for j in range(streamSize):
            newStream = list(finalReg(stream1, stream2, stream3))
            if newStream[j] == known_keystream[j]:
                        agreement += 1
        if (highestAgreement < agreement):
            highestAgreement = agreement            
            best_lfsr1 = lfsr1

    if best_lfsr1:

        result = (f"Highest Agreement: {highestAgreement}\n"
    f"Percentage Match: {(highestAgreement / streamSize) * 100:.2f}%\n"
    f"Tap Sequence: {best_lfsr1.get_tap_sequence()}\n"
    f"Initial State: {format(best_lfsr1.get_State(), f'0{best_lfsr1.get_size()}b')}\n"
    f"Initial State Int: {best_lfsr1.get_State()}")

    return result

print(finalLfsrAttck("StreamFile.txt", 2000, 7, {0,6}, stream2, stream3 ))





    
