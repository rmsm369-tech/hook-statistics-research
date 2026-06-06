def generate_partitions(n):
    def helper(n, max_val):
        if n == 0:
            yield []
            return
        for k in range(min(n, max_val), 0, -1):
            for rest in helper(n - k, k):
                yield [k] + rest
    return list(helper(n, n))

def draw_young(partition):
    for row in partition:
        print("■ " * row)
    print()

def conjugate(partition):
    if not partition:
        return []
    max_len = partition[0]
    return [sum(1 for row in partition if row >= k) for k in range(1, max_len + 1)]

def is_self_conjugate(partition):
    return conjugate(partition) == list(partition)

# Ask user
n = int(input("Enter n: "))
partitions = generate_partitions(n)

print(f"\np({n}) = {len(partitions)}")
print(f"=== Young Diagrams of p({n}) ===\n")

self_conjugate_count = 0

for p in partitions:
    print(f"Partition: {p}")
    draw_young(p)
    conj = conjugate(p)
    selfconj = is_self_conjugate(p)
    if selfconj:
        self_conjugate_count += 1
    print(f"Conjugate: {conj}")
    print(f"Self-conjugate: {selfconj}")
    print("-" * 20)

print(f"\n=== SUMMARY ===")
print(f"p({n}) = {len(partitions)}")
print(f"Self-conjugate partitions: {self_conjugate_count}")
print(f"Non self-conjugate: {len(partitions) - self_conjugate_count}")

def distinct_odd_parts(n):
    count = 0
    def helper(n, max_val):
        nonlocal count
        if n == 0:
            count += 1
            return
        for k in range(min(n, max_val), 0, -2 if max_val % 2 == 1 else -1):
            if k % 2 == 1:  # odd only
                helper(n - k, k - 1)  # k-1 forces distinct
    helper(n, n if n % 2 == 1 else n - 1)
    return count

print(f"\n=== FULL COMPARISON TABLE n=1 to 10 ===")
print(f"{'n':<5} {'p(n)':<8} {'p_odd':<8} {'p_distinct':<12} {'self_conj':<12} {'dist_odd':<10} {'SC=DO?'}")

from partitions import compute_partitions, compute_odd_partitions, compute_distinct_partitions

p = compute_partitions(10)
odd = compute_odd_partitions(10)
distinct = compute_distinct_partitions(10)

for n in range(1, 11):
    parts = generate_partitions(n)
    sc = sum(1 for part in parts if is_self_conjugate(part))
    do = distinct_odd_parts(n)
    print(f"{n:<5} {p[n]:<8} {odd[n]:<8} {distinct[n]:<12} {sc:<12} {do:<10} {sc == do}")