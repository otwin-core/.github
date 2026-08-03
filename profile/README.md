<div align="center">

# Otwin

**A collection of tools for creating digital twins and modeling systems, developed in the Python programming language, with bindings to other languages such as Julia and MATLAB.**

Physics-informed twins that stay consistent over long horizons and tell you when they are uncertain.

[![Specification](https://img.shields.io/badge/specification-v1.0%20draft-blueviolet?style=flat-square)](https://github.com/otwin-core/otwin-spec)
[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen?style=flat-square)](https://opensource.org/licenses/apache)

</div>

---

## This is a tools ecosystem, not a library

Otwin is **not one package**. It is a set of tools that compose, each installable on its own, each doing one thing.

That is deliberate. Digital twins span physics, numerics, statistics and forecasting, and almost nobody needs all of it. Someone validating a load forecast needs the evaluation harness and nothing else. Someone modelling a pumped-hydro plant needs the port-Hamiltonian core and never touches uncertainty quantification. One monolith would make both carry the other's dependencies forever.

**There is no `pip install otwin`.** Install the tool you need:

```bash
pip install otwin-phs          # port-Hamiltonian systems + structure-preserving integration
pip install otwin-systems      # a library of physical models
pip install otwin-eval         # leakage-free forecast validation
pip install otwin-uq           # calibrated uncertainty
```

They compose because they all implement one small contract — [`otwin-base`](https://github.com/otwin-core/otwin-base) — and because a conformance suite verifies that they actually do.

---

## Where to start

| I want to… | Go here |
|---|---|
| **Understand the idea**, from a worked example in Python, Julia or R | [**`otwin-hybrid`**](https://github.com/otwin-core/otwin-hybrid) — one click into Colab |
| **Model a physical system** | [`otwin-systems`](https://github.com/otwin-core/otwin-systems) + [`otwin-phs`](https://github.com/otwin-core/otwin-phs) |
| **Validate a forecast honestly** | [`otwin-eval`](https://github.com/otwin-core/otwin-eval) — useful far beyond digital twins |
| **Attach uncertainty that means something** | [`otwin-uq`](https://github.com/otwin-core/otwin-uq) |
| **See the numbers, reproducibly** | [`otwin-benchmarks`](https://github.com/otwin-core/otwin-benchmarks) |
| **Check my own implementation** | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) — `otwin-conformance` |

---

## What holds it together

Three things, and they are why the tools compose rather than merely coexist.

### 1. One contract

[`otwin-base`](https://github.com/otwin-core/otwin-base) contains types and protocols and **zero algorithms** — a test fails the build if anyone adds one. Every tool depends on it; it depends on NumPy.

A model satisfies the contract *structurally*. No inheritance, no registration, no import from Otwin in your own code:

```python
class WaterTank:
    n_states, n_inputs = 1, 1
    def H(self, x): ...    # the energy stored
    def J(self, x): ...    # routed losslessly   — must satisfy J = -Jᵀ
    def R(self, x): ...    # dissipated          — must be PSD
    def g(self, x): ...    # the port
    def rhs(self, x, u, t): ...
    def observe(self, x, u, t): ...

from otwin_base import PortHamiltonianModel
isinstance(WaterTank(), PortHamiltonianModel)   # True
```

That is what lets you write a tool for this ecosystem without asking anyone's permission.

### 2. A claim that can be falsified

Declaring port-Hamiltonian structure asserts that `J` is skew-symmetric and `R` positive semidefinite — and therefore that forecasts **cannot create energy, at any horizon**.

That claim is the reason to use Otwin instead of a neural network. It is also invisible on a test set: a model with a subtly wrong `J` scores beautifully on held-out data and then drifts when you extrapolate, which is exactly the situation the structure was supposed to protect you from.

So [`otwin-spec`](https://github.com/otwin-core/otwin-spec) checks it, against answers known in closed form:

```
$ otwin-conformance python
    PASS  dc_motor_steady_state       ω_ss = VK/(R_e·b + K²), to 1e-5
    PASS  pumped_hydro_conservation   dH/dt = −c(p_u−p_l)², analytic leakage
    PASS  water_tank_drain_law        Torricelli's exact solution
    PASS  iphs_second_law             dU/dt = 0 and σ ≥ 0, rising
    ...
    8 passed, 0 failed — conformant: yes
```

The suite ships deliberately broken implementations and asserts each is caught — including one containing **no physics at all**, which is the adversary a suite like this usually fails to survive.

### 3. Honest evaluation by default

Temporal splits, not random ones. Baselines that are mandatory rather than optional. Skill score as the headline, because a model with excellent R² can still lose to repeating yesterday's value.

---

## Where to contribute

**You do not need to know anything about Otwin's internals to contribute a physical system.** You need to know your own domain. That is the widest door here, deliberately.

| I know about… | Contribute | Where |
|---|---|---|
| **a physical system** — thermal, electrical, chemical, mechanical, hydraulic | a model: `H`, `J`, `R`, `g` + one closed-form check | [`otwin-systems`](https://github.com/otwin-core/otwin-systems/labels/good-first-system) |
| irreversible thermodynamics | entropy-producing systems | [`otwin-iphs`](https://github.com/otwin-core/otwin-iphs) |
| forecasting and validation | protocols, baselines, metrics | [`otwin-eval`](https://github.com/otwin-core/otwin-eval) |
| uncertainty quantification | conformal, GP, ensembles | [`otwin-uq`](https://github.com/otwin-core/otwin-uq) |
| numerical analysis | structure-preserving integrators | [`otwin-phs`](https://github.com/otwin-core/otwin-phs) |
| **MATLAB** | **own the MATLAB binding** | [`otwin-matlab`](https://github.com/otwin-core/otwin-matlab) |
| **Julia** | **own the Julia binding** | [`Otwin.jl`](https://github.com/otwin-core/Otwin.jl) |
| a real asset with real data | a case study, with a DOI and your name on it | [`otwin-benchmarks`](https://github.com/otwin-core/otwin-benchmarks) |

### What contributing a system actually involves

Four functions, plus **one result you know in advance** — a steady state, a conservation law, an efficiency, an exact solution.

CI proves `J` is skew, `R` is PSD, the power balance holds, and your analytic check passes. **Review is then a ten-minute conversation about whether the model is interesting and correctly cited — not a two-hour audit of your algebra.** That is what makes this maintainable by one person and open to everyone.

`water_tank` is the worked example: a complete system in about forty lines, with Torricelli's exact solution as its test.

---

## Open maintainer slots

Scoped on purpose. "Co-maintain Otwin" is unanswerable; "own the MATLAB binding" is a decision you can make in a minute.

| Slot | Who it suits |
|---|---|
| **[`otwin-matlab`](https://github.com/otwin-core/otwin-matlab)** | a BESS, utility or power-systems engineer — the language the audience actually uses |
| **[`Otwin.jl`](https://github.com/otwin-core/Otwin.jl)** | someone in the Julia / SciML community |
| **[`otwin-iphs`](https://github.com/otwin-core/otwin-iphs)** | anyone working in the Ramírez–Maschke–Sbarbaro line |
| **[`otwin-uq`](https://github.com/otwin-core/otwin-uq)** | a conformal-prediction researcher |

It means reviewing pull requests in your area and having an opinion when a design decision touches it. It does **not** mean writing code on a schedule, and it does not require knowing the rest of the ecosystem. Stop whenever you like and we will say so gracefully.

Open an issue titled `Maintainer: <your name>`, or email javier@jmarin.info. A short yes is enough.

---

## The tools

| Repository | Language | Maturity | What it is |
|---|---|---|---|
| [`otwin-base`](https://github.com/otwin-core/otwin-base) | Python | **Medium** | the contract: types and protocols, no algorithms |
| [`otwin-spec`](https://github.com/otwin-core/otwin-spec) | Python + JSON | **Medium** | the specification and its conformance suite |
| [`otwin-phs`](https://github.com/otwin-core/otwin-phs) | Python | **Medium** | port-Hamiltonian systems, structure-preserving integration |
| [`otwin-systems`](https://github.com/otwin-core/otwin-systems) | Python | **Medium** | the library of physical models |
| [`otwin-eval`](https://github.com/otwin-core/otwin-eval) | Python | **Medium** | leakage-free validation |
| [`otwin-uq`](https://github.com/otwin-core/otwin-uq) | Python | **Medium** | calibrated uncertainty |
| [`otwin-iphs`](https://github.com/otwin-core/otwin-iphs) | Python | **Low** | irreversible port-Hamiltonian systems |
| [`otwin-learn`](https://github.com/otwin-core/otwin-learn) | Python | **Low** | networks with enforced structure |
| [`otwin-hybrid`](https://github.com/otwin-core/otwin-hybrid) | Python · Julia · R | **Tutorial** | the worked example this project grew from |
| [`otwin-benchmarks`](https://github.com/otwin-core/otwin-benchmarks) | Python | **Medium** | worked examples, every number on CI |
| [`otwin-data`](https://github.com/otwin-core/otwin-data) | Python | **Medium** | datasets by identity: checksums, licences, citations |
| [`Otwin.jl`](https://github.com/otwin-core/Otwin.jl) | Julia | **Pending** | contract written, binding not |
| [`otwin-matlab`](https://github.com/otwin-core/otwin-matlab) | MATLAB | **Pending** | contract written, binding not |
| [`otwin-agents`](https://github.com/otwin-core/otwin-agents) | Python | **Research** | an open question, not a product |

**Medium** — usable and tested; expect breaking changes before 1.0.
**Low** — works, and is honest about what it does not cover.
**Pending** — announced and specified; not implemented.
**Research** — an open question.

Labelling our own packages "Research" is a credibility gain, not an admission. It tells you what to expect.

---

## Coming from somewhere else

- **Simulink** — you already think in blocks exchanging power through ports. A port-Hamiltonian model is that, with conservation guaranteed by algebra rather than by care.
- **PyBaMM** — PyBaMM gives you detailed electrochemistry. Otwin covers the systems around it, and treats battery State-of-Health as an *empirical law* rather than an energy balance, which is the correct model class for capacity fade.
- **scikit-learn** — same shape: choose a structure, fit, validate. The differences are that the structure comes from physics, validation is temporal by default, and a baseline is mandatory.

---

## How to cite

Each repository has a `CITATION.cff` and its own DOI. **Cite the components you used** — `print_citations()` will tell you which, including the papers behind the methods.

## License

Apache 2.0 throughout.
