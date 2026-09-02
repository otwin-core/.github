<div align="center">

<img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/otwin-woodmark.png"  width="35%">

# Otwin: open-source tools for building physics-informed digital twins

<br>

[![Maintenance](https://img.shields.io/badge/Maintained-yes-brightgreen.svg?style=flat-square)](https://github.com/otwin-core/)
[![Contibutors](https://img.shields.io/badge/Contributors-Wellcome-brightgreen.svg?style=flat-square)](https://shields.io/)
[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen?style=flat-square)](https://opensource.org/license/apache-2-0)

<br>

[Models of physical assets](#models-of-physical-assets) ·
[What we provide](#what-the-project-provides) ·
[How to start](#how-to-start) ·
[Model-to-asset](#model-to-asset) ·
[Status](#current-status) ·
[Contributing](#contributing)

</div>

<br>

A digital twin is a model of a physical asset that is kept in step with the
asset's sensors and used to predict what it will do next. Otwin is the modelling,
estimation and validation layer of one: you write the physics, it stays
synchronised with the measurements, and it reports how far the resulting forecast
can be trusted.

It is aimed at engineers who need a functional model of a real asset — a battery
bank, an electrical machine, a hydraulic circuit, a thermal network.


## Models of physical assets

Models of physical assets are used to support decisions: when to
schedule maintenance, how much capacity remains, whether a unit can meet a duty
cycle. Two failure modes are common enough to be worth designing against.

- **A model extrapolates outside the range it was fitted to, and gives no
indication that it has.** A model fitted to a year of operating data will
reproduce that year. Asked about a longer horizon or an operating point never
measured, a purely fitted model can drift in a way that violates conservation of
energy, and nothing in the output reports it.

- **A reported accuracy figure does not survive scrutiny.** A model evaluated on a
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
| [**`otwin-hybrid`** ](https://github.com/otwin-core/otwin-hybrid) | A tutorial on building a digital twin of a lithium-ion battery degradation |

<br>

- **`otwin`**: Implements a model form: a state-space system written in terms of stored energy, internal power routing, dissipation, and external ports. If you have drawn a bond graph or an equivalent circuit, this is the same decomposition written as four functions. On top of that sit the estimators that keep the model in step with sensor readings, and the validation layer that measures the resulting forecasts

- **`otwin-spec`**: It states what that form requires and provides a way to check it. A model that declares this structure is asserting two algebraic properties about its matrices, and those properties are what make the energy bound hold. They are not visible in a test-set error figure — a model with a subtly wrong interconnection matrix can score well on held-out data and still drift when extrapolated. So they are tested directly, against reference systems whose answers are known analytically: Torricelli discharge for a draining tank, the steady state of a separately excited DC motor, entropy production in a two-body heat exchanger. We follow the specifications set in IEC and IEEE practice: a one-time verification that a design meets its stated requirements, performed against defined test cases rather than against a previous run of the same software. Because the test suite communicates with an implementation over a process boundary rather than by importing it, it can verify an implementation written in any language |

- **`otwin-hybrid`**: A tutorial on building a digital twin of a lithium-ion battery. It remains a tutorial, and it reports its own results including the case where a straight line beats the physics-based model on RMSE.

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/otwin-core/otwin-hybrid)
[![Stars](https://img.shields.io/github/stars/otwin-core/otwin-hybrid?style=flat-square&label=Stars)](https://github.com/otwin-core/otwin-hybrid/stargazers)
[![Forks](https://img.shields.io/github/forks/otwin-core/otwin-hybrid?style=flat-square&label=Forks)](https://github.com/otwin-core/otwin-hybrid/forks)

</div>

<br>

## How to start

| If you want to… | Go to |
|---|---|
| See a complete worked example before reading anything | [`otwin-hybrid`](https://github.com/otwin-core/otwin-hybrid) — one click into Colab, in Python. Not yet available in other lamguages |
| Build a twin of a physical asset and validate its forecasts | [`otwin`](https://github.com/otwin-core/otwin) — installation, the model form, and worked models |
| Understand what the model form requires, formally | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) — the specification document |
| Verify your own implementation, in any language | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) — `otwin-conformance` |

<br>

## Model-to-asset

<div align="center">

<img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/IEEE.png"  width="55%">

</div>

<br>

IEEE PES Technical Report **PES-TR137**, *Digital Twin of Large-Scale Power Systems* (November 2025), defines a digital twin as a *dynamic, synchronised virtual replica that integrates physics-based and data-driven models with real-time sensor data*. The discriminator commonly used to separate a twin from a simulation is bidirectional, automated data exchange with the asset.

Otwin implements the physics-and-data model (known in AI systems as white and grey box models), the real-time ingestion, the state synchronisation and the predictive layer. It does NOT write back to the asset — every connector is read-only, and closed-loop actuation is deliberately out of scope. The asset-to-model direction is closed; the model-to-asset direction is left to your own control layer, where it belongs alongside the safety case.

<br>

## Current status

| | |
|---|---|
| **Status** | Pre-1.0. Usable and tested; expect breaking API changes before version 1.0. Pin a version in your project |
| **Distribution** | `pip install otwin` |
| **Languages** | Python. Julia and MATLAB implementations are open contributor positions, not yet written |
| **Maintainers** |There is no governance structure yet. We will create one when we have a relevant number of maintainers |
| **Deployment** | The methods were presented at the IEEE PES General Meeting 2026, in the Energy Storage & Stationary Battery Committee panel *AI-powered Digital Twins for Grid-Scale Energy Storage* (paper 26PESGM2792) |
| **Licence** | Apache 2.0 |

<br>

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

<br>

  
> Each repository carries a `CITATION.cff`. Cite the components you use.
