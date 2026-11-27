"""Turn the search result (no counterexample with 0 <= n < m <= N) into a statement for all m.

Lemma (AI-derived, NOT independently reviewed; see README): if M(m,k) = M(n,k) and m >= n+k, then
    (m+1)^k <= (m+k)^pi(k) * (n+k)^k.
If m*(n,k) is the largest m satisfying the inequality, then for every n with m*(n,k) <= N there is
no counterexample at all. All comparisons use exact integer arithmetic.

Usage: python3 certify.py --kmin 3 --kmax 40 --nmax 1000000
"""

import argparse


def primepi(k: int) -> int:
    return sum(all(p % d for d in range(2, int(p**0.5) + 1)) for p in range(2, k + 1))


def ok(m: int, n: int, k: int, pk: int) -> bool:
    """Necessary condition from the lemma (if true, m remains a candidate)."""
    return (m + 1) ** k <= (m + k) ** pk * (n + k) ** k


def mstar(n: int, k: int, pk: int) -> int:
    """Largest m satisfying the inequality (binary search; the ratio is increasing in m)."""
    lo, hi = n + k, n + k
    while ok(hi, n, k, pk):
        hi *= 2
    if not ok(lo, n, k, pk):
        return lo - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid, n, k, pk):
            lo = mid
        else:
            hi = mid
    return lo


def n0(k: int, N: int) -> int:
    """Largest n with m*(n,k) <= N (m* is increasing in n)."""
    pk = primepi(k)
    lo, hi = -1, N
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mstar(mid, k, pk) <= N:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmin", type=int, default=3)
    ap.add_argument("--kmax", type=int, default=40)
    ap.add_argument("--nmax", type=int, default=1_000_000)
    a = ap.parse_args()
    print(f"Assuming no counterexample with m <= {a.nmax}, no counterexample exists for:")
    for k in range(a.kmin, a.kmax + 1):
        print(f"  k={k:3d}  pi(k)={primepi(k):2d}  n <= {n0(k, a.nmax)}")


if __name__ == "__main__":
    main()
