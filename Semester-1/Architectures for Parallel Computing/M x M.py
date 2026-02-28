def systolic_matrix_mul_simple(A, B):
    n, p, m = len(A), len(A[0]), len(B[0])
    
    # Matricea rezultat C si registrele interne
    C = [[0]*m for _ in range(n)]
    regA = [[0]*m for _ in range(n)]
    regB = [[0]*m for _ in range(n)]

    # Timpul total necesar traversarii
    timp_total = n + m + p

    print(f"Simulare {n}x{p} * {p}x{m} ({timp_total} pasi)")

    for t in range(timp_total):
        print(f"\n[Pas t={t}]")
        
        # 1. Calcul (Procesare Paralela)
        for i in range(n):
            for j in range(m):
                val_a, val_b = regA[i][j], regB[i][j]
                if val_a and val_b:
                    C[i][j] += val_a * val_b
                    print(f"  P({i},{j}): {val_a}*{val_b} => C={C[i][j]}")

        # 2. Fluxul Datelor (Shiftare)
        
        # A curge spre dreapta
        for i in range(n):
            for j in range(m-1, 0, -1): 
                regA[i][j] = regA[i][j-1]
            # Intrare noua A (cu intarziere i)
            k = t - i
            regA[i][0] = A[i][k] if 0 <= k < p else 0

        # B curge in jos
        for j in range(m):
            for i in range(n-1, 0, -1): 
                regB[i][j] = regB[i-1][j]
            # Intrare noua B (cu intarziere j)
            k = t - j
            regB[0][j] = B[k][j] if 0 <= k < p else 0

    return C

# Date
A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
B = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]

# Rulare
Rezultat = systolic_matrix_mul_simple(A, B)

print("\n--- Rezultat Final ---")
for linie in Rezultat:
    print(linie)