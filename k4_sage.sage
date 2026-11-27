# Erdős 677, k = 4: integral points via Sage (tested with Sage 10.10, conda-forge).
# Run: sage k4_sage.sage
#
# The m-side curve E1 alone already proves the result; E2 is an independent cross-check.
#
# Reduction (see small_k.py): a counterexample m >= n + 4 forces
#     t(t+1)(t+2)(t+3) = 3 s(s+1)(s+2)(s+3),   t = m+1 >= 5, s = n+1 >= 1,
#     with 3 | t and 3 ∤ s  (from g(n) = 6 iff 3 | n+1).
# Put u = t^2+3t+1, v = s^2+3s+1, T = 2t+3, S = 2s+3. Then
#     u^2 - 3 v^2 = -2,   T^2 = 4u + 5,   S^2 = 4v + 5.
#
# (A) Using only the m-side condition:
#     (T^2 - 5)^2 + 32 = 48 v^2  =>  multiply by 9 T^2 / 16 ... explicitly:
#     x = 3 T^2, y = 36 T v  satisfy  E1 : y^2 = x^3 - 30 x^2 + 513 x.
# (B) Using only the n-side condition:
#     (S^2 - 5)^2 - 32 = 48 u^2 / 3 ... explicitly 16u^2 = 3 S^4 - 30 S^2 + 43, and
#     x = 3 S^2, y = 12 u S  satisfy  E2 : y^2 = x^3 - 30 x^2 + 129 x.
# Every counterexample gives an INTEGRAL point on E1 and on E2.

def check_map_identities():
    R.<T, v, S, u> = QQ[]
    # (A): if 48 v^2 = T^4 - 10 T^2 + 57 then (36 T v)^2 = (3T^2)^3 - 30 (3T^2)^2 + 513 (3T^2)
    lhs = (36*T*v)^2
    rhs = (3*T^2)^3 - 30*(3*T^2)^2 + 513*(3*T^2)
    assert (lhs - rhs) == 27*T^2*(48*v^2 - (T^4 - 10*T^2 + 57)), "map A"
    # (B): if 16 u^2 = 3 S^4 - 30 S^2 + 43 then (12 u S)^2 = (3S^2)^3 - 30 (3S^2)^2 + 129 (3S^2)
    lhs = (12*u*S)^2
    rhs = (3*S^2)^3 - 30*(3*S^2)^2 + 129*(3*S^2)
    assert (lhs - rhs) == 9*S^2*(16*u^2 - (3*S^4 - 30*S^2 + 43)), "map B"
    # and the curve equations follow from the reduction:
    # u = (T^2-5)/4, u^2 - 3v^2 = -2  <=>  48 v^2 = T^4 - 10 T^2 + 57
    uu = (T^2 - 5)/4
    assert 16*(uu^2 - 3*v^2 + 2) == -(48*v^2 - (T^4 - 10*T^2 + 57)), "curve A"
    vv = (S^2 - 5)/4
    assert 16*(u^2 - 3*vv^2 + 2) == 16*u^2 - (3*S^4 - 30*S^2 + 43), "curve B"
    print("map identities OK")


def analyse(name, a2, a4):
    E = EllipticCurve([0, a2, 0, a4, 0])
    print(f"\n== {name}: {E}")
    print("   conductor:", E.conductor(), "  torsion:", E.torsion_subgroup().invariants())
    r = E.rank(proof=True)
    G = E.gens(proof=True)
    print("   rank (proof=True):", r, "  rank bounds:", E.rank_bounds(), "  generators:", G)
    pts = E.integral_points(mw_base=G, both_signs=False)
    # saturation check on a fresh copy (calling it on E first breaks a precision cache in Sage 10.10)
    Ec = EllipticCurve(E.ainvs())
    sat, index, reg = Ec.saturation([Ec(P) for P in G])
    print("   saturation index of generators:", index, "  regulator:", reg)
    assert index == 1 and len(G) == r
    print("   integral points (y >= 0):", pts)
    return pts


def T_values(pts):
    out = set()
    for P in pts:
        x = ZZ(P[0])
        if x > 0 and x % 3 == 0 and (x // 3).is_square():
            out.add((x // 3).sqrt())
    return sorted(out)


check_map_identities()
ptsA = analyse("E1 (m side)", -30, 513)
ptsB = analyse("E2 (n side)", -30, 129)

TA = T_values(ptsA)   # candidates for T = 2t+3
SB = T_values(ptsB)   # candidates for S = 2s+3
print("\nT candidates from E1:", TA)
print("S candidates from E2:", SB)

found = []
for T0 in TA:
    if T0 % 2 == 0 or T0 < 5:
        continue
    t = (T0 - 3) // 2
    for S0 in SB:
        if S0 % 2 == 0 or S0 < 5:
            continue
        s = (S0 - 3) // 2
        if t*(t+1)*(t+2)*(t+3) == 3*s*(s+1)*(s+2)*(s+3):
            m, n = t - 1, s - 1
            same_lcm = lcm(range(m+1, m+5)) == lcm(range(n+1, n+5))
            found.append((n, m, same_lcm, m >= n + 4))
print("solutions (n, m, M(n,4)==M(m,4), m>=n+4):", found)
print("COUNTEREXAMPLES:", [f for f in found if f[2] and f[3]])
