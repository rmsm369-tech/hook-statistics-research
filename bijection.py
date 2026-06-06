def conjugate(part):
    if not part:
        return []
    return [sum(1 for r in part if r >= k) for k in range(1, part[0] + 1)]

def is_self_conjugate(part):
    return list(part) == conjugate(list(part))

def hooks_from_self_conjugate(part):
    c = conjugate(list(part))
    hooks = []
    for i in range(len(part)):
        if i < part[i]:
            hook_size = part[i] + c[i] - 2*i - 1
            hooks.append(hook_size)
    return sorted(hooks, reverse=True)

def gen_partitions(n):
    def helper(n, max_val):
        if n == 0:
            yield []
            return
        for k in range(min(n, max_val), 0, -1):
            for rest in helper(n - k, k):
                yield [k] + rest
    return helper(n, n)

def distinct_odd_parts(n):
    results = []
    def build(remaining, max_odd, current):
        if remaining == 0:
            results.append(current[:])
            return
        start = max_odd if max_odd % 2 == 1 else max_odd - 1
        for k in range(start, 0, -2):
            if k <= remaining:
                current.append(k)
                build(remaining - k, k - 2, current)
                current.pop()
    start = n if n % 2 == 1 else n - 1
    build(n, start, [])
    return results

max_n = int(input("Enter max n: "))

print("=== Bijection: Self-Conjugate <-> Distinct Odd Parts ===\n")

for n in range(1, max_n + 1):
    sc_parts = [list(p) for p in gen_partitions(n) if is_self_conjugate(list(p))]
    do_parts = distinct_odd_parts(n)

    print(f"n={n}:")
    print(f"  Self-conjugate partitions: {sc_parts}")
    for p in sc_parts:
        hooks = hooks_from_self_conjugate(p)
        print(f"    {p} -> hooks: {hooks}")
    print(f"  Distinct odd parts: {do_parts}")
    print(f"  Counts match: {len(sc_parts) == len(do_parts)}")
    print()