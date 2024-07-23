class LFSR:
    def __init__(self, size=0, initial_state=0, tap_sequence=[]):
        self.size = size
        self.state = initial_state & ((1 << size) - 1)
        self.tap_sequence = tap_sequence

    def set_size(self, size):
        self.size = size
        self.state = self.state & ((1 << size) - 1)

    def get_size(self):
        return self.size

    def set_initial_state(self, initial_state):
        self.state = initial_state & ((1 << self.size) - 1)

    def get_initial_state(self):
        return self.state

    def set_tap_sequence(self, tap_sequence):
        self.tap_sequence = tap_sequence

    def get_tap_sequence(self):
        return self.tap_sequence

    def get_next_bit1(self):
        feedback_bit = 0
        for tap_bit in self.tap_sequence:
            feedback_bit ^= (self.state >> tap_bit) & 1
        self.state = (self.state >> 1) | (feedback_bit << (self.size - 1))
        return feedback_bit
    
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
    
lfsr = LFSR(size=3, initial_state = 3, tap_sequence={1, 2})
stream = lfsr.generate_stream(4)
print(stream)
