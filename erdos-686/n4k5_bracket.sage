# Erdős 686, N = 4, k = 5: step 1 (rigorous bracket).
#
# Centered form: X = m+3, Y = n+3, f(z) = z(z^2-1)(z^2-4) = (z-2)(z-1)z(z+1)(z+2).
# Equation: f(X) = 4 f(Y),  Y >= 3 (n >= 0),  X >= Y + 5 (m >= n+5).
# f is strictly increasing for z >= 2.
#
# Claim: for Y >= Y0,  f(alpha*Y - c/Y) < 4 f(Y) < f(alpha*Y),  alpha = 4^(1/5), c = 3/5.
# Hence for any solution with Y >= Y0:  0 < alpha*Y - X < c/Y.
#
# Proof method: Q_s(Y) := Y^5 * (f(alpha*Y + s/Y) - 4 f(Y)) is a polynomial in Y over the
# real algebraic numbers AA; we compute its real roots EXACTLY and its leading coefficient sign.

R.<Y> = AA[]
alpha = AA(4)^(1/5)

def f(z):
    return z*(z^2 - 1)*(z^2 - 4)

def Q(s):
    # Y^5 * (f(alpha*Y + s/Y) - 4 f(Y)) as a polynomial in Y over AA
    S.<Yv> = AA[]
    Fr = S.fraction_field()
    z = alpha*Fr(Yv) + AA(s)/Fr(Yv)
    expr = Fr(Yv)^5 * (f(z) - 4*f(Fr(Yv)))
    assert expr.denominator() == 1
    return R(expr.numerator().change_variable_name('Y'))

for s, want in ((0, 1), (-3/5, -1)):
    P = Q(s)
    lc = P.leading_coefficient()
    roots = [r for r, _ in P.roots(AA)]
    maxroot = max(roots) if roots else None
    print(f"s = {s}: degree {P.degree()}, leading coeff ~ {RR(lc):.6f} (want sign {want}), "
          f"largest real root ~ {RR(maxroot) if maxroot is not None else None}")
    assert sign(lc) == want
    Y0 = floor(maxroot) + 1 if maxroot is not None else 3
    print(f"   => sign of Q_s(Y) is {want} for all real Y >= {Y0}")
    assert Y0 <= 5

# Also confirm f strictly increasing for z >= 2: f'(z) = 5z^4 - 15z^2 + 4 > 0 for z >= 2
fp = 5*Y^4 - 15*Y^2 + 4
print("largest real root of f'(z):", RR(max(r for r, _ in fp.roots(AA))))
