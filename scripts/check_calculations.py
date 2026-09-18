#!/usr/bin/env python3
"""Independent finite-dimensional checks of the book's worked calculations.
Standard library only. These are examples and regression checks, not theorem proofs.
"""
import cmath
import math
import sys
import unittest
from pathlib import Path


def adj(a):
    return [list(map(complex.conjugate, map(complex, col))) for col in zip(*a)]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def add(*matrices):
    return [[sum(m[i][j] for m in matrices) for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def tensor(a, b):
    return [[x*y for x in row_a for y in row_b] for row_a in a for row_b in b]


def ket(*entries):
    return [[complex(x)] for x in entries]


def projector(v):
    return mm(v, adj(v))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def channel(rho, operators):
    return add(*(mm(mm(k, rho), adj(k)) for k in operators))


def qft(n, inverse=False):
    sign = -1 if inverse else 1
    return [[cmath.exp(sign*2j*math.pi*j*k/n)/math.sqrt(n) for k in range(n)] for j in range(n)]


def entropy(probabilities):
    return -sum(p*math.log2(p) for p in probabilities if p > 1e-14)


I = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
Y = [[0, -1j], [1j, 0]]
Z = [[1, 0], [0, -1]]
H = scale(1/math.sqrt(2), [[1, 1], [1, -1]])
CNOT = [[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]]
zero = ket(1, 0)
plus = ket(1/math.sqrt(2), 1/math.sqrt(2))
minus = ket(1/math.sqrt(2), -1/math.sqrt(2))
bell = ket(1/math.sqrt(2), 0, 0, 1/math.sqrt(2))


class Calculations(unittest.TestCase):
    def same(self, actual, expected):
        self.assertEqual((len(actual), len(actual[0])), (len(expected), len(expected[0])))
        for ar, er in zip(actual, expected):
            for a, e in zip(ar, er):
                self.assertLess(abs(a-e), 1e-10)

    def test_01_bloch_and_measurement(self):
        v = ket(math.sqrt(3)/2, .5j)
        means = [mm(mm(adj(v), p), v)[0][0] for p in (X,Y,Z)]
        self.same([means], [[0,math.sqrt(3)/2,.5]])
        self.assertAlmostEqual(abs(mm(adj(plus), v)[0][0])**2, .5)
        # Figure data (scripts/figures/ch01_qubit.py) computes probabilities from amplitudes.
        # Check it by a different route: density matrices and p(+1) = (1 + <P>)/2.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch01_qubit as fig
        rhos = [projector(plus), projector(minus), scale(.5, I)]
        for (_, _, pz, px), rho in zip(fig.source_table(), rhos):
            for probs, pauli in ((pz, Z), (px, X)):
                mean = trace(mm(rho, pauli)).real
                self.assertAlmostEqual(probs[0], (1+mean)/2)
                self.assertAlmostEqual(probs[1], (1-mean)/2)
        for got, want in zip(fig.bloch(fig.WORKED), means):
            self.assertAlmostEqual(got, want.real)
        # Projection used for the sphere is orthonormal, so the outline is a circle.
        for u in (fig.RIGHT, fig.UP, fig.TOWARDS):
            self.assertAlmostEqual(fig.dot(u, u), 1)
        self.assertAlmostEqual(fig.dot(fig.RIGHT, fig.UP), 0)
        self.assertAlmostEqual(fig.dot(fig.RIGHT, fig.TOWARDS), 0)
        self.assertAlmostEqual(fig.dot(fig.UP, fig.TOWARDS), 0)

    def test_02_unambiguous_discrimination(self):
        c = 2-math.sqrt(2)
        ep = scale(c, projector(ket(0,1)))
        e0 = scale(c, projector(minus))
        eq = add(I, scale(-1,ep), scale(-1,e0))
        self.assertAlmostEqual((eq[0][0]*eq[1][1]-eq[0][1]*eq[1][0]).real, 0)
        self.assertGreater(trace(eq).real, 0)
        self.assertAlmostEqual(mm(mm(adj(zero),ep),zero)[0][0].real,0)
        self.assertAlmostEqual(mm(mm(adj(plus),e0),plus)[0][0].real,0)
        for v in (zero, plus):
            self.assertAlmostEqual(mm(mm(adj(v),eq),v)[0][0].real,1/math.sqrt(2))
        # Figure data (scripts/figures/ch02_measurement.py). Check against the chapter's text:
        # the running example, the controlled-NOT pointer model giving M, N_m = X M_m, equal
        # effects, branch probabilities summing to one, normalised conditional states.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch02_measurement as fig
        psi = ket(math.sqrt(3)/2, .5j)
        self.same([[a] for a in fig.EXAMPLE], psi)
        joint = mm(CNOT, tensor(psi, zero))            # system first, pointer second
        for m in (0, 1):
            v = [[joint[2*i+m][0]] for i in range(2)]  # component with pointer value m
            mo = [[1 if (i == j == m) else 0 for j in range(2)] for i in range(2)]
            self.same(v, mm(mo, psi))
            self.same([list(r) for r in fig.M[m]], mo)
            self.same([list(r) for r in fig.N[m]], mm(X, mo))
            self.same(mm(adj(mm(X, mo)), mm(X, mo)), mm(adj(mo), mo))
        for key, expect in (("M", ["|0⟩", "|1⟩"]), ("N", ["|1⟩", "|0⟩"])):
            rows = fig.branches(key)
            self.assertAlmostEqual(sum(r["p"] for r in rows), 1)
            self.assertEqual([r["name"] for r in rows], expect)
            for r, p in zip(rows, (.75, .25)):
                self.assertAlmostEqual(r["p"], p)
                self.assertAlmostEqual(fig.norm2(r["state"]), 1)
        self.assertEqual([r["again"] for r in fig.branches("M")], [0, 1])
        self.assertEqual([r["again"] for r in fig.branches("N")], [1, 0])
        effects = [e0, ep, eq]                          # says |0>, says |+>, don't know
        for (name, probs), v in zip(fig.unambiguous_rows(), (zero, plus)):
            self.assertAlmostEqual(sum(probs), 1)
            for prob, e in zip(probs, effects):
                self.assertAlmostEqual(prob, mm(mm(adj(v), e), v)[0][0].real)
        # The "ignored outcome" paragraph: |+> after an unread Z measurement gives + with p = 1/2.
        avg = sum(abs(mm(adj(plus), b)[0][0])**2 * abs(mm(adj(b), plus)[0][0])**2 for b in (zero, ket(0, 1)))
        self.assertAlmostEqual(avg, .5)

    def test_03_partial_trace_and_correlations(self):
        rho = projector(bell)
        reduced = [[sum(rho[2*i+j][2*k+j] for j in range(2)) for k in range(2)] for i in range(2)]
        self.same(reduced, scale(.5,I))
        self.assertAlmostEqual(trace(mm(rho,tensor(Y,Y))).real,-1)
        classical = [[rho[i][j] if i==j else 0 for j in range(4)] for i in range(4)]
        self.assertAlmostEqual(trace(mm(classical,tensor(X,X))).real,0)
        # Figure data (scripts/figures/ch03_density.py) averages Bloch vectors. Check the other
        # way: build each ensemble's density matrix from projectors, then read r from Pauli traces.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch03_density as fig
        rhos = {}
        for name, ens in fig.ENSEMBLES.items():
            rho = add(*[scale(w, projector(ket(*fig.KETS[k]))) for w, k in ens])
            rhos[name] = rho
            r = [trace(mm(rho, s)).real for s in (X, Y, Z)]
            for got, want in zip(fig.average(ens), r):
                self.assertAlmostEqual(got, want)
        self.same(rhos["source C"], rhos["plus-minus coin"]); self.same(rhos["source C"], scale(.5, I))
        self.same(rhos["3:1 coin"], rhos["tilted pair"]); self.same(rhos["3:1 coin"], [[.75, 0], [0, .25]])
        self.same(reduced, rhos["source C"])  # half of a Bell pair: the same matrix

    def test_04_gate_order_and_bell_preparation(self):
        self.same(mm(mm(H,Z),H),X)
        circuit = mm(CNOT,tensor(H,I))
        self.same(mm(circuit,ket(1,0,0,0)),bell)
        self.same(mm(CNOT,tensor(plus,plus)),tensor(plus,plus))
        # Figure rows (scripts/figures/ch04_circuit.py) use basis rules on labelled terms. Check
        # them with 4x4 matrices, and check that label "ab" is index 2a+b (qubit 1 leftmost).
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch04_circuit as fig
        for k, lab in enumerate(fig.LABELS):
            a_, b_ = int(lab[0]), int(lab[1])
            basis = tensor(ket(1-a_, a_), ket(1-b_, b_))
            self.assertAlmostEqual(basis[k][0], 1)
        start = ket(1, 0, 0, 0)
        expected = [start, mm(tensor(H, I), start), mm(circuit, start), mm(tensor(H, I), mm(CNOT, start))]
        for (_, state), want in zip(fig.rows(), expected):
            self.same([[state[lab]] for lab in fig.LABELS], want)
        self.same(expected[3], tensor(plus, zero))  # other order: a product state

    def test_05_rotation_and_detuning(self):
        theta = math.pi/3
        ry = [[math.cos(theta/2),-math.sin(theta/2)],[math.sin(theta/2),math.cos(theta/2)]]
        rz = [[cmath.exp(-1j*math.pi/4),0],[0,cmath.exp(1j*math.pi/4)]]
        v = mm(mm(rz,ry),zero)
        self.same(projector(v),projector(ket(math.sqrt(3)/2,.5j)))
        # Detuned constant pulse at its first population maximum: Omega=Delta=1.
        u = scale(-1j/math.sqrt(2),add(X,Z))
        self.assertAlmostEqual(abs(mm(u,zero)[1][0])**2,.5)
        # Figure paths (scripts/figures/ch05_rotation.py) use the rotation formula for Bloch
        # vectors. Recompute them from the 2x2 matrix exp(-i w t n.sigma/2) acting on |0>.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch05_rotation as fig
        for ratio in (0, 1):
            w = math.sqrt(1 + ratio**2)
            nsig = scale(1/w, add(X, scale(ratio, Z)))
            for k in range(13):
                omega_t = 2*math.pi*k/12
                ang = w*omega_t
                evo = add(scale(math.cos(ang/2), I), scale(-1j*math.sin(ang/2), nsig))
                v = mm(evo, zero)
                r = [mm(mm(adj(v), s), v)[0][0].real for s in (X, Y, Z)]
                for got, want in zip(fig.bloch_after(omega_t, ratio), r):
                    self.assertAlmostEqual(got, want)
                closed = math.sin(w*omega_t/2)**2/(1+ratio**2)   # the chapter's p(1; t) formula
                self.assertAlmostEqual(fig.p1(omega_t, ratio), closed)
        self.assertAlmostEqual(fig.p1(math.pi, 0), 1)
        self.assertAlmostEqual(fig.p1(math.pi/math.sqrt(2), 1), .5)
        self.assertAlmostEqual(math.pi/(2*math.pi*10e6), 50e-9)          # pi pulse at Omega/2pi = 10 MHz

    def test_06_copying_orthogonal_alphabet(self):
        circuit = mm(mm(tensor(H,H),CNOT),tensor(H,I))
        for v in (plus, minus):
            self.same(mm(circuit,tensor(v,zero)),tensor(v,v))
        self.assertNotEqual(projector(bell),projector(tensor(plus,plus)))
        # Figure rows (scripts/figures/ch06_cloning.py): check with CNOT and tensor products.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch06_cloning as fig
        want = [mm(CNOT, tensor(zero, zero)), mm(CNOT, tensor(ket(0, 1), zero)),
                mm(CNOT, tensor(plus, zero)), tensor(plus, plus)]
        for (_, state, _), w in zip(fig.rows(), want):
            self.same([[state[k]] for k in fig.LABELS], w)

    def test_07_schmidt_spectrum(self):
        c = scale(1/math.sqrt(3),[[1,1],[1,0]])
        rho = mm(c,adj(c))
        self.assertAlmostEqual(trace(mm(rho,rho)).real,7/9)
        for lam in ((3+math.sqrt(5))/6,(3-math.sqrt(5))/6):
            self.assertAlmostEqual((rho[0][0]-lam)*(rho[1][1]-lam)-rho[0][1]*rho[1][0],0)
        # Figure spectra (scripts/figures/ch07_schmidt.py) use the eigenvalues of C C^dagger.
        # Check by another route: s1^2 + s2^2 = 1 and s1^2 s2^2 = |det C|^2, and the product and
        # Bell rows against tensor products and the Bell vector.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch07_schmidt as fig
        for _, cm in fig.STATES:
            l1, l2 = fig.schmidt_squares(cm)
            self.assertAlmostEqual(l1 + l2, 1)
            self.assertAlmostEqual(l1 * l2, fig.det(cm)**2)
        self.same([[x] for row in fig.STATES[0][1] for x in row], tensor(plus, ket(0, 1)))
        self.same([[x] for row in fig.STATES[2][1] for x in row], bell)
        self.same(scale(math.sqrt(3), [[x] for row in fig.STATES[1][1] for x in row]), ket(1, 1, 1, 0))
        # Best product overlap equals the largest s^2 (text claim): search product states on a grid.
        def best_overlap(cm):
            # For fixed u the best v gives |<u x v|Psi>| = ||C^dagger u||; search u over the sphere.
            best = 0
            for i in range(241):
                for j in range(96):
                    ta, pa = math.pi*i/240, 2*math.pi*j/96
                    u = (math.cos(ta/2), cmath.exp(1j*pa)*math.sin(ta/2))
                    w = [sum(u[r].conjugate()*cm[r][s] for r in range(2)) for s in range(2)]
                    best = max(best, sum(abs(x)**2 for x in w))
            return best
        for _, cm in fig.STATES:
            got = best_overlap(cm); top = max(fig.schmidt_squares(cm))
            self.assertLessEqual(got, top + 1e-9); self.assertGreater(got, top - 1e-3)

    def test_08_chsh(self):
        b0,b1 = scale(1/math.sqrt(2),add(Z,X)),scale(1/math.sqrt(2),add(Z,scale(-1,X)))
        observables = [tensor(Z,b0),tensor(Z,b1),tensor(X,b0),tensor(X,b1)]
        values = [mm(mm(adj(bell),a),bell)[0][0].real for a in observables]
        self.assertAlmostEqual(values[0]+values[1]+values[2]-values[3],2*math.sqrt(2))
        # Figure curve (scripts/figures/ch08_chsh.py): S(phi) = 3cos(phi) - cos(3phi) from cosines.
        # Recompute from 4x4 matrices on |Phi+>, and check the 68.5 degree crossing.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch08_chsh as fig
        def obs(t): return add(scale(math.cos(t), Z), scale(math.sin(t), X))
        for deg in (0, 15, 30, 45, 60, 75, 90):
            phi = math.radians(deg); st = fig.settings(phi)
            e = lambda a, b: mm(mm(adj(bell), tensor(obs(st[a]), obs(st[b]))), bell)[0][0].real
            s = e("A0","B0") + e("A0","B1") + e("A1","B0") - e("A1","B1")
            self.assertAlmostEqual(fig.s_value(phi), s)
        self.assertAlmostEqual(fig.s_value(fig.crossing()), 2)
        self.assertAlmostEqual(math.degrees(fig.crossing()), 68.53, places=2)
        self.same(obs(fig.settings(math.pi/4)["B0"]), b0); self.same(obs(fig.settings(math.pi/4)["B1"]), b1)

    def test_09_all_teleportation_branches(self):
        # Full three-register circuit; compare every branch on several complex inputs.
        for v in (zero,plus,ket(math.sqrt(.3),1j*math.sqrt(.7))):
            output = mm(tensor(tensor(H,I),I),mm(tensor(CNOT,I),tensor(v,bell)))
            for a in range(2):
                for b in range(2):
                    branch = output[2*(2*a+b):2*(2*a+b)+2]
                    self.assertAlmostEqual(mm(adj(branch),branch)[0][0].real,.25)
                    recovery=mm(Z if a else I,X if b else I)
                    self.same(mm(recovery,scale(2,branch)),v)
            rho=projector(v)
            self.same(scale(.25,add(*(mm(mm(p,rho),adj(p)) for p in (I,X,Z,mm(X,Z))))),scale(.5,I))
        # Figure (scripts/figures/ch09_teleport.py): execute the drawn STEPS with 8x8 matrices in
        # register order Q, A, B, and check every branch recovers the input.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch09_teleport as fig
        self.assertEqual(fig.REGISTERS, ["Q", "A", "B"])
        self.assertEqual([fig.OWNER[r] for r in fig.REGISTERS], ["Alice", "Alice", "Bob"])
        def on(reg, g):
            ops = [g if r == reg else I for r in fig.REGISTERS]
            return tensor(tensor(ops[0], ops[1]), ops[2])
        def cnot_on(c, tg):
            idx = {r: i for i, r in enumerate(fig.REGISTERS)}
            m = [[0]*8 for _ in range(8)]
            for s in range(8):
                bits = [(s >> (2 - i)) & 1 for i in range(3)]
                if bits[idx[c]]: bits[idx[tg]] ^= 1
                m[bits[0]*4 + bits[1]*2 + bits[2]][s] = 1
            return m
        for v in (zero, plus, ket(math.sqrt(.3), 1j*math.sqrt(.7))):
            state = tensor(v, bell)
            for step in fig.STEPS:
                if step[0] == "cnot": state = mm(cnot_on(step[1], step[2]), state)
                elif step[0] == "h": state = mm(on(step[1], H), state)
            corrections = [s for s in fig.STEPS if s[0] in ("x_if", "z_if")]
            for a in range(2):
                for b in range(2):
                    bob = [[state[4*a + 2*b + k][0]*2] for k in range(2)]
                    for kind, _, bit in corrections:
                        if {"a": a, "b": b}[bit]: bob = mm(X if kind == "x_if" else Z, bob)
                    self.same(bob, v)

    def test_10_all_two_bit_deutsch_jozsa_promises(self):
        h2=tensor(H,H)
        for mask in range(16):
            values=[(mask>>x)&1 for x in range(4)]
            if sum(values) not in (0,2,4):
                continue
            state=ket(*[(-1)**f/2 for f in values])
            p0=abs(mm(h2,state)[0][0])**2
            self.assertAlmostEqual(p0,1 if sum(values) in (0,4) else 0)
        self.same(mm(h2,ket(.5,-.5,-.5,.5)),ket(0,0,0,1))
        # Figure panels (scripts/figures/ch10_deutsch.py) use sign rules and the a_z formula.
        # Recompute them with 4x4 matrices: diagonal phase oracle, then H x H.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch10_deutsch as fig
        hh = tensor(H, H); s = mm(hh, ket(1, 0, 0, 0))
        for _, fn in fig.FUNCTIONS:
            oracle = [[(-1)**fn(*fig.bits(fig.LABELS[r])) if r == c else 0 for c in range(4)] for r in range(4)]
            after = mm(oracle, s); final = mm(hh, after)
            self.same([[fig.after_oracle(fn)[k]] for k in fig.LABELS], after)
            self.same([[fig.after_hadamards(fn)[k]] for k in fig.LABELS], final)

    def test_11_period_sampling_and_phase_estimation(self):
        state=ket(*[.5 if x in (1,5,9,13) else 0 for x in range(16)])
        probabilities=[abs(x[0])**2 for x in mm(qft(16),state)]
        self.same([probabilities],[[.25 if k%4==0 else 0 for k in range(16)]])
        phase=ket(*[cmath.exp(2j*math.pi*j*3/8)/math.sqrt(8) for j in range(8)])
        self.same(mm(qft(8,True),phase),ket(*[1 if k==3 else 0 for k in range(8)]))
        # Figure (scripts/figures/ch11_fourier.py). Exact panel: build the conditional coset state
        # for f(x) = x mod 4 and Fourier-transform it. Order panel: simulate the two-register
        # circuit sum_j |j>|2^j mod 21> directly, inverse-QFT the control for each target value,
        # and add probabilities; no eigenstates are used.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch11_fourier as fig
        n = fig.EXACT_N
        coset = [1/2 if x % 4 == 1 else 0 for x in range(n)]
        probs = [abs(sum(cmath.exp(2j*math.pi*x*k/n)*coset[x] for x in range(n)))**2/n for k in range(n)]
        for got, want in zip(fig.exact_distribution(), probs):
            self.assertAlmostEqual(got, want)
        n = fig.ORDER_N; groups = {}
        for j in range(n):
            groups.setdefault(pow(fig.BASE, j, fig.MOD), []).append(j)
        self.assertEqual(len(groups), fig.ORDER_R)
        direct = [sum(abs(sum(cmath.exp(-2j*math.pi*j*k/n) for j in js))**2 for js in groups.values())/n**2 for k in range(n)]
        for got, want in zip(fig.order_distribution(), direct):
            self.assertAlmostEqual(got, want)
        self.assertAlmostEqual(sum(direct), 1)

    def test_12_grover_against_closed_form(self):
        for n in (4,8,16):
            s=ket(*[1/math.sqrt(n)]*n)
            eye=[[int(i==j) for j in range(n)] for i in range(n)]
            d=add(scale(2,projector(s)),scale(-1,eye))
            oracle=[row[:] for row in eye];oracle[2][2]=-1
            g=mm(d,oracle);state=s
            for k in range(5):
                self.assertAlmostEqual(abs(state[2][0])**2,math.sin((2*k+1)*math.asin(1/math.sqrt(n)))**2)
                if n==8 and k in (1,2,3):
                    self.assertAlmostEqual(abs(state[2][0])**2,{1:25/32,2:121/128,3:169/512}[k])
                state=mm(g,state)
        # Figure data (scripts/figures/ch12_grover.py) uses the mean-reflection rule and the
        # closed form. Check both against the matrix G = D O_w, and the plotted angles against
        # the simulated components along |w> and |r>.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch12_grover as fig
        def simulate(n, w, steps):
            s=ket(*[1/math.sqrt(n)]*n)
            eye=[[int(i==j) for j in range(n)] for i in range(n)]
            oracle=[row[:] for row in eye];oracle[w][w]=-1
            d=add(scale(2,projector(s)),scale(-1,eye))
            states=[s]
            for _ in range(steps):states.append(mm(d,mm(oracle,states[-1])))
            return states,oracle
        states,oracle=simulate(fig.N_SMALL,fig.W_SMALL,1)
        panels=[amps for _,amps in fig.small_panels()]
        self.same([panels[0]],[[row[0] for row in states[0]]])
        self.same([panels[1]],[[row[0] for row in mm(oracle,states[0])]])
        self.same([panels[2]],[[row[0] for row in states[1]]])
        self.assertEqual(format(fig.W_SMALL,'02b'),'10')  # label order: leftmost register first
        n=fig.N_PLANE;states,_=simulate(n,0,fig.K_BARS-1)
        for k,state in enumerate(states):
            along_w=state[0][0].real;along_r=sum(row[0].real for row in state[1:])/math.sqrt(n-1)
            self.assertAlmostEqual(along_w**2+along_r**2,1)
            self.assertAlmostEqual(math.atan2(along_w,along_r)%(2*math.pi),fig.angle(k,n)%(2*math.pi))
            self.assertAlmostEqual(along_w**2,fig.success(k,n))
        best=max(range(4),key=lambda k:abs(states[k][0][0])**2)
        self.assertEqual(fig.stopping_count(n),best)
        # Caption claims: k = 6 beats k = 2 (a later peak), and two runs at k = 2 both fail with p = 0.003.
        self.assertGreater(fig.success(6,n),fig.success(2,n));self.assertAlmostEqual(fig.success(6,n),0.9998,places=4)
        self.assertAlmostEqual((1-fig.success(2,n))**2,0.003,places=3)

    def test_13_damping(self):
        operators=[[[1,0],[0,.5]],[[0,math.sqrt(.75)],[0,0]]]
        self.same(add(*(mm(adj(k),k) for k in operators)),I)
        rho=channel(projector(plus),operators)
        self.same(rho,[[7/8,1/4],[1/4,1/8]])
        self.assertAlmostEqual(trace(mm(rho,rho)).real,29/32)
        # Figure (scripts/figures/ch13_channels.py). Top: build the joint system-environment
        # unitary, act on |+>|0>_E, read branches off the environment, and trace it out.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch13_channels as fig
        g = fig.GAMMA; c, s = math.sqrt(1-g), math.sqrt(g)
        u = [[1,0,0,0],[0,c,s,0],[0,-s,c,0],[0,0,0,1]]   # order |system, env>; |1,0> -> c|1,0> + s|0,1>
        joint = mm(u, tensor(plus, zero))
        branches = []
        for e in range(2):
            v = [[joint[2*i+e][0]] for i in range(2)]
            p = sum(abs(x[0])**2 for x in v)
            r = [mm(mm(adj(v), m), v)[0][0].real/p for m in (X, Z)]
            branches.append((p, r))
        for (_, p, _, r), (pw, rw) in zip(fig.branches(), branches):
            self.assertAlmostEqual(p, pw); self.assertAlmostEqual(r[0], rw[0]); self.assertAlmostEqual(r[1], rw[1])
        reduced = [[sum(joint[2*i+e][0]*joint[2*k+e][0].conjugate() for e in range(2)) for k in range(2)] for i in range(2)]
        self.same(reduced, [[7/8, 1/4], [1/4, 1/8]])
        for got, m in zip(fig.ignored(), (X, Z)):
            self.assertAlmostEqual(got, trace(mm(reduced, m)).real)
        # Bottom: the Bloch-ball maps against Kraus operators on points of the circle.
        deph = [scale(math.sqrt(1-fig.P_DEPHASE), I), scale(math.sqrt(fig.P_DEPHASE), Z)]
        damp = [[[1,0],[0,c]], [[0,s],[0,0]]]
        for k in range(12):
            th = 2*math.pi*k/12
            rho = scale(.5, add(I, scale(math.sin(th), X), scale(math.cos(th), Z)))
            for ks, fmap in ((deph, fig.dephase_map), (damp, fig.damp_map)):
                out = channel(rho, ks)
                want = fmap(math.sin(th), math.cos(th))
                self.assertAlmostEqual(trace(mm(out, X)).real, want[0]); self.assertAlmostEqual(trace(mm(out, Z)).real, want[1])

    def test_14_syndrome_and_coherent_recovery(self):
        encoded=ket(math.sqrt(.3),0,0,0,0,0,0,1j*math.sqrt(.7))
        checks=[tensor(tensor(Z,Z),I),tensor(tensor(I,Z),Z)]
        errors=[tensor(tensor(I,I),I),tensor(tensor(X,I),I),tensor(tensor(I,X),I),tensor(tensor(I,I),X)]
        syndromes=[(1,1),(-1,1),(-1,-1),(1,-1)]
        for err,syndrome in zip(errors,syndromes):
            state=mm(err,encoded)
            for check,sign in zip(checks,syndrome):
                self.same(mm(check,state),scale(sign,state))
            self.same(mm(err,state),encoded)
        # Every single-site Pauli must satisfy the nine-qubit recovery criterion.
        gp={0:1/math.sqrt(2),7:1/math.sqrt(2)}
        gm={0:1/math.sqrt(2),7:-1/math.sqrt(2)}
        def blocks(g):
            return {(a<<6)|(b<<3)|c:x*y*z for a,x in g.items() for b,y in g.items() for c,z in g.items()}
        code=[blocks(gp),blocks(gm)]
        def error(state,site,pauli):
            bit=1<<site
            out={}
            for x,amp in state.items():
                phase=1 if not (x&bit) else -1
                if pauli=='I': y,f=x,1
                elif pauli=='X': y,f=x^bit,1
                elif pauli=='Z': y,f=x,phase
                else: y,f=x^bit,1j*phase
                out[y]=amp*f
            return out
        operations=[(0,'I')]+[(q,p) for q in range(9) for p in 'XYZ']
        states=[[error(v,q,p) for v in code] for q,p in operations]
        def inner(a,b): return sum(complex(v).conjugate()*b.get(k,0) for k,v in a.items())
        for a in states:
            for b in states:
                self.assertLess(abs(inner(a[0],b[1])),1e-10)
                self.assertLess(abs(inner(a[0],b[0])-inner(a[1],b[1])),1e-10)
        # Figure table (scripts/figures/ch14_syndrome.py): readings from Z1Z2, Z2Z3 eigenvalues on the
        # corrupted state for several (alpha, beta), and recovery restores the logical state.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch14_syndrome as fig
        def op(ms): return tensor(tensor(ms[0], ms[1]), ms[2])
        z12, z23 = op([Z, Z, I]), op([I, Z, Z])
        for al, be in ((1, 0), (0, 1), (math.sqrt(.3), 1j*math.sqrt(.7))):
            logical = [[0]]*8; logical = [[al if k == 0 else be if k == 7 else 0] for k in range(8)]
            for (name, terms, (b1, b2), _), k in zip(fig.rows(), fig.ERRORS):
                err = op([X if q == k else I for q in range(3)])
                bad = mm(err, logical)
                self.same(mm(z12, bad), scale((-1)**b1, bad)); self.same(mm(z23, bad), scale((-1)**b2, bad))
                self.same(mm(err, bad), logical)
                self.assertEqual(sorted(format(i, '03b') for i in range(8) if abs(bad[i][0]) > 1e-12),
                                 sorted(tm for tm, amp in zip(terms, (al, be)) if abs(amp) > 1e-12))

    def test_15_information_accounting(self):
        chi=entropy([(1+1/math.sqrt(2))/2,(1-1/math.sqrt(2))/2])
        measured=entropy([.75,.25])-.5
        self.assertAlmostEqual(chi,.6008760366928562)
        self.assertAlmostEqual(measured,.31127812445913283)
        self.assertLess(measured,chi)
        self.assertEqual(entropy([.5,.5])-entropy([.5,.5]),0)
        self.assertEqual(entropy([.25]*4),2)
        # Figure rows (scripts/figures/ch15_resources.py): chi from density-matrix eigenvalues, and
        # achieved information from joint outcome distributions.
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'figures'))
        import ch15_resources as fig
        def eig2(r):
            tr = (r[0][0]+r[1][1]).real; det = (r[0][0]*r[1][1]-r[0][1]*r[1][0]).real
            d = math.sqrt(max(tr*tr/4-det, 0)); return [tr/2+d, tr/2-d]
        def chi(states):
            avg = scale(1/len(states), add(*states))
            return entropy(eig2(avg)) - sum(entropy(eig2(s)) for s in states)/len(states)
        def mutual(states, basis):
            joint = [[mm(mm(adj(b), s), b)[0][0].real/len(states) for b in basis] for s in states]
            px = [sum(r) for r in joint]; py = [sum(c) for c in zip(*joint)]
            return sum(joint[x][y]*math.log2(joint[x][y]/(px[x]*py[y])) for x in range(len(states)) for y in range(len(basis)) if joint[x][y] > 0)
        rows = {r[0]: r for r in fig.SCENARIOS}
        one = ket(0, 1)
        for name, states in (("|0⟩ or |1⟩", [projector(zero), projector(one)]), ("|0⟩ or |+⟩", [projector(zero), projector(plus)]),
                             ("I/2 for every message", [scale(.5, I), scale(.5, I)])):
            self.assertAlmostEqual(rows[name][2], chi(states))
            self.assertAlmostEqual(rows[name][3], mutual(states, [zero, one]))
        sent = [projector(mm(tensor(mm(mm(X, Z) if (a and b) else X if b else Z if a else I, I), I), bell)) for a in (0, 1) for b in (0, 1)]
        alone = [[[sum(s[2*i+j][2*k+j] for j in range(2)) for k in range(2)] for i in range(2)] for s in sent]
        self.assertAlmostEqual(rows["dense coding, sent qubit alone"][2], chi(alone))
        avg = scale(.25, add(*sent)); self.same(avg, scale(.25, tensor(I, I)))
        self.assertAlmostEqual(rows["dense coding, Bob holds both"][2], 2 - 0)

    def test_16_two_register_projection(self):
        # Build a function-evaluation state, project the output, and renormalise.
        n, r = 16, 4
        joint = {(x, x % r): 1/math.sqrt(n) for x in range(n)}
        selected = {x: amp for (x,y),amp in joint.items() if y == 1}
        probability = sum(abs(amp)**2 for amp in selected.values())
        self.assertAlmostEqual(probability, 1/4)
        conditional = ket(*[selected.get(x,0)/math.sqrt(probability) for x in range(n)])
        self.same(conditional, ket(*[.5 if x in (1,5,9,13) else 0 for x in range(n)]))
        for k, amp in enumerate(mm(qft(n), conditional)):
            self.assertAlmostEqual(abs(amp[0])**2, .25 if k%4==0 else 0)

    def test_17_modular_order_and_convergents(self):
        from fractions import Fraction
        modulus, a, dimension, r = 21, 2, 32, 6
        # Actual multiplication permutation, not just the claimed phase formula.
        u = [[0]*dimension for _ in range(dimension)]
        for y in range(dimension):
            destination = a*y%modulus if y<modulus else y
            u[destination][y] = 1
        self.same(mm(adj(u),u), [[int(i==j) for j in range(dimension)] for i in range(dimension)])
        eigenstates=[]
        for s in range(r):
            v=[0j]*dimension
            for j in range(r):
                v[pow(a,j,modulus)]=cmath.exp(-2j*math.pi*s*j/r)/math.sqrt(r)
            v=ket(*v);eigenstates.append(v)
            self.same(mm(u,v),scale(cmath.exp(2j*math.pi*s/r),v))
        self.same(scale(1/math.sqrt(r),add(*eigenstates)),ket(*[int(y==1) for y in range(dimension)]))
        def convergents(n,d):
            terms=[]
            while d:
                q,remainder=divmod(n,d);terms.append(q);n,d=d,remainder
            p0,p1,q0,q1=0,1,1,0
            out=[]
            for term in terms:
                p0,p1=p1,term*p1+p0;q0,q1=q1,term*q1+q0
                out.append(Fraction(p1,q1))
            return terms,out
        for numerator,denominator in [(85,256),(341,1024)]:
            terms,cs=convergents(numerator,denominator)
            self.assertIn(Fraction(1,3),cs)
            self.assertEqual(Fraction(numerator,denominator).denominator,denominator)
            self.assertLess(abs(Fraction(numerator,denominator)-Fraction(1,3)),Fraction(1,2*r*r))
        terms,cs=convergents(171,1024)
        self.assertEqual(terms,[0,5,1,84,2]);self.assertIn(Fraction(1,6),cs)
        self.assertEqual(pow(2,3,21),8);self.assertEqual(pow(2,6,21),1)
        self.assertTrue(all(pow(2,q,21)!=1 for q in (1,2,3)))

    def test_18_kraus_extraction_and_mutual_information(self):
        gamma=.75;c=math.sqrt(1-gamma);s=math.sqrt(gamma)
        u=[[1,0,0,0],[0,c,s,0],[0,-s,c,0],[0,0,0,1]]
        self.same(mm(adj(u),u),tensor(I,I))
        ks=[[[u[2*i+j][2*k] for k in range(2)] for i in range(2)] for j in range(2)]
        self.same(ks[0],[[1,0],[0,c]]);self.same(ks[1],[[0,s],[0,0]])
        v=tensor(plus,zero);joint=projector(mm(u,v))
        reduced=[[sum(joint[2*i+j][2*k+j] for j in range(2)) for k in range(2)] for i in range(2)]
        self.same(reduced,channel(projector(plus),ks))
        # Compute information directly from joint probabilities, independently of H(Y)-H(Y|X).
        joint=[[3/8,1/8],[1/8,3/8]]
        px=[sum(row) for row in joint];py=[sum(col) for col in zip(*joint)]
        mutual=sum(joint[x][y]*math.log2(joint[x][y]/(px[x]*py[y])) for x in range(2) for y in range(2))
        self.assertAlmostEqual(mutual,1-entropy([.25,.75]))
        self.assertAlmostEqual(mutual,.18872187554086717)


if __name__ == '__main__':
    unittest.main(verbosity=2)
