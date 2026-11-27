"""Erdős Problem 677: exhaustive counterexample search

M(n, k) = lcm(n+1, n+2, ..., n+k)

Conjecture: for k >= 1 and m >= n + k, M(m, k) != M(n, k).
(Formal statement: google-deepmind/formal-conjectures, ErdosProblems/677.lean; n >= 0 allowed.)

Method: for each fixed k, compute M(n, k) for n = 0..N, record value -> list of n, and report a
counterexample whenever the same value occurs for two disjoint windows (m >= n + k).

k = 1, 2 are trivial (M(n,1) = n+1 and M(n,2) = (n+1)(n+2) are increasing in n).

Usage:
    python3 search.py --kmax 40 --nmax 100000
    python3 search.py --selftest
"""

import argparse
import math
import sys
import time


def M(n: int, k: int) -> int:
    return math.lcm(*range(n + 1, n + k + 1))


def search_k(k: int, nmax: int, f=M):
    """Return all counterexamples (n, m) with 0 <= n < m <= nmax for this k."""
    seen: dict[int, list[int]] = {}
    found = []
    for n in range(nmax + 1):
        v = f(n, k)
        prev = seen.get(v)
        if prev is None:
            seen[v] = [n]
        else:
            for p in prev:
                if n >= p + k:
                    found.append((p, n))
            prev.append(n)
    return found


def selftest():
    # Examples from the Lean file (coincidences with different k)
    assert M(4, 3) == M(13, 2) == 210
    assert M(3, 4) == M(19, 2) == 420
    # OEIS A399050: A(n,k) = lcm(n..n+k), M(n,k) = A(n+1, k-1)
    assert M(0, 7) == 420 and M(4, 4) == 840 and M(5, 6) == 27720
    # Search logic check 1: a planted counterexample (n=5, m=20) is found
    fake = lambda n, k: 999 if n in (5, 20) else n
    assert search_k(3, 30, fake) == [(5, 20)]
    # Search logic check 2: coincidences of overlapping windows (m < n+k) are not counted
    fake2 = lambda n, k: 999 if n in (5, 6) else n
    assert search_k(3, 30, fake2) == []
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmin", type=int, default=3)
    ap.add_argument("--kmax", type=int, default=40)
    ap.add_argument("--nmax", type=int, default=100_000)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    t0 = time.time()
    total = []
    for k in range(a.kmin, a.kmax + 1):
        f = search_k(k, a.nmax)
        if f:
            print(f"k={k}: COUNTEREXAMPLES {f[:10]}{' ...' if len(f) > 10 else ''}", flush=True)
            for n, m in f[:3]:
                print(f"   M({n},{k}) = M({m},{k}) = {M(n, k)}")
        total += [(k, n, m) for n, m in f]
        print(f"k={k} done ({time.time() - t0:.1f}s)", file=sys.stderr, flush=True)
    print(f"\nRange k={a.kmin}..{a.kmax}, 0<=n<m<={a.nmax}: {len(total)} counterexamples ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
