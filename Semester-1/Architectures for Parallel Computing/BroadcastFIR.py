class BroadcastFIR:
    def __init__(self, coefficients):

        self.coeffs = coefficients
        self.registers = [0.0] * len(coefficients)

    def process_sample(self, x):
       
        y_out = self.registers[0] + (self.coeffs[0] * x)
        # Shift registers and update with new input

        for i in range(len(self.registers) - 1):
            # Update each register based on the next one and the input
            self.registers[i] = self.registers[i+1] + (self.coeffs[i+1] * x)

        # Update the last register
        self.registers[-1] = 0 + (self.coeffs[-1] * x)

        return y_out


def run_demo():
    coeffs = [1, 2, 3] 
    fir = BroadcastFIR(coeffs)
    input_signal = [1, 1, 1, 1, 0]

    print(f"Filter Coefficients: {coeffs}")
    print(f"Input Signal:        {input_signal}")
    print("-" * 30)
    print("Step-by-Step Execution:")
    print("-" * 30)

    for i, x in enumerate(input_signal):
        y = fir.process_sample(x)
        print(f"Time {i}: Input x = {x}  -->  Output y = {y}")
        print(f"        Internal Registers: {fir.registers}")

if __name__ == "__main__":
    run_demo()