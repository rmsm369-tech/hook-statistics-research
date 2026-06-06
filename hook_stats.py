import matplotlib.pyplot as plt

def conjugate(part):
    if not part:
        return []
    return [sum(1 for r in part if r >= k) for k in range(1, part[0] + 1)]

def is_self_conjugate(part):
    return list(part) == conjugate(list(part))

def all_hooks(part):
    c = conjugate(list(part))
    hooks = []
    for i in range(len(part)):
        for j in range(part[i]):
            hook = (part[i] - j - 1) + (c[j] - i - 1) + 1
            hooks.append(hook)
    return hooks

def mean_hook(part):
    h = all_hooks(part)
    return sum(h) / len(h)

def gen_partitions(n):
    def helper(n, max_val):
        if n == 0:
            yield []
            return
        for k in range(min(n, max_val), 0, -1):
            for rest in helper(n - k, k):
                yield [k] + rest
    return helper(n, n)

max_n = int(input("Enter max n: "))

print(f"\n{'n':<5} {'avg H(all)':<15} {'avg H(sc)':<15} {'diff'}")
print("-" * 45)

all_avgs = []
sc_avgs = []
ns = []

for n in range(2, max_n + 1):
    parts = list(gen_partitions(n))
    
    all_means = [mean_hook(list(p)) for p in parts]
    sc_means = [mean_hook(list(p)) for p in parts if is_self_conjugate(list(p))]
    
    avg_all = sum(all_means) / len(all_means)
    avg_sc = sum(sc_means) / len(sc_means) if sc_means else 0
    
    diff = avg_sc - avg_all
    
    print(f"{n:<5} {avg_all:<15.4f} {avg_sc:<15.4f} {diff:.4f}")
    
    all_avgs.append(avg_all)
    sc_avgs.append(avg_sc)
    ns.append(n)

plt.figure(figsize=(12, 5))
plt.plot(ns, all_avgs, 'b-o', markersize=4, label='avg H — all partitions')
plt.plot(ns, sc_avgs, 'r-s', markersize=4, label='avg H — self-conjugate only')
plt.title('Mean hook length: all partitions vs self-conjugate')
plt.xlabel('n')
plt.ylabel('mean hook length')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('figure2_hook_stats.png', dpi=300, bbox_inches='tight')
plt.show()
print(f"\nLast 5 diffs: {[round(sc_avgs[i]-all_avgs[i],4) for i in range(-5,0)]}")