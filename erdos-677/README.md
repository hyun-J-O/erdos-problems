# Erdős Problem #677: the cases k = 3 and k = 4

> **AI disclosure.** The mathematics, code and Lean formalization in this repository were produced by Claude, an AI assistant made by Anthropic. The repository owner is not a mathematician; they started the project and are publishing the result. Separate, independent AI reviews checked the k = 3 and k = 4 arguments. Please read everything here with the usual caution for AI-generated mathematics.

> **See also:** [`../erdos-686/`](../erdos-686): a rigorous bounded search for the related Problem #686 (N ∈ {4, 25, 49, 64, 81}, odd k = 5 to 13, Y < 10^10000).

## The problem

Let M(n, k) = lcm(n+1, …, n+k). [Erdős Problem #677](https://www.erdosproblems.com/677) asks: is it true that M(m, k) ≠ M(n, k) whenever m ≥ n + k?

Formal statement: [`erdos_677`](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/677.lean) in google-deepmind/formal-conjectures.

## Main observation: k = 3 follows from Chan (2025)

**Claim.** For 0 ≤ n < m, M(n,3) = M(m,3) holds only for (n, m) = (2, 3), where lcm(3,4,5) = lcm(4,5,6) = 60. Since 3 < 2 + 3, the answer to #677 is "yes" for k = 3.

**Proof.** Let P(n) = (n+1)(n+2)(n+3). Since gcd(n+1, n+3) = gcd(n+1, 2), M(n,3) = P(n) for even n and M(n,3) = P(n)/2 for odd n. P is strictly increasing, so M(n,3) = M(m,3) with n < m forces n even, m odd and P(m) = 2P(n). With a = n+1 ≥ 1 and b = m+1 this is

  b(b+1)(b+2) = 2a(a+1)(a+2).

By **Theorem 1** of T. H. Chan, *The Diophantine equation b(b+1)(b+2) = t a(a+1)(a+2) and gap principle*, Period. Math. Hungar. (2025), [doi:10.1007/s10998-025-00635-3](https://doi.org/10.1007/s10998-025-00635-3), [arXiv:2408.01306](https://arxiv.org/abs/2408.01306), the only positive solution is (a, b) = (3, 4), i.e. (n, m) = (2, 3). ∎

This is a direct corollary of Chan's theorem, not a new result. Chan's paper does not mention Erdős or lcm.

## Lean formalization (conditional on Chan's theorem)

[`Erdos677K3.lean`](Erdos677K3.lean) proves

```lean
theorem erdos_677_k3 (hChan : ChanTheorem1) :
    ∀ m n : ℕ, m ≥ n + 3 → lcmInterval m 3 ≠ lcmInterval n 3
```

where `ChanTheorem1` states Chan's Theorem 1 as a hypothesis:

```lean
def ChanTheorem1 : Prop :=
  ∀ a b : ℕ, 0 < a → 0 < b → b * (b + 1) * (b + 2) = 2 * (a * (a + 1) * (a + 2)) → a = 3 ∧ b = 4
```

- It uses the official definition `Finset.lcmInterval` from formal-conjectures, so the conclusion is exactly the k = 3 instance of `erdos_677`.
- It contains no `sorry`. `#print axioms` reports only `propext`, `Classical.choice` and `Quot.sound`.
- **Caveat:** the hypothesis `ChanTheorem1` was transcribed from the paper by the AI, not by a human.

**To check it:**

```sh
git clone https://github.com/google-deepmind/formal-conjectures.git
cd formal-conjectures
git checkout ea8e3e198ded6fc73efb7f5653b74b28ac4ae1a8   # tested commit (Lean v4.33.1)
lake exe cache get
lake build FormalConjecturesForMathlib.Algebra.GCDMonoid.Finset
lake env lean /path/to/Erdos677K3.lean
```

## The case k = 4 (computer-assisted proof with Sage)

**Claim.** For 0 ≤ n < m, M(n,4) = M(m,4) holds only for (n, m) = (1, 2), where lcm(2,3,4,5) = lcm(3,4,5,6) = 60. So the answer to #677 is also "yes" for k = 4.

**Reduction.** Let P(n) = (n+1)(n+2)(n+3)(n+4). Primes ≥ 5 divide at most one of the four terms. The two even terms differ by 2, so exactly one of them is 2 mod 4. Two terms are multiples of 3 only when 3 | n+1, and they differ by 3, so at most one is divisible by 9. Hence M(n,4) = P(n)/g(n) with g(n) = 6 if 3 | n+1 and g(n) = 2 otherwise.

If M(n,4) = M(m,4) with n < m, then g(m)/g(n) = P(m)/P(n) > 1. So g(m) = 6, g(n) = 2 and P(m) = 3P(n).

Put t = m+1, s = n+1, u = t²+3t+1 and v = s²+3s+1. The identity t(t+1)(t+2)(t+3) = u² − 1 turns this into u² − 3v² = −2. With T = 2t+3 we have T² = 4u + 5, so

  T⁴ − 10T² + 57 = 48v²,

and x = 3T², y = 36Tv is an **integral point** on

  E₁ : y² = x³ − 30x² + 513x.

**Integral points.** In Sage 10.10, E₁ has rank 2, proved by 2-descent with rank bounds (2, 2). Its generators (3, 36) and (19, −76) have saturation index 1, so they are a basis of E₁(ℚ) modulo the torsion Z/2. With this basis, `integral_points` (the elliptic-logarithm method) returns all 17 integral points up to sign. The only x of the form 3T² give T ∈ {0, 1, 3, 5, 9, 17}. Since t ≥ 1, T ≥ 5:

- T = 5 (m = 0): v = 3, but s²+3s+1 = 3 has no integer solution.
- T = 9 (m = 2): v = 11, so s = 2 and n = 1. This is the pair (1, 2), which has m < n + 4.
- T = 17 (m = 6): v = 41, so s = 5 and n = 4. Here P(6) = 3P(4), but 3 ∤ 7, so g(6) = 2 and M(4,4) = 840 ≠ M(6,4) = 2520.

So there is no counterexample for k = 4. ∎

**Script and checks.**
- [`k4_sage.sage`](k4_sage.sage) verifies the change-of-variables identities symbolically and computes the integral points. Its output is in [`results/k4_sage_output.txt`](results/k4_sage_output.txt).
- It also runs the same analysis on the n-side curve E₂ : y² = x³ − 30x² + 129x (x = 3S², y = 12uS with S = 2s+3) as a cross-check. It gives the same two pairs.
- The result agrees with an elementary search (odd T, S < 10⁶), a brute-force search over n < m ≤ 2·10⁵, and the first 3000 Pell solutions (`small_k.py`).

**Caveats.**
- The proof relies on the correctness of Sage's implementation (2-descent, saturation, integral points). An independent check with Magma's `IntegralPoints` has not been done.
- A separate AI review found no mathematical error.
- A literature search did not find this equation, but equations of the form t(t+1)⋯(t+k−1) = c·s(s+1)⋯(s+k−1) have been studied, so it may already be known.

## Supporting computations (evidence only, not proofs)

| Script | What it does |
|---|---|
| [`search.py`](search.py) | Exhaustive search for counterexamples. Result: none for 3 ≤ k ≤ 40 and 0 ≤ n < m ≤ 10⁶ ([`results/`](results)). Run `python3 search.py --selftest` to test the search logic. |
| [`small_k.py`](small_k.py) | Checks the k = 3 reduction numerically (1 ≤ a < 10⁷, consistent with Chan). Reduces k = 4 to the Pell-type equation X² − 3Y² = −2 and checks its first 3000 solutions (about 1700 digits): no counterexample. (The full k = 4 proof is in the section above.) |
| [`certify.py`](certify.py) | Uses an AI-derived lemma, **not independently reviewed**, to turn the search into "no counterexample for n ≤ n₀(k)" with no bound on m. The lemma: if M(m,k) = M(n,k) and m ≥ n+k, then (m+1)^k ≤ (m+k)^π(k) (n+k)^k. Treat this as unverified. |

## Related

- On #677, the [comment thread](https://www.erdosproblems.com/forum/thread/677) notes that for fixed k there are only finitely many solutions (Thue–Siegel), and lists coincidences for different k such as M(8,4) = M(43,2).
- Earlier AI-assisted Lean work on #677: [qrdlgit/erdos677](https://github.com/qrdlgit/erdos677).

## License

Apache-2.0, the same as formal-conjectures.
