"""Erdős 686, N = 4, k = 5: rigorous search for solutions with Y < 10^L.

Equation (centered): f(X) = 4 f(Y), f(z) = z(z^2-1)(z^2-4), X = m+3, Y = n+3,
n >= 0, m >= n+5  (so Y >= 3, X >= Y+5).

Step 1 (n4k5_bracket.sage, exact algebraic computation): for Y >= 5 every solution has
    0 < alpha*Y - X < (3/5)/Y,   alpha = 4^(1/5).
Step 2: Y = 3, 4 are checked directly.
Step 3: write g = gcd(X,Y), X = g p, Y = g q. Then 0 < alpha*q - p < 0.6/(g^2 q), so
  |alpha - p/q| < 0.6/(g^2 q^2).
  * g >= 2: |alpha - p/q| < 0.15/q^2 < 1/(2q^2), so p/q is a convergent (Legendre).
  * g = 1:  |alpha - p/q| < 0.6/q^2. By Worley's theorem (J. Austral. Math. Soc. 1981, see also
            Dujella 2004, Thm 1) p/q = (r p_{j+1} + e s p_j)/(r q_{j+1} + e s q_j) with
            e = +-1 and r s < 2*0.6, i.e. p/q is a convergent or (p_{j+1} +- p_j)/(q_{j+1} +- q_j).
  For every candidate fraction p/q and every admissible g we test f(gp) == 4 f(gq) exactly.

The continued fraction of alpha is computed rigorously: we expand both lo = A/10^P and
hi = (A+1)/10^P with A = floor(alpha*10^P) and keep only the common prefix.
"""

import sys
import time

try:
    import gmpy2
    from gmpy2 import mpz, iroot
except ImportError:  # pragma: no cover
    gmpy2 = None


def f(z):
    return z * (z * z - 1) * (z * z - 4)


def cf_expand(num, den, maxterms):
    out = []
    while den and len(out) < maxterms:
        a = num // den
        out.append(a)
        num, den = den, num - a * den
    return out


def alpha_cf(P):
    """Partial quotients of 4^(1/5) that are certified by both bounds lo < alpha < hi."""
    ten = mpz(10) ** P
    A, exact = iroot(mpz(4) * ten ** 5, 5)  # A = floor(alpha * 10^P)
    assert not exact
    lo = cf_expand(A, ten, 10 ** 7)
    hi = cf_expand(A + 1, ten, 10 ** 7)
    common = []
    for a, b in zip(lo, hi):
        if a != b:
            break
        common.append(a)
    # the last common term may still be incomplete; drop it to be safe
    return common[:-1], A, ten


def main(L):
    t0 = time.time()
    P = 2 * L + 50
    cf, A, ten = alpha_cf(P)
    print(f"alpha = 4^(1/5): {len(cf)} certified partial quotients (P = {P} digits)")
    bound = mpz(10) ** L

    # convergents
    ps, qs = [mpz(1), cf[0]], [mpz(0), mpz(1)]   # p_{-1}=1,p_0=a0 ; q_{-1}=0,q_0=1
    for a in cf[1:]:
        ps.append(a * ps[-1] + ps[-2])
        qs.append(a * qs[-1] + qs[-2])
        if qs[-1] > bound:
            break
    assert qs[-1] > bound, "not enough partial quotients for this L"

    # candidate reduced fractions p/q with q < 10^L
    cands = set()
    # Worley's m = -1 case: (p_0 +- p_{-1}) / (q_0 +- q_{-1}); harmless here, included for completeness
    for e in (1, -1):
        cands.add((ps[1] + e * ps[0], qs[1] + e * qs[0]))
    for j in range(1, len(ps)):
        for (p, q) in ((ps[j], qs[j]),):
            cands.add((p, q))
        if j + 1 < len(ps):
            for e in (1, -1):
                cands.add((ps[j + 1] + e * ps[j], qs[j + 1] + e * qs[j]))
    cands = {(p, q) for p, q in cands if 0 < q < bound}
    print(f"{len(cands)} candidate fractions with q < 10^{L}")

    checked = 0
    sols = []
    for p, q in cands:
        # alpha*q - p, certified sign/size via lo/hi: (A*q - p*ten)/ten <= alpha*q - p < ((A+1)*q - p*ten)/ten
        num_lo = A * q - p * ten
        num_hi = (A + 1) * q - p * ten
        if num_hi <= 0:
            continue  # alpha*q - p < 0: excluded (need alpha*q - p > 0)
        # g^2 < 0.6 / (q (alpha q - p)) <= 0.6 * ten / (q * num_lo)   (if num_lo > 0)
        if num_lo <= 0:
            gmax = None  # alpha*q - p is extremely small; cannot bound g this way
        else:
            gmax_sq = (3 * ten) // (5 * q * num_lo)
            gmax = int(iroot(gmax_sq, 2)[0]) + 1
        # alpha*q - p must be certified positive; otherwise increase P
        assert gmax is not None, f"increase P: cannot bound g for candidate with q = {q}"
        gmax = min(gmax, int(bound // q) + 1)
        for g in range(1, gmax + 1):
            X, Y = g * p, g * q
            if Y < 5 or Y >= bound:
                continue
            checked += 1
            if f(X) == 4 * f(Y):
                sols.append((X, Y))
    # Y = 3, 4 directly (X ranges over all integers with f(X) = 4 f(Y))
    for Y in (3, 4):
        T = 4 * f(Y)
        for X in range(Y + 5, 100):
            if f(X) == T:
                sols.append((X, Y))
    print(f"exact checks: {checked}; solutions with 3 <= Y < 10^{L}: {sols}")
    print(f"time {time.time() - t0:.1f}s")
    return sols


if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    main(L)
