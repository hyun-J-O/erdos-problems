# Erdős 686: rigorous bracket for N = P_k(m)/P_k(n), k odd.
#
# X = m + (k+1)/2, Y = n + (k+1)/2, f(z) = z * prod_{j=1}^{h} (z^2 - j^2), h = (k-1)/2.
# Equation f(X) = N f(Y), Y >= h+1 (n >= 0), X >= Y + k (m >= n + k).
# alpha = N^(1/k) (assumed irrational). Heuristic constant C = (sum j^2 / k) (alpha^2 - 1) / alpha.
# We pick a rational c > C and prove EXACTLY (over AA) that for all real Y >= Y0
#     f(alpha Y - c/Y) < N f(Y) < f(alpha Y),
# and that f is increasing on [alpha Y0 - c/Y0, oo). Hence every solution with Y >= Y0 has
#     0 < alpha Y - X < c / Y.
# Output: one line per (N,k):  N k c_num c_den Y0
import sys

def f_poly(k):
    R.<z> = QQ[]
    h = (k - 1) // 2
    return z * prod(z^2 - j^2 for j in range(1, h + 1))

def bracket(N, k):
    h = (k - 1) // 2
    alpha = AA(N)^(1/k)
    assert alpha.minpoly().degree() > 1, "alpha must be irrational"
    C = (sum(j^2 for j in range(1, h + 1)) / k) * (alpha^2 - 1) / alpha
    c = QQ(ceil(RR(C) * 1.05 * 100)) / 100          # rational c slightly above C
    fz = f_poly(k)
    S.<Y> = AA[]
    Fr = S.fraction_field()
    def Q(s):
        z = alpha * Fr(Y) + AA(s) / Fr(Y)
        e = Fr(Y)^(k) * (fz(z) - N * fz(Fr(Y)))
        assert e.denominator() == 1
        return e.numerator()
    Y0 = h + 1
    for s, want in ((0, 1), (-c, -1)):
        P = Q(s)
        assert sign(P.leading_coefficient()) == want, (N, k, s)
        rts = [r for r, _ in P.roots(AA)]
        if rts:
            Y0 = max(Y0, floor(max(rts)) + 1)
    # monotonicity: f'(z) > 0 for z >= z0; need alpha*Y0 - c/Y0 >= z0
    R.<z> = AA[]
    fp = R(fz.derivative())
    z0 = max(r for r, _ in fp.roots(AA))
    while alpha * Y0 - c / Y0 <= z0:
        Y0 += 1
    return C, c, Y0

pairs = [(int(a), int(b)) for a, b in (p.split(',') for p in ' '.join(sys.argv[1:]).split())]
for N, k in pairs:
    C, c, Y0 = bracket(N, k)
    print(N, k, c.numerator(), c.denominator(), Y0, f"# C ~ {RR(C):.5f}")
