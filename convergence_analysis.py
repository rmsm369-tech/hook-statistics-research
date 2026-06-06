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

def hook_entropy(hook_list):
    if not hook_list:
        return 0
    total = len(hook_list)
    counts = Counter(hook_list)
    return -sum((c/total)*math.log(c/total) for c in counts.values())

max_n = int(input("Enter max n (suggest 50): "))
t_values = [1, 2, 3]
colors = ['blue', 'red', 'green']

# Collect data
data = {}
for t in t_values:
    ns, emp_list, thy_list = [], [], []
    rel_err, signed_err = [], []
    entropy_list = []

    for n in range(3, max_n + 1):
        sc_parts = [list(p) for p in gen_partitions(n)
                    if is_self_conjugate(list(p))]
        if not sc_parts:
            continue

        all_hook_counts = []
        all_hook_flat = []
        for p in sc_parts:
            h = all_hooks(p)
            all_hook_counts.append(h.count(t))
            all_hook_flat.extend(h)

        emp = sum(all_hook_counts) / len(all_hook_counts)
        thy = theory_mean(t, n)
        R = abs(emp - thy) / abs(thy) if thy != 0 else 0
        S = emp - thy
        E = hook_entropy(all_hook_flat)

        ns.append(n)
        emp_list.append(emp)
        thy_list.append(thy)
        rel_err.append(R)
        signed_err.append(S)
        entropy_list.append(E)

    data[t] = {
        'ns': ns,
        'emp': emp_list,
        'thy': thy_list,
        'rel': rel_err,
        'signed': signed_err,
        'entropy': entropy_list
    }
    print(f"t={t} done.")

# ── LENS 1: Relative error R(t,n) split by parity ──────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Lens 1: Relative Error R(t,n) — Parity Split', fontsize=13)

for t, color in zip(t_values, colors):
    d = data[t]
    label = f't={t} ({"odd" if t%2==1 else "even"})'
    axes[0].plot(d['ns'], d['rel'], color=color, linewidth=1.2, label=label)

axes[0].set_title('R(t,n) all n')
axes[0].set_xlabel('n')
axes[0].set_ylabel('relative error')
axes[0].legend()
axes[0].grid(True)

# split by parity of n
for t, color in zip(t_values, colors):
    d = data[t]
    even_n = [n for n in d['ns'] if n % 2 == 0]
    odd_n  = [n for n in d['ns'] if n % 2 == 1]
    even_r = [d['rel'][i] for i,n in enumerate(d['ns']) if n % 2 == 0]
    odd_r  = [d['rel'][i] for i,n in enumerate(d['ns']) if n % 2 == 1]
    axes[1].plot(even_n, even_r, color=color, linewidth=1,
                 linestyle='-',  label=f't={t} even n')
    axes[1].plot(odd_n,  odd_r,  color=color, linewidth=1,
                 linestyle='--', label=f't={t} odd n')

axes[1].set_title('R(t,n) split by parity of n')
axes[1].set_xlabel('n')
axes[1].set_ylabel('relative error')
axes[1].legend(fontsize=7)
axes[1].grid(True)

plt.tight_layout()
plt.savefig('lens1_relative_error.png', dpi=300, bbox_inches='tight')
# plt.show()

# ── LENS 2: Signed error + FFT ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Lens 2: Signed Error and FFT', fontsize=13)

for t, color in zip(t_values, colors):
    d = data[t]
    axes[0].plot(d['ns'], d['signed'], color=color, linewidth=1.2,
                 label=f't={t}')

axes[0].axhline(0, color='black', linewidth=0.8)
axes[0].set_title('Signed error: empirical minus theory')
axes[0].set_xlabel('n')
axes[0].set_ylabel('signed error')
axes[0].legend()
axes[0].grid(True)

for t, color in zip(t_values, colors):
    d = data[t]
    signal = np.array(d['signed'])
    fft_vals = np.abs(np.fft.rfft(signal))
    freqs = np.fft.rfftfreq(len(signal))
    axes[1].plot(freqs[1:], fft_vals[1:], color=color,
                 linewidth=1.2, label=f't={t}')

axes[1].set_title('FFT of signed error')
axes[1].set_xlabel('frequency')
axes[1].set_ylabel('amplitude')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('lens2_signed_fft.png', dpi=300, bbox_inches='tight')
# plt.show()

# ── LENS 3: Hook entropy ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle('Lens 3: Hook Distribution Entropy', fontsize=13)

for t, color in zip(t_values, colors):
    d = data[t]
    ax.plot(d['ns'], d['entropy'], color=color, linewidth=1.2,
            label=f't={t}')

ax.set_xlabel('n')
ax.set_ylabel('entropy H')
ax.set_title('Entropy of hook distribution across self-conjugate partitions')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.savefig('lens3_entropy.png', dpi=300, bbox_inches='tight')
# plt.show()

# ── LENS 4: Decay rate of R(t,n) ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
fig.suptitle('Lens 4: Log Relative Error — Decay Rate', fontsize=13)

for t, color in zip(t_values, colors):
    d = data[t]
    log_r = [math.log(r) if r > 0 else None for r in d['rel']]
    ns_clean = [n for n, r in zip(d['ns'], log_r) if r is not None]
    lr_clean = [r for r in log_r if r is not None]
    ax.plot(ns_clean, lr_clean, color=color, linewidth=1.2,
            label=f't={t}')

ax.set_xlabel('n')
ax.set_ylabel('log R(t,n)')
ax.set_title('Log relative error — linear decay = exponential convergence')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.savefig('lens4_decay_rate.png', dpi=300, bbox_inches='tight')
# plt.show()

print("\nSaved: lens1_relative_error.png")
print("Saved: lens2_signed_fft.png")
print("Saved: lens3_entropy.png")
print("Saved: lens4_decay_rate.png")

# ── LENS 5: Scaled error e(t,n) * sqrt(n) ──────────────────────────────────
import numpy as np
fig, ax = plt.subplots(figsize=(12, 5))

for t, color in zip(t_values, colors):
    d = data[t]
    scaled = [s * math.sqrt(n) for s, n in zip(d['signed'], d['ns'])]
    ax.plot(d['ns'], scaled, color=color, linewidth=1.2,
            label=f't={t} ({"odd" if t%2==1 else "even"})')

ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Scaled error: signed_error × √n')
ax.set_xlabel('n')
ax.set_ylabel('error × √n')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('lens5_scaled_error.png', dpi=300, bbox_inches='tight')
print("Saved: lens5_scaled_error.png")