/-
Erdős Problem 677, case k = 3, conditional on Chan (2025), Theorem 1.

M(n, k) = lcm(n+1, ..., n+k) is `Finset.lcmInterval n k` from google-deepmind/formal-conjectures
(`(Finset.Ioc n (n + k)).lcm id`).

T. H. Chan, "The Diophantine equation b(b+1)(b+2) = t a(a+1)(a+2) and gap principle",
Period. Math. Hungar. (2025), arXiv:2408.01306, Theorem 1:
the only positive integer solution of b(b+1)(b+2) = 2a(a+1)(a+2) is (a, b) = (3, 4).
-/
import Mathlib
import FormalConjecturesForMathlib.Algebra.GCDMonoid.Finset

open Finset

namespace Erdos677K3

/-- Chan (2025), Theorem 1, taken as a hypothesis. -/
def ChanTheorem1 : Prop :=
  ∀ a b : ℕ, 0 < a → 0 < b → b * (b + 1) * (b + 2) = 2 * (a * (a + 1) * (a + 2)) → a = 3 ∧ b = 4

/-- `M(n,3) = lcm(n+1, lcm(n+2, n+3))`. -/
lemma lcmInterval_three (n : ℕ) :
    lcmInterval n 3 = Nat.lcm (n + 1) (Nat.lcm (n + 2) (n + 3)) := by
  have h : Finset.Ioc n (n + 3) = {n + 1, n + 2, n + 3} := by
    ext x; simp only [Finset.mem_Ioc, Finset.mem_insert, Finset.mem_singleton]; omega
  simp [lcmInterval, h, Finset.lcm_insert, Finset.lcm_singleton]
  rfl

/-- `gcd(n+1, 2) · M(n,3) = (n+1)(n+2)(n+3)`. -/
lemma gcd_mul_lcmInterval_three (n : ℕ) :
    Nat.gcd (n + 1) 2 * lcmInterval n 3 = (n + 1) * (n + 2) * (n + 3) := by
  have h23 : Nat.Coprime (n + 2) (n + 3) := by
    have : n + 3 = (n + 2) + 1 := by omega
    rw [Nat.coprime_iff_gcd_eq_one, this, Nat.gcd_self_add_right, Nat.gcd_one_right]
  have h21 : Nat.Coprime (n + 2) (n + 1) := by
    have : n + 2 = (n + 1) + 1 := by omega
    rw [Nat.coprime_comm, Nat.coprime_iff_gcd_eq_one, this, Nat.gcd_self_add_right,
      Nat.gcd_one_right]
  have hl : Nat.lcm (n + 2) (n + 3) = (n + 2) * (n + 3) := h23.lcm_eq_mul
  have hg : Nat.gcd (n + 1) ((n + 2) * (n + 3)) = Nat.gcd (n + 1) 2 := by
    rw [Nat.gcd_comm, Nat.Coprime.gcd_mul_left_cancel _ h21, Nat.gcd_comm]
    have : n + 3 = (n + 1) + 2 := by omega
    rw [this, Nat.gcd_self_add_right]
  rw [lcmInterval_three, hl, ← hg, Nat.gcd_mul_lcm, mul_assoc]

lemma gcd_two_cases (n : ℕ) : Nat.gcd (n + 1) 2 = 1 ∨ Nat.gcd (n + 1) 2 = 2 :=
  (Nat.dvd_prime Nat.prime_two).1 (Nat.gcd_dvd_right _ _)

lemma P_strictMono {n m : ℕ} (h : n < m) :
    (n + 1) * (n + 2) * (n + 3) < (m + 1) * (m + 2) * (m + 3) := by
  have h1 : n + 1 < m + 1 := by omega
  have h2 : n + 2 < m + 2 := by omega
  have h3 : n + 3 < m + 3 := by omega
  exact Nat.mul_lt_mul'' (Nat.mul_lt_mul'' h1 h2) h3

/-- **Erdős 677, k = 3** (conditional on Chan's theorem):
for `m ≥ n + 3`, `M(m,3) ≠ M(n,3)`. -/
theorem erdos_677_k3 (hChan : ChanTheorem1) :
    ∀ m n : ℕ, m ≥ n + 3 → lcmInterval m 3 ≠ lcmInterval n 3 := by
  intro m n hmn heq
  have hn := gcd_mul_lcmInterval_three n
  have hm := gcd_mul_lcmInterval_three m
  have hlt := P_strictMono (show n < m by omega)
  have hpos : 0 < lcmInterval n 3 := by
    have : 0 < (n + 1) * (n + 2) * (n + 3) := by positivity
    rw [← hn] at this
    exact Nat.pos_of_mul_pos_left this
  rw [heq] at hm
  rcases gcd_two_cases n with gn | gn <;> rcases gcd_two_cases m with gm | gm <;>
    rw [gn] at hn <;> rw [gm] at hm
  · omega
  · -- P(m) = 2 P(n): apply Chan with a = n+1, b = m+1
    have key : (m + 1) * (m + 1 + 1) * (m + 1 + 2) = 2 * ((n + 1) * (n + 1 + 1) * (n + 1 + 2)) := by
      have e1 : (m + 1) * (m + 1 + 1) * (m + 1 + 2) = (m + 1) * (m + 2) * (m + 3) := by ring
      have e2 : (n + 1) * (n + 1 + 1) * (n + 1 + 2) = (n + 1) * (n + 2) * (n + 3) := by ring
      rw [e1, e2, ← hm, ← hn]; ring
    obtain ⟨ha, hb⟩ := hChan (n + 1) (m + 1) (by omega) (by omega) key
    omega
  · omega
  · omega

end Erdos677K3
