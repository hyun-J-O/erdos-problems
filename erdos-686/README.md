# Erdős Problem #686: N ∈ {4, 25, 49, 64, 81}, odd k from 5 to 13

> **AI disclosure.** Claude, an AI assistant made by Anthropic, produced everything in this folder. Separate AI reviews checked it independently. The repository owner is not a mathematician. This is a **rigorous bounded search, not a proof**.

## Background

[Erdős Problem #686](https://www.erdosproblems.com/686) asks whether every N ≥ 2 can be written as

  N = (m+1)(m+2)⋯(m+k) / ((n+1)(n+2)⋯(n+k)) with k ≥ 2, n ≥ 0 and m ≥ n + k.

The [forum thread](https://www.erdosproblems.com/forum/thread/686) reports that 4, 25, 49, 64 and 81 have no representation with k ≤ 4. For N = 4, it also rules out k = 6, 8 and 12. The odd cases k ≥ 5 were open, and for N = 4 with k = 5 only a brute-force search with |x|, |y| < 10⁴ was reported.

## Result

For every N ∈ {4, 25, 49, 64, 81} and every odd k ∈ {5, 7, 9, 11, 13}, there is **no representation with Y = n + (k+1)/2 < 10^10000**. For N = 4 and k = 5 the bound is Y < 10^100000.

## Method

Let h = (k−1)/2, X = m + h + 1, Y = n + h + 1 and f(z) = z·∏_{j=1..h}(z² − j²). The equation becomes f(X) = N·f(Y). Let α = N^{1/k}, which is irrational in all 25 cases.

1. **Bracket** ([`gen_bracket.sage`](gen_bracket.sage)). Expanding f^{1/k} suggests αY − X ≈ C/Y, with C = (Σj²/k)(α²−1)/α. For a rational c slightly larger than C, an exact computation over the real algebraic numbers (exact real roots of Y^k·(f(αY + s/Y) − N f(Y)) for s = 0 and s = −c, plus monotonicity of f) proves that every solution with Y ≥ Y₀ satisfies

   0 < αY − X < c / Y.

   The values of c and Y₀ are in [`results/brackets.txt`](results/brackets.txt). Y₀ ranges from 6 to 15.
2. **Candidates** ([`gen_search.py`](gen_search.py)). Write g = gcd(X, Y), X = gp and Y = gq, so that |α − p/q| < c/q². By Worley's theorem (in the form of A. Dujella, *Continued fractions and RSA with small secret exponent*, 2004, Theorem 1), every such coprime p/q has the form (r·p_{j+1} ± s·p_j)/(r·q_{j+1} ± s·q_j), where p_j/q_j are the convergents of α and r, s are nonnegative integers with rs < 2c. Every admissible g is then tested with exact integer arithmetic.
3. **Continued fraction certification.** Only partial quotients shared by floor(α·10^P)/10^P and (floor(α·10^P)+1)/10^P are used.
4. **Small Y** (h+1 ≤ Y < Y₀) are searched directly.

## Checks

- **Planted tests.** The method recovers the known k = 3 representations N = 6 with (m,n) = (7,3), N = 9 with (25,11) and N = 16 with (13,4), and finds none for N = 2 and N = 4, which are proven non-representable. See [`results/planted_tests_output.txt`](results/planted_tests_output.txt). An independent review also built 16 representable cases with k = 5 and k = 7 by brute force, and the method found all of them.
- **Brute force.** Independent exact searches up to n ≈ 2·10⁵ find nothing admissible.
- **Review fixes.**
  1. Candidates from convergent indices beyond the search bound can have q below the bound. There were 0 to 2 such candidates per case, and [`supplement_check.py`](supplement_check.py) tests them all. Results: [`results/run_686_supplement_L10000.txt`](results/run_686_supplement_L10000.txt) and [`results/run_686_supplement_n4k5_L100000.txt`](results/run_686_supplement_n4k5_L100000.txt). No solutions.
  2. The starting point of the small-Y search was corrected to X ≥ α(Y − h) and re-run. No solutions.
- **N = 4, k = 5** also has a dedicated pair of scripts ([`n4k5_bracket.sage`](n4k5_bracket.sage), [`n4k5_search.py`](n4k5_search.py)) that was reviewed separately. The 10^100000 run used a version without Worley's m = −1 candidates (2/1 and 0/1). The review found these are excluded anyway, by the sign of α − p/q and by X ≥ Y + 5.

## Limitations

- The result is not a proof for all Y. That would need effective control of the integral points on the curve f(X) = N f(Y).
- It relies on Worley's theorem as stated by Dujella.
- Beyond the search bound, convergent indices were checked only up to 2·max(r) + 5. A brute-force comparison up to 10⁶ found no missed candidates.

## Reproduce

```sh
sage gen_bracket.sage "4,5 4,7 ... 81,13" > brackets.txt     # Sage 10.10
python3 gen_search.py 10000 < brackets.txt                   # needs gmpy2
python3 supplement_check.py 10000 < brackets.txt
```
