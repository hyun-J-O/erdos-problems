"""Erdős 686: rigorous search for N = P_k(m)/P_k(n), k odd, with Y < 10^L.

Input per case (from gen_bracket.sage): N k c_num c_den Y0, meaning: every solution with Y >= Y0
satisfies 0 < alpha*Y - X < c/Y  (alpha = N^(1/k), c = c_num/c_den).

Candidates: write g = gcd(X,Y), X = g p, Y = g q. Then |alpha - p/q| < c/(g^2 q^2) <= c/q^2.
By Worley's theorem (Dujella 2004, Thm 1; m >= -1): (p,q) = (r p_{j+1} +- s p_j, r q_{j+1} +- s q_j)
with nonnegative integers r, s, rs < 2c. Coprimality of (p,q) forces r = 1 when s = 0 and s = 1
when r = 0. For each candidate we test every g with g^2 < c/(q(alpha q - p)) exactly.
Y < Y0 is handled by direct search.
"""

import sys
import time
from math import isqrt
from gmpy2 import mpz, iroot


def f(z, k):
    h = (k - 1) // 2
    r = z
    for j in range(1, h + 1):
        r *= z * z - j * j
    return r


def cf_expand(num, den, maxterms):
    out = []
    while den and len(out) < maxterms:
        a = num // den
        out.append(a)
        num, den = den, num - a * den
    return out


def alpha_cf(N, k, P):
    ten = mpz(10) ** P
    A, exact = iroot(mpz(N) * ten ** k, k)
    assert not exact
    lo = cf_expand(A, ten, 10 ** 8)
    hi = cf_expand(A + 1, ten, 10 ** 8)
    common = []
    for a, b in zip(lo, hi):
        if a != b:
            break
        common.append(a)
    return common[:-1], A, ten


def rs_pairs(c_num, c_den):
    """All (r, s), r, s >= 0, r*s < 2c, that can give a coprime pair."""
    out = {(1, 0), (0, 1)}
    r = 1
    while r * 1 * c_den < 2 * c_num:          # r*s < 2c with s >= 1
        s = 1
        while r * s * c_den < 2 * c_num:
            out.add((r, s))
            s += 1
        r += 1
    return sorted(out)


def search(N, k, c_num, c_den, Y0, L):
    t0 = time.time()
    h = (k - 1) // 2
    P = 2 * L + 50
    cf, A, ten = alpha_cf(N, k, P)
    bound = mpz(10) ** L
    pairs = rs_pairs(c_num, c_den)
    extra = 2 * max(r for r, _ in pairs) + 5   # convergents computed beyond the first q_M > bound
    ps, qs = [mpz(1), mpz(cf[0])], [mpz(0), mpz(1)]
    over = 0
    for a in cf[1:]:
        ps.append(a * ps[-1] + ps[-2])
        qs.append(a * qs[-1] + qs[-2])
        if qs[-1] > bound:
            over += 1
            if over > extra:
                break
    assert over > extra, "not enough partial quotients"
    cands = set()
    for j in range(0, len(ps) - 1):           # index j <-> convergent m = j-1 (m >= -1)
        for r, s in pairs:
            for e in (1, -1):
                p = r * ps[j + 1] + e * s * ps[j]
                q = r * qs[j + 1] + e * s * qs[j]
                if 0 < q < bound and p > 0:
                    cands.add((p, q))
    checked, sols = 0, []
    for p, q in cands:
        num_lo = A * q - p * ten          # <= ten*(alpha q - p)
        num_hi = (A + 1) * q - p * ten    # >  ten*(alpha q - p)
        if num_hi <= 0:
            continue
        assert num_lo > 0, f"increase P (q = {q})"
        gmax_sq = (c_num * ten) // (c_den * q * num_lo)
        gmax = min(int(iroot(gmax_sq, 2)[0]) + 1, int(bound // q) + 1)
        for g in range(1, gmax + 1):
            X, Y = g * p, g * q
            if Y < Y0 or Y >= bound:
                continue
            checked += 1
            if f(X, k) == N * f(Y, k) and X >= Y + k:
                sols.append((X, Y))
    # direct search for h+1 <= Y < Y0
    for Y in range(h + 1, Y0):
        T = N * f(Y, k)
        # admissible X satisfy X >= alpha*(Y-h) since (Y-h)^k <= f(Y) and f(X) <= X^k
        X = int(iroot(mpz(N) * mpz(Y - h) ** k, k)[0]) - 1
        X = max(X, Y + k)
        while f(X, k) < T:
            X += 1
        if f(X, k) == T:
            sols.append((X, Y))
    m_n = [(X - (h + 1), Y - (h + 1)) for X, Y in sols]
    return dict(N=N, k=k, c=f"{c_num}/{c_den}", Y0=Y0, L=L, cf_terms=len(cf), cands=len(cands),
                checked=checked, solutions_mn=m_n, secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    L = int(sys.argv[1])
    for line in sys.stdin:
        line = line.split("#")[0].split()
        if not line:
            continue
        N, k, cn, cd, Y0 = map(int, line)
        print(search(N, k, cn, cd, Y0, L), flush=True)
