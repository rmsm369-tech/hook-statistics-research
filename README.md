# Hook Statistics Research

**"I write from the shadows — where truth hides, and questions dare to burn."**

---

> ⚠️ **RESEARCH UPDATE (IN DEVELOPMENT): High- $n$ Computational Scaling & Asymptotic Resolution**
> 
> **Status:** Active Investigation / Work in Progress
> 
> **Recent Findings (Scaling to $n=10,000$):**
> Initial exploratory computations in this repository tracked data up to $n \le 60$, identifying what appeared to be a stable $O(n^{-1/2})$ period-4 oscillatory structure in the residual error. To rigorously test this hypothesis, a custom $O(n^2)$ dynamic programming algorithm was developed to bypass recursive memory limits, scaling the exact computations to $n=10,000$.
> 
> The high- $n$ data cleanly resolves the nature of the oscillation:
> 1. **Finite- $n$ Transient Artifact:** Pushing the computation to $n=10,000$ proves that the period-4 wave (characterized by constants $C_1 \cos(\pi n / 2) + D_1 \sin(\pi n / 2)$) flattens to $< 3 \times 10^{-5}$. It is not a persistent asymptotic feature, but a deterministic finite-size transient.
> 2. **Combinatorial Baseline Shift:** The root cause of the residual wave was isolated to an asymptotic scaling mismatch. The computational engine correctly mapped the *distinct-odd parts* bijection, tracking a bounded statistic whose mathematically rigorous main asymptotic term is $\frac{\ln 2}{\pi}\sqrt{6n}$.
> 3. **The Literature Divergence:** The expected theoretical baseline previously subtracted was derived from the Craig-Ono-Singh (COS) theorem for peelable $t$-hooks (rim hooks), which scales identically to unrestricted partitions at $\frac{\sqrt{6n}}{\pi}$ (originating from a $1/(1-q^2)^2$ double-pole singularity).
> 
> **Conclusion:**
> The subtraction of the unrestricted COS baseline ($\approx 78.0$ at $n=10,000$) from the strictly evaluated distinct-odd statistic ($\approx 54.04$ at $n=10,000$) created an underlying $\ln 2$ scaling divergence. At the extreme small- $n$ limit ($n \le 60$), integer discretization effects within this growing gap perfectly aliased as a trigonometric wave. Modifying the DP engine's inner loop to inject the exact $1/(1-q)^2$ multiplicity pole instantaneously shifts the empirical mean to the expected $\approx 78.0$, closing the gap.
> 
> *This repository is currently being updated to reflect these extended high- $n$ proofs and the corrected generating-function weights.*


## Overview
This repository contains the source code, raw data, computational plots, and the compiled manuscript for the research paper: *Finite-n Convergence and Period-4 Oscillatory Structure in Hook Statistics of Self-Conjugate Partitions*.

This study provides a computational and theoretical investigation into the finite-n convergence behavior of the Craig-Ono-Singh asymptotic formula for t-hook statistics within self-conjugate partitions. We report the discovery of a distinct, previously uncharacterized period-4 oscillatory structure embedded within the lower-order asymptotic deviations—a feature unique to the self-conjugate framework.

## Abstract
> We present a computational and theoretical investigation into the finite-n convergence behavior of the Craig-Ono-Singh asymptotic formula for t-hook statistics within self-conjugate partitions. By evaluating the error terms across extensive partition intervals, we identify a distinct, previously uncharacterized period-4 oscillatory structure embedded within the lower-order asymptotic deviations. This periodic fluctuation appears unique to the self-conjugate framework and is completely absent in unrestricted partition profiles. Our findings provide a refined empirical baseline for error-bound optimization in asymptotic combinatorics and offer insights into the fine-grained distribution of hook lengths.
