import matplotlib.pyplot as plt
import math

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

def gen_partitions(n):
    def helper(n, max_val):
        if n == 0:
            yield []
            return
        for k in range(min(n, max_val), 0, -1):
            for rest in helper(n - k, k):
                yield [k] + rest
    return helper(n, n)

def theory_mean(t, n):
    delta = 1 if t % 2 == 1 else 0
    return math.sqrt(6*n)/math.pi - t/2 + 3/(math.pi**2) + delta/4

max_n = int(input("Enter max n (suggest 60): "))
t_values = [1, 2, 3]
colors = ['blue', 'red', 'green']

# Collect data
data = {}
for t in t_values:
    emp_list, thy_list, diff_list, ns = [], [], [], []
    for n in range(2, max_n + 1):
        sc_parts = [list(p) for p in gen_partitions(n)
                    if is_self_conjugate(list(p))]
        if not sc_parts:
            continue
        counts = [all_hooks(p).count(t) for p in sc_parts]
        emp = sum(counts) / len(counts)
        thy = theory_mean(t, n)
        emp_list.append(emp)
        thy_list.append(thy)
        diff_list.append(emp - thy)
        ns.append(n)
    data[t] = (ns, emp_list, thy_list, diff_list)
    print(f"t={t} done.")

# Figure A: empirical vs theoretical
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Empirical vs Craig-Ono-Singh Asymptotic Mean Hook Count', fontsize=13)

for i, t in enumerate(t_values):
    ns, emp, thy, diff = data[t]
    axes[i].plot(ns, emp, color=colors[i], linewidth=1.5, label=f'Empirical (t={t})')
    axes[i].plot(ns, thy, color=colors[i], linewidth=1.5,
                 linestyle='--', label=f'Asymptotic (t={t})')
    axes[i].set_title(f't={t} ({"odd" if t%2==1 else "even"})')
    axes[i].set_xlabel('n')
    axes[i].set_ylabel('mean hook count')
    axes[i].legend(fontsize=8)
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('figureA_empirical_vs_asymptotic.png', dpi=300, bbox_inches='tight')
# plt.show()

# Figure B: difference curves
plt.figure(figsize=(12, 5))
for t, color in zip(t_values, colors):
    ns, emp, thy, diff = data[t]
    label = f't={t} ({"odd" if t%2==1 else "even"})'
    plt.plot(ns, diff, color=color, linewidth=1.5, label=label)

plt.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
plt.title('Convergence: Empirical minus Asymptotic mean hook count')
plt.xlabel('n')
plt.ylabel('difference')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('figureB_convergence_diff.png', dpi=300, bbox_inches='tight')
# plt.show()

print("\nSaved: figureA_empirical_vs_asymptotic.png")
print("Saved: figureB_convergence_diff.png")