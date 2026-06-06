import matplotlib.pyplot as plt

def compute_all(max_n):
    # p(n) unrestricted
    p = [0] * (max_n + 1)
    p[0] = 1
    for k in range(1, max_n + 1):
        for i in range(k, max_n + 1):
            p[i] += p[i - k]

    # p_odd
    odd = [0] * (max_n + 1)
    odd[0] = 1
    for k in range(1, max_n + 1, 2):
        for i in range(k, max_n + 1):
            odd[i] += odd[i - k]

    # p_distinct
    distinct = [0] * (max_n + 1)
    distinct[0] = 1
    for k in range(1, max_n + 1):
        for i in range(max_n, k - 1, -1):
            distinct[i] += distinct[i - k]

    # self conjugate
    def conjugate(part):
        if not part:
            return []
        return [sum(1 for r in part if r >= k) for k in range(1, part[0] + 1)]

    def gen_partitions(n):
        def helper(n, max_val):
            if n == 0:
                yield []
                return
            for k in range(min(n, max_val), 0, -1):
                for rest in helper(n - k, k):
                    yield [k] + rest
        return helper(n, n)

    self_conj = [0] * (max_n + 1)
    for n in range(1, max_n + 1):
        self_conj[n] = sum(
            1 for part in gen_partitions(n)
            if list(part) == conjugate(list(part))
        )

    return p, odd, distinct, self_conj

max_n = int(input("Enter max n (suggest 20): "))
p, odd, distinct, sc = compute_all(max_n)

# Print table
print(f"\n{'n':<6} {'p(n)':<10} {'p_odd':<10} {'p_distinct':<12} {'self_conj'}")
print("-" * 50)
for n in range(1, max_n + 1):
    print(f"{n:<6} {p[n]:<10} {odd[n]:<10} {distinct[n]:<12} {sc[n]}")

# Plot
ns = list(range(1, max_n + 1))
plt.figure(figsize=(12, 6))
plt.plot(ns, [p[n] for n in ns], 'b-o', label='p(n)', markersize=4)
plt.plot(ns, [odd[n] for n in ns], 'r-s', label='p_odd(n)', markersize=4)
plt.plot(ns, [distinct[n] for n in ns], 'g-^', label='p_distinct(n)', markersize=4)
plt.plot(ns, [sc[n] for n in ns], 'm-d', label='self_conjugate(n)', markersize=4)
plt.title('Partition sequences up to n')
plt.xlabel('n')
plt.ylabel('count')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('figure1_partition_sequences.png', dpi=300, bbox_inches='tight')
print("Graph saved as figure1_partition_sequences.png")
plt.show()
print("Graph saved as figure1_partition_sequences.png")