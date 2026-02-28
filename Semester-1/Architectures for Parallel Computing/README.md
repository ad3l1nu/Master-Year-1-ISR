# Architectures for Parallel Computing

This folder contains implementations of various parallel computing architectures and algorithms, demonstrating different parallel processing patterns and optimization techniques.

---

## 📋 File Descriptions

### 1. **BroadcastFIR.py**

**Purpose**: Implements a **Broadcast Finite Impulse Response (FIR) Filter** architecture.

**What it does**:
- Creates a parallel FIR filter where the input signal is simultaneously broadcast to all processing elements
- Uses internal shift registers to maintain filter state
- Processes one sample at a time, with all coefficients being applied in parallel to the same input value
- Updates registers in a cascading manner where each register receives contributions from both the previous register and the input

**Key Features**:
- Broadcasting pattern for data distribution
- Parallel coefficient application
- Sequential processing of input samples
- Internal register management for state

**Example Usage**:
```bash
python BroadcastFIR.py
```

Demonstrates filtering [1, 1, 1, 1, 0] with coefficients [1, 2, 3]

---

### 2. **RipplingFIR.py**

**Purpose**: Implements a **Rippling/Shifting Finite Impulse Response (FIR) Filter** architecture.

**What it does**:
- Creates an FIR filter using the rippling (array shift) method
- New input samples are loaded at the first register and propagate through the array
- Unlike broadcast, this uses a sequential shift pattern where registers contain historical input values
- The output is computed by multiplying each coefficient with its corresponding register value

**Key Features**:
- Shift register data flow pattern
- History buffer for past input samples
- Linear convolution operation
- First-in, first-out data propagation

**Example Usage**:
```bash
python RipplingFIR.py
```

Demonstrates filtering [1, 1, 1, 1, 0] with coefficients [1, 2, 3]

---

### 3. **CA.py**

**Purpose**: Implements **Elementary Cellular Automaton** (Rule-based evolution).

**What it does**:
- Simulates 1D cellular automata with Wolfram's rule notation (0-255)
- Each rule defines how cells evolve based on their neighborhood (left, center, right)
- Starts with a single live cell in the middle and evolves over 50 generations
- Visualizes the evolution with '#' for alive cells and spaces for dead cells

**Key Features**:
- Rule parameterization (0-255)
- Parallel state transitions across all cells
- Visual grid output
- Self-organizing patterns based on simple local rules

**Example Usage**:
```bash
python CA.py
```
Enter a rule number between 0-255 when prompted (e.g., rule 30 creates famous Sierpinski patterns)

**Common Rules**:
- Rule 30: Chaotic pattern (famous for fine structure)
- Rule 110: Complex behavior, potentially universal computation
- Rule 184: Traffic flow patterns
- Rule 90: XOR rule, creates Sierpinski triangle

---

### 4. **GoL.py**

**Purpose**: Implements **Conway's Game of Life** - a cellular automaton demonstrating self-organization.

**What it does**:
- Simulates Conway's Game of Life on a 30x30 grid
- Applies four rules in parallel to determine cell state transitions:
  - Live cell with 2-3 neighbors survives
  - Dead cell with exactly 3 neighbors becomes alive
  - All other cells die or stay dead
- Continuously animates the evolution
- Displays '#' for live cells and spaces for dead cells

**Key Features**:
- Parallel neighborhood computation
- Self-organizing complex patterns
- Real-time visualization
- Emergent behavior from simple rules
- Continues until interrupted (Ctrl+C)

**Example Usage**:
```bash
python GoL.py
```

Watch for emergent patterns:
- **Still lifes**: Stable configurations (blocks, beehives, loaves)
- **Oscillators**: Repeating cycles (blinkers, toads, pulsar)
- **Spaceships**: Patterns that move across the grid (gliders)

---

### 5. **M x M.py**

**Purpose**: Implements **Systolic Array for Matrix Multiplication** - a specialized parallel architecture.

**What it does**:
- Simulates a systolic array architecture for multiplying two matrices (n×p) × (p×m)
- Uses a grid of processing elements (PE) that work in parallel
- Data flows through the array: matrix A flows right, matrix B flows down
- Each PE computes partial products and accumulates results
- Requires O(n + p + m) time steps to complete multiplication

**Key Features**:
- Systolic data flow pattern
- Synchronized parallel computation
- Register-based intermediate storage
- Demonstrates data locality and reuse
- Efficient hardware implementation suitable for VLSI

**Algorithm Flow**:
1. Elements of A enter from the left and flow rightward
2. Elements of B enter from the top and flow downward
3. Each PE multiplies its local data and accumulates
4. Results gradually fill the output matrix

**Example Usage**:
```bash
python "M x M.py"
```

Multiplies:
- A = 3×3 matrix [1,2,3; 4,5,6; 7,8,9]
- B = 3×3 matrix [1,0,0; 0,2,0; 0,0,3]
- Displays step-by-step computation and final result

---

## 🎯 Parallel Computing Patterns Demonstrated

| File | Pattern | Communication | Data Flow |
|------|---------|---|---|
| BroadcastFIR | Broadcast | One-to-many | Scattered input |
| RipplingFIR | Pipeline | Sequential | Shift/ripple |
| CA | Cellular | Local neighborhood | No global sync |
| GoL | Cellular | Local neighborhood | Synchronous rounds |
| M x M | Systolic | Local | Controlled streaming |

---

## 💡 Key Concepts

- **Parallelism**: Multiple operations executed simultaneously
- **Data Flow**: How data moves through the architecture
- **Synchronization**: Coordination between processing elements
- **Hardware Efficiency**: Trade-offs between latency, throughput, and resource usage

---

## 🚀 Running the Examples

All scripts can be run directly with Python:

```bash
python BroadcastFIR.py
python RipplingFIR.py
python CA.py
python GoL.py
python "M x M.py"
```

---

## 📚 Further Reading

- **Cellular Automata**: Stephen Wolfram's "A New Kind of Science"
- **Systolic Arrays**: H.T. Kung and Charles E. Leiserson papers
- **FIR Filters**: Digital Signal Processing fundamentals
- **Conway's Game of Life**: Classic reference on emergence and complexity
