def compute_partitions(max_n):
    coeffs = [0] * (max_n + 1)
    coeffs[0] = 1
    
    for k in range(1, max_n + 1):
        for i in range(k, max_n + 1):
            coeffs[i] += coeffs[i - k]
    
    return coeffs

result = compute_partitions(10)

for n in range(1, 8):
    print(f"p({n}) = {result[n]}")
    
def compute_odd_partitions(max_n):
    coeffs = [0] * (max_n + 1)
    coeffs[0] = 1
    
    for k in range(1, max_n + 1, 2):  # only odd k: 1,3,5,7...
        for i in range(k, max_n + 1):
            coeffs[i] += coeffs[i - k]
    
    return coeffs

odd = compute_odd_partitions(10)

print("\n--- Euler's Theorem Check ---")
for n in range(1, 8):
    print(f"n={n}: p_odd={odd[n]}")

def compute_distinct_partitions(max_n):
    coeffs = [0] * (max_n + 1)
    coeffs[0] = 1
    
    for k in range(1, max_n + 1):  # each part used at most once
        for i in range(max_n, k - 1, -1):  # loop backwards = distinct
            coeffs[i] += coeffs[i - k]
    
    return coeffs

distinct = compute_distinct_partitions(10)

print("\n--- Euler's Theorem PROOF ---")
print(f"{'n':<5} {'p_odd':<10} {'p_distinct':<10} {'Equal?'}")
for n in range(1, 8):
    print(f"{n:<5} {odd[n]:<10} {distinct[n]:<10} {odd[n] == distinct[n]}")