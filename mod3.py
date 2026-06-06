import matplotlib.pyplot as plt
from partitions import compute_partitions

def mod3_split(max_n):
    p = compute_partitions(max_n)
    
    S1_n = []  # n ≡ 1 or 2 mod 3
    S1_p = []
    S2_n = []  # n ≡ 0 mod 3
    S2_p = []
    delta_n = []
    delta_v = []

    for n in range(1, max_n + 1):
        if n % 3 == 1 or n % 3 == 2:
            S1_n.append(n)
            S1_p.append(p[n])
        else:
            S2_n.append(n)
            S2_p.append(p[n])
        
        delta_n.append(n)
        delta_v.append(p[n] - (p[n-1] if n > 1 else 0))

    return p, S1_n, S1_p, S2_n, S2_p, delta_n, delta_v

max_n = int(input("Enter max n: "))
p, S1_n, S1_p, S2_n, S2_p, delta_n, delta_v = mod3_split(max_n)

# Print table
print(f"\n{'n':<5} {'n mod 3':<10} {'p(n)':<8} {'S1/S2'}")
for n in range(1, max_n + 1):
    group = "S1" if n % 3 != 0 else "S2"
    print(f"{n:<5} {n % 3:<10} {p[n]:<8} {group}")

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(S1_n, S1_p, 'bo-', label='S1 (n≡1,2 mod 3)')
ax1.plot(S2_n, S2_p, 'rs-', label='S2 (n≡0 mod 3)')
ax1.set_title('Partition counts: S1 vs S2')
ax1.set_xlabel('n')
ax1.set_ylabel('p(n)')
ax1.legend()
ax1.grid(True)

ax2.bar(delta_n, delta_v, color='purple', alpha=0.7)
ax2.set_title('Delta(n) = p(n) - p(n-1)')
ax2.set_xlabel('n')
ax2.set_ylabel('Delta')
ax2.grid(True)

plt.tight_layout()
plt.show()