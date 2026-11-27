"""Supplement for run_686_all_L10000.txt: test the candidates that the ORIGINAL run did not
generate, i.e. those built from convergent indices beyond the first q_M > 10^L.
Uses the updated gen_search.py logic restricted to these extra candidates."""
import sys
from gmpy2 import mpz, iroot
from gen_search import alpha_cf, rs_pairs, f

def extra_check(N, k, c_num, c_den, Y0, L):
    P = 2 * L + 50
    cf, A, ten = alpha_cf(N, k, P)
    bound = mpz(10) ** L
    pairs = rs_pairs(c_num, c_den)
    extra = 2 * max(r for r, _ in pairs) + 5
    ps, qs = [mpz(1), mpz(cf[0])], [mpz(0), mpz(1)]
    M = None
    for a in cf[1:]:
        ps.append(a * ps[-1] + ps[-2]); qs.append(a * qs[-1] + qs[-2])
        if qs[-1] > bound and M is None:
            M = len(ps) - 1          # original run used j in range(0, M)
        if M is not None and len(ps) - 1 >= M + extra:
            break
    assert M is not None and len(ps) - 1 >= M + extra
    new = set()
    for j in range(M, len(ps) - 1):  # indices the original run did not use
        for r, s in pairs:
            for e in (1, -1):
                p = r * ps[j + 1] + e * s * ps[j]; q = r * qs[j + 1] + e * s * qs[j]
                if 0 < q < bound and p > 0:
                    new.add((p, q))
    sols = []
    for p, q in new:
        num_lo = A * q - p * ten; num_hi = (A + 1) * q - p * ten
        if num_hi <= 0: continue
        assert num_lo > 0
        gmax = min(int(iroot((c_num * ten) // (c_den * q * num_lo), 2)[0]) + 1, int(bound // q) + 1)
        for g in range(1, gmax + 1):
            X, Y = g * p, g * q
            if Y0 <= Y < bound and X >= Y + k and f(X, k) == N * f(Y, k):
                sols.append((X, Y))
    # redo the small-Y direct search with the corrected starting point
    h = (k - 1) // 2
    for Y in range(h + 1, Y0):
        T = N * f(Y, k); X = max(int(iroot(mpz(N) * mpz(Y - h) ** k, k)[0]) - 1, Y + k)
        while f(X, k) < T: X += 1
        if f(X, k) == T: sols.append((X, Y))
    return len(new), sols

L = int(sys.argv[1])
for line in sys.stdin:
    line = line.split("#")[0].split()
    if not line: continue
    N, k, cn, cd, Y0 = map(int, line)
    n_new, sols = extra_check(N, k, cn, cd, Y0, L)
    print({"N": N, "k": k, "extra_candidates_below_bound": n_new, "solutions": sols}, flush=True)
