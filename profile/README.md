<div align="center">

# What is Otwin

[![Specification](https://img.shields.io/badge/specification-v1.0%20draft-blueviolet?style=flat-square)](https://github.com/otwin-core/otwin-spec)
[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen?style=flat-square)](https://opensource.org/licenses/apache)

</div>

It started as one repository: a tutorial showing how to build a digital twin of a Li-ion battery in Python. The original repository is still here at ´otwin-hybrid´. Now we have opened the idea because a tutorial can only be copied and a contract can be built on. A contract is different because it's a fixed, published statement of shape: a twin is anything that has an energy function, a routing matrix, a dissipation matrix, a port, and a right-hand side.

We split into three stacked layers.

- At the bottom is a contract: `otwin-base`. Types and protocols, no algorithms, enforced by a test that fails the build if anyone adds one. It defines what counts as a twin — a thing with an energy function, an internal routing matrix, a dissipation matrix, a port. 

- Above that is a specification that's executable: `otwin-spec`. A schema for describing a twin, a set of fixtures whose answers are known in closed form, and a runner — `otwin-conformance` — that tells you whether your implementation is right-

- Above that is everything that actually computes. `otwin-phs` and `otwin-iphs` for port-Hamiltonian and irreversible port-Hamiltonian dynamics. `otwin-learn` for neural networks constrained to that same form. `otwin-systems` for implementing a catalogue of physical models — water tank, DC motor, pumped hydro. `otwin-uq` for uncertainty that has been checked against measured coverage, and `otwin-eval` for validation. Then the supporting cast: `otwin-data`, `otwin-benchmarks`, `otwin-docs`, `otwin-notes`, `otwin-agents`. And three bindings — R MATLAB, Julia.

---

## Install

To install the tool you need:

```bash
pip install otwin-phs          # port-Hamiltonian systems + structure-preserving integration
pip install otwin-systems      # a library of physical models
pip install otwin-eval         # leakage-free forecast validation
pip install otwin-uq           # calibrated uncertainty
```

All them implement one small contract — [`otwin-base`](https://github.com/otwin-core/otwin-base)

---

## Where to start

| I want to… | Go here |
|---|---|
| **Understand the idea**, from a worked example in Python, Julia or R | [**`otwin-hybrid`**](https://github.com/otwin-core/otwin-hybrid) — one click into Colab |
| **Model a physical system** | [`otwin-systems`](https://github.com/otwin-core/otwin-systems) + [`otwin-phs`](https://github.com/otwin-core/otwin-phs) |
| **Validate a forecast** | [`otwin-eval`](https://github.com/otwin-core/otwin-eval) — useful far beyond digital twins |
| **Attach calibrated uncertainty** | [`otwin-uq`](https://github.com/otwin-core/otwin-uq) |
| **See some benchmark** | [`otwin-benchmarks`](https://github.com/otwin-core/otwin-benchmarks) |
| **Check my own implementation** | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) — `otwin-conformance` |

---

## How it works

Otwin has three components:

### 1. Contract

[`otwin-base`](https://github.com/otwin-core/otwin-base) contains types and protocols and **zero algorithms** — a test fails the build if anyone adds one. Every tool depends on it; it depends on NumPy in python.

A model satisfies the contract *structurally*:
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

### 2. A standarized physical model

A port-Hamiltonian system is a way of writing down a physical model in terms of its energy rather than in terms of its behaviour. When we want to model something we write "here is how the state changes each instant". We write one function, fitted or derived, that maps the current state to a rate of change. 

The port-Hamiltonian way splits the same model into four separate statements about energy, and the dynamics fall out of them:

- How much energy is stored, as a function of the state. For a water tank, the water sitting in it.
- Where energy moves internally, losing none of it. Kinetic becoming potential, electrical becoming mechanical. This is the `J` part.
- Where energy leaves for good. Friction, resistance, viscous drag. This is `R`.
- Where energy enters or exits through the boundary — the port. The pump feeding the tank, the valve draining it.

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

### 3. Checklist

We do a checklist and run it against your implementation. If it passes, it will be otwin-conformant
Temporal splits, not random ones. Baselines that are mandatory rather than optional. Skill score as the headline, because a model with excellent $R^2$ can still lose to repeating yesterday's value.

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
