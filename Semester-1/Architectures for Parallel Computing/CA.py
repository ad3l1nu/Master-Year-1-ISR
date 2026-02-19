import numpy as np

rule = int(input("Regula (0-255): "))
rule_binary = format(rule, '08b')
print(f"Regula {rule}: {rule_binary}\n")

v = np.zeros(100, dtype=int)
v[50] = 1

for _ in range(50):
    for x in v:
        print('#' if x else ' ', end='')
    print()
    new_v = np.zeros(100, dtype=int)
    for i in range(1, 99):
        pattern = 4 * v[i-1] + 2 * v[i] + v[i+1]
        new_v[i]= int(rule_binary[7 - pattern])
    v = new_v