<div align="center">

# Otwin:Open-source tools for building physics-informed digital twins of engineering assets

[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen?style=flat-square)](https://opensource.org/license/apache-2-0)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/downloads/)

[Models of physical assets](#models-of-physical-assets) ·
[What we provide](#what-the-project-provides) ·
[How it fits together](#how-the-three-fit-together) ·
[Where to start](#where-to-start) ·
[Status](#current-status) ·
[Contributing](#contributing)

</div>


A digital twin is a model of a physical asset that is kept in step with the
asset's sensors and used to predict what it will do next. Otwin is the modelling,
estimation and validation layer of one: you write the physics, it stays
synchronised with the measurements, and it reports how far the resulting forecast
can be trusted.

It is aimed at engineers who need a defensible model of a real asset — a battery
bank, an electrical machine, a hydraulic circuit, a thermal network — and who
will have to answer the question *how accurate is it, and how do you know?*


## Models of physical assets

Models of physical assets are routinely used to support decisions: when to
schedule maintenance, how much capacity remains, whether a unit can meet a duty
cycle. Two failure modes are common enough to be worth designing against.

**A model extrapolates outside the range it was fitted to, and gives no
indication that it has.** A model fitted to a year of operating data will
reproduce that year. Asked about a longer horizon or an operating point never
measured, a purely fitted model can drift in a way that violates conservation of
energy, and nothing in the output reports it.

**A reported accuracy figure does not survive scrutiny.** A model evaluated on a
randomly partitioned time series is being tested on interpolation, not on
forecasting. Reported without a reference forecaster, an error figure says
nothing about whether the model beats repeating the last measured value.

Otwin addresses the first by writing models in a form where the energy balance
is a property of the algebra rather than of the fit, and the second by making
out-of-sample partitioning and a reference forecaster the default in the
validation interface rather than an option.


## What the project provides

| Repository | What it is |
|---|---|
| [**`otwin`**](https://github.com/otwin-core/otwin) | The Python library. Model class, numerical solvers, state estimators, forecast validation, and field connectors for SunSpec Modbus and Modbus TCP/RTU |
| [**`otwin-spec`**](https://github.com/otwin-core/otwin-spec) | The specification and its **type-test procedure**: a set of reference cases whose correct answers are known in closed form, used to verify that an implementation is right. Language-independent |
| [**`otwin-hybrid`**](https://github.com/otwin-core/otwin-hybrid) | A worked example in Python, Julia and R — predicting the end of life of a lithium-ion cell from the first 40 % of its life. Opens in Colab in one click |

---

## How the three fit together

The **library** implements a model form: a state-space system written in terms
of stored energy, internal power routing, dissipation, and external ports. If
you have drawn a bond graph or an equivalent circuit, this is the same
decomposition written as four functions. On top of that sit the estimators that
keep the model in step with sensor readings, and the validation layer that
measures the resulting forecasts.

The **specification** states what that form requires and provides a way to check
it. A model that declares this structure is asserting two algebraic properties
about its matrices, and those properties are what make the energy bound hold.
They are not visible in a test-set error figure — a model with a subtly wrong
interconnection matrix can score well on held-out data and still drift when
extrapolated. So they are tested directly, against reference systems whose
answers are known analytically: Torricelli discharge for a draining tank, the
steady state of a separately excited DC motor, entropy production in a two-body
heat exchanger.

This follows the same pattern as a **type test** in IEC and IEEE practice: a
one-time verification that a design meets its stated requirements, performed
against defined test cases rather than against a previous run of the same
software. Because the test suite communicates with an implementation over a
process boundary rather than by importing it, it can verify an implementation
written in any language.

The **worked example** is where the project started, as a tutorial on building a
digital twin of a lithium-ion battery. It remains a tutorial, and it reports its
own results including the case where a straight line beats the physics-based
model on RMSE.

### Scope, against the formal definition

IEEE PES Technical Report **TR137**, *Digital Twin of Large-Scale Power Systems*
(December 2025), defines a digital twin as a *dynamic, synchronised virtual
replica that integrates physics-based and data-driven models with real-time
sensor data*. The discriminator commonly used to separate a twin from a
simulation is bidirectional, automated data exchange with the asset.

Otwin implements the physics-and-data model (known in AI systems as white and grey box models), the real-time ingestion, the state
synchronisation and the predictive layer. It does **not** write back to the
asset — every connector is read-only, and closed-loop actuation is deliberately
out of scope. The asset-to-model direction is closed; the model-to-asset
direction is left to your own control layer, where it belongs alongside the
safety case.


## Where to start

| If you want to… | Go to |
|---|---|
| See a complete worked example before reading anything | [`otwin-hybrid`](https://github.com/otwin-core/otwin-hybrid) — one click into Colab, in Python, Julia or R |
| Build a twin of a physical asset and validate its forecasts | [`otwin`](https://github.com/otwin-core/otwin) — installation, the model form, and worked models |
| Understand what the model form requires, formally | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) — the specification document |
| Verify your own implementation, in any language | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) — `otwin-conformance` |


## Current status

| | |
|---|---|
| **Status** | Pre-1.0. Usable and tested; expect breaking API changes before version 1.0. Pin a version in your project |
| **Distribution** | Not yet on PyPI. Install from source: `pip install git+https://github.com/otwin-core/otwin.git` |
| **Languages** | Python. Julia and MATLAB implementations are open contributor positions, not yet written |
| **Maintainers** | One. There is no governance structure yet, and there will not be one until there is more than one maintainer |
| **Deployment** | The methods were presented at the IEEE PES General Meeting 2026, in the Energy Storage & Stationary Battery Committee panel *AI-powered Digital Twins for Grid-Scale Energy Storage* (paper 26PESGM2792). There is no production deployment of the library on an operating asset. If you deploy it, an issue saying so would be useful |
| **Licence** | Apache 2.0 throughout |



## Contributing

You can contribute to this project as maintainer or creator. We have several ideas that will strenghten the project:

- **A physical system.** A model of something not yet in the catalogue —
a heat exchanger network, a hydraulic actuator, a synchronous machine, a
distillation column. What it takes: four functions of the state, plus one result
you know in advance (a steady state, a conservation law, an efficiency, an exact
solution) used as its test. Continuous integration checks the structural
properties automatically, so review is a short conversation about whether the
model is correct and properly cited, not an audit of your algebra. You need to
know your own domain and nothing about this library's internals.

- **A reference case for the specification.** A physical system with an
analytically known answer that no current case covers. It also needs a
deliberately faulty implementation demonstrating that the check catches the
fault it was written for — a check that has never been shown to fail is not
evidence.

- **A Julia or MATLAB implementation.** Because the type-test procedure verifies
an implementation over a process boundary, a second-language implementation is
well-defined work with an objective completion criterion: pass the test suite
unmodified. Scope is roughly a thousand lines. Both positions are open.

To take a position, open an issue titled `Maintainer: <your name>` on the
relevant repository, or email javier@jmarin.info. It means reviewing pull
requests in your area and having an opinion when a design decision touches it.
It does not mean writing code on a schedule.


## Background reading

- IEEE PES Technical Report **TR137** (2025). *Digital Twin of Large-Scale Power
  Systems: Fundamentals, Challenges, and Future Prospects.* PSOPE Committee.
- van der Schaft, A. & Jeltsema, D. (2014). *Port-Hamiltonian Systems Theory: An
  Introductory Overview.* Foundations and Trends in Systems and Control.
- Karnopp, D., Margolis, D. & Rosenberg, R. *System Dynamics: Modeling,
  Simulation, and Control of Mechatronic Systems.* Wiley.
- Willems, J. C. (1972). *Dissipative dynamical systems.* Archive for Rational
  Mechanics and Analysis, 45(5).
- ISO 13374 — *Condition monitoring and diagnostics of machines: data
  processing, communication and presentation.*
- ISO 13381-1:2015 — *Condition monitoring and diagnostics of machines:
  prognostics.*

Each repository carries a `CITATION.cff`. Cite the components you use.
