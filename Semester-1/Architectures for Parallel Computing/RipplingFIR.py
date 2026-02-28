class SimpleFIRRippling:
    def __init__(self, coefficients):
        self.coeffs = coefficients
        self.registers = [0.0] * len(coefficients)

    def process_sample(self, x):
        # Shift registers to the right
        for i in range(len(self.registers) - 1, 0, -1):
            self.registers[i] = self.registers[i-1]

            # Update the first register with the new input
        self.registers[0] = float(x)

            # Calculate output
        y_out = 0.0
        for i in range(len(self.coeffs)):
            y_out += self.coeffs[i] * self.registers[i]

        return y_out

def run_demo():
    coeffs = [1, 2, 3] 
    fir = SimpleFIRRippling(coeffs)
    input_signal = [1, 1, 1, 1, 0]

    print(f"Filter Coefficients: {coeffs}")
    print(f"Input Signal:        {input_signal}")
    print("-" * 50)
    print("Step-by-Step Execution:")
    print("-" * 50)

    for i, x in enumerate(input_signal):
        y = fir.process_sample(x)
        
        print(f"Time {i}: Input x = {x}  -->  Output y = {y}")
        print(f"        Internal Registers: {fir.registers}")

if __name__ == "__main__":
    run_demo()