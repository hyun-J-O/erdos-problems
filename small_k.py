"""Erdős 677, cases k = 3 and k = 4: reduction to Diophantine equations, with numerical checks.

P(n) = (n+1)(n+2)...(n+k),  M(n,k) = P(n) / g(n).

k = 3: g(n) = 2 if n odd else 1.
    P is increasing, so M(n,3) = M(m,3) with m > n implies P(m) = 2 P(n).
    With a = n+1, b = m+1: b(b+1)(b+2) = 2 a(a+1)(a+2).
    T. H. Chan (Period. Math. Hungar. 2025, arXiv:2408.01306), Theorem 1:
    the only positive solution is (a,b) = (3,4), i.e. n = 2, m = 3 < n + 3 (overlapping windows).
    Hence no counterexample for k = 3.

k = 4: g(n) = 6 if 3 | n+1 else 2.
    A counterexample needs P(m) = 3 P(n). Since t(t+1)(t+2)(t+3) = (t^2+3t+1)^2 - 1,
    X = (m+1)^2 + 3(m+1) + 1 and Y = (n+1)^2 + 3(n+1) + 1 satisfy X^2 - 3Y^2 = -2.
    In Z[sqrt3] the elements of norm -2 are unit multiples of 1+sqrt3, so the positive solutions
    are exactly (1,1)(2+sqrt3)^j. We search those with X and Y both of the form t^2+3t+1
    (a search for j < J, NOT a proof). A full proof needs the integral points of the quartic
    (s^2-5)^2 - 3(r^2-5)^2 = -32 (e.g. Sage/Magma).
"""

import math


def g(n: int, k: int) -> int:
    return math.prod(range(n + 1, n + k + 1)) // math.lcm(*range(n + 1, n + k + 1))


def check_g(N=20000):
    for n in range(N):
        assert g(n, 3) == (2 if n % 2 else 1)
        assert g(n, 4) == (6 if (n + 1) % 3 == 0 else 2)
    print(f"g formula checked for n < {N}")


def k3_bruteforce(Y=10**7):
    """b(b+1)(b+2) = 2a(a+1)(a+2) for 1 <= a < Y: numerical cross-check of Chan's theorem."""
    c = 2 ** (1 / 3)
    sols = []
    for a in range(1, Y):
        t = 2 * a * (a + 1) * (a + 2)
        b0 = round(c * (a + 1)) - 1
        for b in (b0 - 1, b0, b0 + 1):
            if b * (b + 1) * (b + 2) == t:
                sols.append((a, b))
    print(f"k=3: solutions with 1 <= a < {Y}: {sols}  (Chan Theorem 1: only (3,4))")


def k4_pell(J=3000):
    def t_of(Z):
        s = math.isqrt(4 * Z + 5)
        return (s - 3) // 2 if s * s == 4 * Z + 5 and s % 2 == 1 else None

    X, Y, hits = 1, 1, []
    for j in range(J):
        tm, tn = t_of(X), t_of(Y)
        if tm is not None and tn is not None and tm >= 1 and tn >= 1:
            m, n = tm - 1, tn - 1
            hits.append((j, n, m, "COUNTEREXAMPLE" if m >= n + 4 and math.lcm(*range(m + 1, m + 5)) == math.lcm(*range(n + 1, n + 5)) else "not a counterexample"))
        X, Y = 2 * X + 3 * Y, X + 2 * Y
    print(f"k=4: among the first {J} Pell solutions (X up to ~{len(str(X))} digits), candidates (j, n, m): {hits}")


if __name__ == "__main__":
    check_g()
    k3_bruteforce()
    k4_pell()
