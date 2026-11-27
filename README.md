# Erdős Problem #677: the case k = 3

> **AI disclosure.** The mathematics, code and Lean formalization in this repository were produced by Claude, an AI assistant made by Anthropic. The repository owner is not a mathematician; they started the project and are publishing the result. A separate, independent AI review checked the k = 3 argument. Please read everything here with the usual caution for AI-generated mathematics.

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

## Supporting computations (evidence only, not proofs)

| Script | What it does |
|---|---|
| [`search.py`](search.py) | Exhaustive search for counterexamples. Result: none for 3 ≤ k ≤ 40 and 0 ≤ n < m ≤ 10⁶ ([`results/`](results)). Run `python3 search.py --selftest` to test the search logic. |
| [`small_k.py`](small_k.py) | Checks the k = 3 reduction numerically (1 ≤ a < 10⁷, consistent with Chan). Reduces k = 4 to the Pell-type equation X² − 3Y² = −2 and checks its first 3000 solutions (about 1700 digits): no counterexample. A full proof for k = 4 would need the integral points of the quartic (s²−5)² − 3(r²−5)² = −32. |
| [`certify.py`](certify.py) | Uses an AI-derived lemma, **not independently reviewed**, to turn the search into "no counterexample for n ≤ n₀(k)" with no bound on m. The lemma: if M(m,k) = M(n,k) and m ≥ n+k, then (m+1)^k ≤ (m+k)^π(k) (n+k)^k. Treat this as unverified. |

## Related

- On #677, the [comment thread](https://www.erdosproblems.com/forum/thread/677) notes that for fixed k there are only finitely many solutions (Thue–Siegel), and lists coincidences for different k such as M(8,4) = M(43,2).
- Earlier AI-assisted Lean work on #677: [qrdlgit/erdos677](https://github.com/qrdlgit/erdos677).

## License

Apache-2.0, the same as formal-conjectures.
