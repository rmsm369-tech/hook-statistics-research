import math
import time

def count_t_hooks_in_sc(odd_parts, t):
    if not odd_parts: return 0
    
    # 1. Map distinct odd parts to Frobenius arm lengths
    a = [(p - 1) // 2 for p in odd_parts]
    
    # 2. Build the exact 2D shape array (number of cells in each row)
    shape = [0] * (a[0] + 1)
    for i, arm in enumerate(a):
        shape[i] = arm + i + 1
    for i, arm in enumerate(a):
        for j in range(i + 1, i + 1 + arm):
            shape[j] += 1
            
    # 3. Literally count the hooks of length t
    hooks = 0
    for r, row_len in enumerate(shape):
        for c in range(row_len):
            # Hook length = (cells right) + (cells below) + 1
            # Since it's self-conjugate, col_length == row_length for mirrored indices
            if row_len - c + shape[c] - r - 1 == t:
                hooks += 1
    return hooks

def verify_range(start_n, end_n, t=1):
    # Blazing fast memory-efficient generator for distinct odd parts
    def generate_odd_distinct(n, max_val):
        if n == 0:
            yield []
        else:
            for v in range(min(n, max_val | 1), 0, -2):
                for rest in generate_odd_distinct(n - v, v - 2):
                    yield [v] + rest

    for n in range(start_n, end_n + 1):
        total_hooks = 0
        count = 0
        
        # Generate and count exactly
        for odd_parts in generate_odd_distinct(n, n if n % 2 != 0 else n - 1):
            total_hooks += count_t_hooks_in_sc(odd_parts, t)
            count += 1
            
        if count == 0: continue
        
        avg = total_hooks / count
        # The exact unrestricted Craig-Ono-Singh theoretical limit
        theory = (math.sqrt(6 * n) / math.pi) - (t / 2) + (3 / math.pi**2) + (1/4 if t % 2 != 0 else 0)
        scaled_error = (avg - theory) * math.sqrt(n)
        
        print(f"n={n:3d} | Avg={avg:.4f} | Scaled Err={scaled_error:.5f}")

if __name__ == "__main__":
    start = time.time()
    print("--- Exact Literal t-Hook Enumeration (Claude's Verification) ---")
    # Pushing past the n=60 barrier to n=100
    verify_range(60, 100, t=1)
    print(f"\nCompleted in {time.time() - start:.2f} seconds.")
