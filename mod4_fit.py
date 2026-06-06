import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import curve_fit

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

def oscillatory_model(n, A, B, C, D):
    return (A + B*np.cos(np.pi*n) + C*np.cos(np.pi*n/2) + D*np.sin(np.pi*n/2)) / np.sqrt(n)

max_n = int(input("Enter max n (suggest 60): "))
t_values = [1, 2, 3]
colors = ['blue', 'red', 'green']

# Collect base data
data = {}
for t in t_values:
    ns, signed = [], []
    for n in range(3, max_n + 1):
        sc_parts = [list(p) for p in gen_partitions(n)
                    if is_self_conjugate(list(p))]
        if not sc_parts:
            continue
        counts = [all_hooks(p).count(t) for p in sc_parts]
        emp = sum(counts) / len(counts)
        thy = theory_mean(t, n)
        ns.append(n)
        signed.append(emp - thy)
    data[t] = {'ns': np.array(ns), 'signed': np.array(signed)}
    print(f"t={t} done.")

# ── TEST: Mod 4 residue split ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Mod 4 Residue Split of Signed Error', fontsize=13)

mod4_colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'purple'}

for i, t in enumerate(t_values):
    d = data[t]
    for r in range(4):
        mask = d['ns'] % 4 == r
        ns_r = d['ns'][mask]
        e_r  = d['signed'][mask]
        if len(ns_r) > 0:
            axes[i].plot(ns_r, e_r, color=mod4_colors[r],
                        linewidth=1.2, marker='o', markersize=3,
                        label=f'n≡{r} mod 4')
    axes[i].axhline(0, color='black', linewidth=0.8)
    axes[i].set_title(f't={t} ({"odd" if t%2==1 else "even"})')
    axes[i].set_xlabel('n')
    axes[i].set_ylabel('signed error')
    axes[i].legend(fontsize=7)
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('mod4_split.png', dpi=300, bbox_inches='tight')
print("Saved: mod4_split.png")

# ── Oscillatory model fit ───────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Oscillatory Model Fit: e(t,n) ≈ (A+B·cos(πn)+C·cos(πn/2)+D·sin(πn/2))/√n',
             fontsize=11)

print("\n=== FITTED CONSTANTS ===")
print(f"{'t':<5} {'A':<10} {'B':<10} {'C':<10} {'D':<10} {'residual'}")
print("-" * 55)

fit_results = {}
for i, t in enumerate(t_values):
    d = data[t]
    ns = d['ns'].astype(float)
    signed = d['signed']

    try:
        popt, pcov = curve_fit(oscillatory_model, ns, signed,
                               p0=[0.5, 0.2, 0.2, 0.2],
                               maxfev=10000)
        A, B, C, D = popt
        fitted = oscillatory_model(ns, *popt)
        residual = np.sqrt(np.mean((signed - fitted)**2))

        print(f"{t:<5} {A:<10.4f} {B:<10.4f} {C:<10.4f} {D:<10.4f} {residual:.4f}")
        fit_results[t] = popt

        axes[i].plot(ns, signed, color=colors[i], alpha=0.4,
                    linewidth=1, label='empirical error')
        axes[i].plot(ns, fitted, color=colors[i], linewidth=2,
                    linestyle='--', label='model fit')
        axes[i].axhline(0, color='black', linewidth=0.8)
        axes[i].set_title(f't={t}: A={A:.3f}, B={B:.3f}, C={C:.3f}, D={D:.3f}')
        axes[i].set_xlabel('n')
        axes[i].set_ylabel('error')
        axes[i].legend(fontsize=8)
        axes[i].grid(True)

    except Exception as ex:
        print(f"t={t}: fit failed — {ex}")

plt.tight_layout()
plt.savefig('oscillatory_fit.png', dpi=300, bbox_inches='tight')
print("Saved: oscillatory_fit.png")

# ── Mod 4 amplitude table ───────────────────────────────────────────────────
print("\n=== MOD 4 AMPLITUDE A(t,n)×√n MEANS ===")
print(f"{'t':<5} {'n≡0':<10} {'n≡1':<10} {'n≡2':<10} {'n≡3':<10}")
print("-" * 45)

for t in t_values:
    d = data[t]
    A_scaled = d['signed'] * np.sqrt(d['ns'])
    means = []
    for r in range(4):
        mask = d['ns'] % 4 == r
        vals = A_scaled[mask]
        means.append(f"{np.mean(vals):.4f}" if len(vals) > 0 else "N/A")
    print(f"{t:<5} {means[0]:<10} {means[1]:<10} {means[2]:<10} {means[3]:<10}")

plt.show()