import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.optimize import curve_fit

# ── Partition machinery ─────────────────────────────────────────────────────
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

# ── Asymptotic formulas ─────────────────────────────────────────────────────
def theory_mean_sc(t, n):
    delta = 1 if t % 2 == 1 else 0
    return math.sqrt(6*n)/math.pi - t/2 + 3/(math.pi**2) + delta/4

def theory_mean_unrestricted(t, n):
    # Griffin-Ono-Tsai: mean ~ sqrt(6n)/pi - t/2
    return math.sqrt(6*n)/math.pi - t/2

def oscillatory_model(n, A, B, C, D):
    return (A + B*np.cos(np.pi*n) + C*np.cos(np.pi*n/2) + D*np.sin(np.pi*n/2)) / np.sqrt(n)

# ── Data collection ─────────────────────────────────────────────────────────
max_n = int(input("Enter max n (suggest 60): "))
t_values = [1, 2, 3]
colors_sc  = ['blue', 'red', 'green']
colors_un  = ['cornflowerblue', 'salmon', 'lightgreen']

data_sc = {}
data_un = {}

for t in t_values:
    ns_sc, err_sc = [], []
    ns_un, err_un = [], []

    for n in range(3, max_n + 1):
        all_parts = list(gen_partitions(n))
        sc_parts  = [p for p in all_parts if is_self_conjugate(list(p))]

        # SC
        if sc_parts:
            counts = [all_hooks(list(p)).count(t) for p in sc_parts]
            emp_sc = sum(counts) / len(counts)
            ns_sc.append(n)
            err_sc.append(emp_sc - theory_mean_sc(t, n))

        # Unrestricted
        if all_parts:
            counts_un = [all_hooks(list(p)).count(t) for p in all_parts]
            emp_un = sum(counts_un) / len(counts_un)
            ns_un.append(n)
            err_un.append(emp_un - theory_mean_unrestricted(t, n))

    data_sc[t] = {'ns': np.array(ns_sc), 'err': np.array(err_sc)}
    data_un[t] = {'ns': np.array(ns_un), 'err': np.array(err_un)}
    print(f"t={t} done.")

# ── Figure 1: SC vs Unrestricted signed error ───────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Signed Error: Self-Conjugate vs Unrestricted Partitions', fontsize=13)

for i, t in enumerate(t_values):
    axes[i].plot(data_sc[t]['ns'], data_sc[t]['err'],
                 color=colors_sc[i], linewidth=1.2, label='SC')
    axes[i].plot(data_un[t]['ns'], data_un[t]['err'],
                 color=colors_un[i], linewidth=1.2, linestyle='--', label='Unrestricted')
    axes[i].axhline(0, color='black', linewidth=0.8)
    axes[i].set_title(f't={t}')
    axes[i].set_xlabel('n')
    axes[i].set_ylabel('signed error')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('comp1_signed_error.png', dpi=300, bbox_inches='tight')
print("Saved: comp1_signed_error.png")

# ── Figure 2: Scaled error A(t,n) = error * sqrt(n) ────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Scaled Error A(t,n) = error × √n: SC vs Unrestricted', fontsize=13)

for i, t in enumerate(t_values):
    sc_scaled = data_sc[t]['err'] * np.sqrt(data_sc[t]['ns'])
    un_scaled = data_un[t]['err'] * np.sqrt(data_un[t]['ns'])

    axes[i].plot(data_sc[t]['ns'], sc_scaled,
                 color=colors_sc[i], linewidth=1.2, label='SC')
    axes[i].plot(data_un[t]['ns'], un_scaled,
                 color=colors_un[i], linewidth=1.2, linestyle='--', label='Unrestricted')
    axes[i].axhline(0, color='black', linewidth=0.8)
    axes[i].set_title(f't={t}')
    axes[i].set_xlabel('n')
    axes[i].set_ylabel('error × √n')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('comp2_scaled_error.png', dpi=300, bbox_inches='tight')
print("Saved: comp2_scaled_error.png")

# ── Figure 3: FFT comparison ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('FFT of Signed Error: SC vs Unrestricted', fontsize=13)

for i, t in enumerate(t_values):
    fft_sc = np.abs(np.fft.rfft(data_sc[t]['err']))
    fft_un = np.abs(np.fft.rfft(data_un[t]['err']))
    freqs_sc = np.fft.rfftfreq(len(data_sc[t]['err']))
    freqs_un = np.fft.rfftfreq(len(data_un[t]['err']))

    axes[i].plot(freqs_sc[1:], fft_sc[1:],
                 color=colors_sc[i], linewidth=1.2, label='SC')
    axes[i].plot(freqs_un[1:], fft_un[1:],
                 color=colors_un[i], linewidth=1.2, linestyle='--', label='Unrestricted')
    axes[i].set_title(f't={t}')
    axes[i].set_xlabel('frequency')
    axes[i].set_ylabel('amplitude')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('comp3_fft.png', dpi=300, bbox_inches='tight')
print("Saved: comp3_fft.png")

# ── Table: Fitted constants comparison ─────────────────────────────────────
print("\n=== FITTED CONSTANTS: SC vs UNRESTRICTED ===")
print(f"{'t':<4} {'type':<15} {'A':<8} {'B':<8} {'C':<8} {'D':<8} {'resid'}")
print("-" * 60)

for t in t_values:
    for label, d in [('SC', data_sc[t]), ('Unrestr', data_un[t])]:
        ns = d['ns'].astype(float)
        err = d['err']
        try:
            popt, _ = curve_fit(oscillatory_model, ns, err,
                                p0=[0.5, 0.2, 0.2, 0.2], maxfev=10000)
            A, B, C, D = popt
            fitted = oscillatory_model(ns, *popt)
            resid = np.sqrt(np.mean((err - fitted)**2))
            print(f"{t:<4} {label:<15} {A:<8.3f} {B:<8.3f} {C:<8.3f} {D:<8.3f} {resid:.3f}")
        except Exception as ex:
            print(f"{t:<4} {label:<15} fit failed: {ex}")

# ── Table: Mod 4 amplitude means comparison ─────────────────────────────────
print("\n=== MOD 4 AMPLITUDE MEANS: SC vs UNRESTRICTED ===")
print(f"{'t':<4} {'type':<12} {'n≡0':<10} {'n≡1':<10} {'n≡2':<10} {'n≡3':<10}")
print("-" * 55)

for t in t_values:
    for label, d in [('SC', data_sc[t]), ('Unrestr', data_un[t])]:
        A_scaled = d['err'] * np.sqrt(d['ns'])
        means = []
        for r in range(4):
            mask = d['ns'] % 4 == r
            vals = A_scaled[mask]
            means.append(f"{np.mean(vals):.4f}" if len(vals) > 0 else "N/A")
        print(f"{t:<4} {label:<12} {means[0]:<10} {means[1]:<10} {means[2]:<10} {means[3]:<10}")