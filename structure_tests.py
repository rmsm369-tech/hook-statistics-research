import matplotlib.pyplot as plt
import math
import numpy as np
from collections import Counter

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

max_n = int(input("Enter max n (suggest 50): "))
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
    data[t] = {'ns': ns, 'signed': signed}
    print(f"t={t} done.")

# ── TEST 1: Parity separation ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Test 1: Signed Error — Parity of n Separated', fontsize=13)

for i, t in enumerate(t_values):
    d = data[t]
    even_n = [n for n in d['ns'] if n % 2 == 0]
    odd_n  = [n for n in d['ns'] if n % 2 == 1]
    even_e = [e for n, e in zip(d['ns'], d['signed']) if n % 2 == 0]
    odd_e  = [e for n, e in zip(d['ns'], d['signed']) if n % 2 == 1]

    axes[i].plot(even_n, even_e, 'b-o', markersize=3, label='even n')
    axes[i].plot(odd_n,  odd_e,  'r-o', markersize=3, label='odd n')
    axes[i].axhline(0, color='black', linewidth=0.8)
    axes[i].set_title(f't={t} ({"odd" if t%2==1 else "even"})')
    axes[i].set_xlabel('n')
    axes[i].set_ylabel('signed error')
    axes[i].legend(fontsize=8)
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('test1_parity_separation.png', dpi=300, bbox_inches='tight')
print("Saved: test1_parity_separation.png")

# ── TEST 2: Amplitude A_t(n) = error * sqrt(n), means by parity ────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Test 2: A(t,n) = error × √n — Parity Means', fontsize=13)

for i, t in enumerate(t_values):
    d = data[t]
    A = [e * math.sqrt(n) for e, n in zip(d['signed'], d['ns'])]

    even_n = [n for n in d['ns'] if n % 2 == 0]
    odd_n  = [n for n in d['ns'] if n % 2 == 1]
    even_A = [a for n, a in zip(d['ns'], A) if n % 2 == 0]
    odd_A  = [a for n, a in zip(d['ns'], A) if n % 2 == 1]

    # running means
    even_means = [sum(even_A[:k+1])/(k+1) for k in range(len(even_A))]
    odd_means  = [sum(odd_A[:k+1])/(k+1)  for k in range(len(odd_A))]

    axes[i].plot(even_n, even_A, 'b-', alpha=0.3, linewidth=0.8)
    axes[i].plot(odd_n,  odd_A,  'r-', alpha=0.3, linewidth=0.8)
    axes[i].plot(even_n, even_means, 'b-', linewidth=2, label=f'even mean→{even_means[-1]:.3f}')
    axes[i].plot(odd_n,  odd_means,  'r-', linewidth=2, label=f'odd mean→{odd_means[-1]:.3f}')
    axes[i].axhline(0, color='black', linewidth=0.8)
    axes[i].set_title(f't={t}')
    axes[i].set_xlabel('n')
    axes[i].set_ylabel('A(t,n)')
    axes[i].legend(fontsize=8)
    axes[i].grid(True)

plt.tight_layout()
plt.savefig('test2_amplitude.png', dpi=300, bbox_inches='tight')
print("Saved: test2_amplitude.png")

# ── TEST 3: Remove parity oscillation via averaging ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Test 3: Parity-Averaged Error e+(n)', fontsize=13)

for t, color in zip(t_values, colors):
    d = data[t]
    ns = d['ns']
    signed = d['signed']

    # e+(n) = (e(n) + e(n+1)) / 2
    e_plus_n, e_plus_v = [], []
    for k in range(len(ns) - 1):
        if ns[k+1] == ns[k] + 1:
            e_plus_n.append(ns[k])
            e_plus_v.append((signed[k] + signed[k+1]) / 2)

    scaled_eplus = [v * math.sqrt(n) for v, n in zip(e_plus_v, e_plus_n)]

    axes[0].plot(e_plus_n, e_plus_v, color=color, linewidth=1.2,
                 label=f't={t}')
    axes[1].plot(e_plus_n, scaled_eplus, color=color, linewidth=1.2,
                 label=f't={t}')

axes[0].axhline(0, color='black', linewidth=0.8)
axes[0].set_title('Parity-averaged error e+(n)')
axes[0].set_xlabel('n')
axes[0].set_ylabel('e+(n)')
axes[0].legend()
axes[0].grid(True)

axes[1].axhline(0, color='black', linewidth=0.8)
axes[1].set_title('Parity-averaged scaled: e+(n) × √n')
axes[1].set_xlabel('n')
axes[1].set_ylabel('e+(n) × √n')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('test3_parity_averaged.png', dpi=300, bbox_inches='tight')
print("Saved: test3_parity_averaged.png")

# ── TEST 4: FFT on raw, scaled, averaged ────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Test 4: FFT Decomposition', fontsize=13)

for t, color in zip(t_values, colors):
    d = data[t]
    signed = np.array(d['signed'])
    scaled = np.array([e * math.sqrt(n) for e, n in zip(d['signed'], d['ns'])])

    # parity averaged
    e_plus = []
    ns = d['ns']
    for k in range(len(ns) - 1):
        if ns[k+1] == ns[k] + 1:
            e_plus.append((d['signed'][k] + d['signed'][k+1]) / 2)
    e_plus = np.array(e_plus)

    for ax, signal, title in zip(
        axes,
        [signed, scaled, e_plus],
        ['Raw error', 'Scaled error × √n', 'Parity-averaged']
    ):
        fft_v = np.abs(np.fft.rfft(signal))
        freqs = np.fft.rfftfreq(len(signal))
        ax.plot(freqs[1:], fft_v[1:], color=color, linewidth=1.2,
                label=f't={t}', alpha=0.8)
        ax.set_title(title)
        ax.set_xlabel('frequency')
        ax.set_ylabel('amplitude')
        ax.legend(fontsize=8)
        ax.grid(True)

plt.tight_layout()
plt.savefig('test4_fft_decomposition.png', dpi=300, bbox_inches='tight')
print("Saved: test4_fft_decomposition.png")