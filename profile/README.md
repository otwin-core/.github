<div align="center">

<img src="assets/brand/otwin-header.png" width="100%" alt="otwin: open digital twins of real equipment. A battery plant at dusk with a live dashboard over it: state of health 87.4 %, coverage 91 %, and a warning that the band width is trending up.">

<br>

<br>

[![License](https://img.shields.io/badge/license-Apache%202.0-7a2ffc.svg)](https://opensource.org/license/apache-2-0)
[![PyPI](https://img.shields.io/pypi/v/otwin?color=7a2ffc&cacheSeconds=3600)](https://pypi.org/project/otwin/)
[![Julia](https://github.com/otwin-core/otwin/actions/workflows/julia.yml/badge.svg)](https://github.com/otwin-core/otwin/tree/main/julia/Otwin.jl)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/otwin-core/otwin/badge)](https://scorecard.dev/viewer/?uri=github.com/otwin-core/otwin)
[![REUSE status](https://api.reuse.software/badge/github.com/otwin-core/otwin)](https://api.reuse.software/info/github.com/otwin-core/otwin)
[![SLSA 2](https://slsa.dev/images/gh-badge-level2.svg)](https://github.com/otwin-core/otwin/attestations)

</div>

<br>

# Welcome to the Otwin project

A model of a battery, a pump or a power grid becomes a digital twin when it stays connected to the real machine and can say how far to trust itself. Otwin is open-source software for building those twins. You describe the equipment as components and connections, the way its drawing reads — or bring a model from Modelica or Julia — and Otwin fits it to the machine's measurements, forecasts with a range whose coverage is measured on data the model never saw, audits what the model promised against what the machine did, and refuses to answer outside what was validated. It reads the measurements from the plant itself, over Modbus, SunSpec and OPC UA.

```bash
pip install otwin
```

<br>

# Where to start

| You want to | Start here |
|---|---|
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-forecast-dark.svg"><img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-forecast.svg" width="26" alt=""></picture> See a complete twin working | [**`otwin-hybrid`**](https://github.com/otwin-core/otwin-hybrid), a battery degradation twin in Python, Julia and R |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-core-dark.svg"><img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-core.svg" width="26" alt=""></picture> Build a model from physical parts | [**`otwin`**](https://github.com/otwin-core/otwin), with ten [tutorials](https://github.com/otwin-core/otwin/tree/main/tutorials) that cover every component on real equipment |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-estimators-dark.svg"><img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-estimators.svg" width="26" alt=""></picture> Check whether a model of your equipment can be trusted | [**`otwin`**](https://github.com/otwin-core/otwin): fit, calibrate, audit and refuse, in [tutorial 10](https://github.com/otwin-core/otwin/blob/main/tutorials/10_from_model_to_twin.md) |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-solvers-dark.svg"><img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-solvers.svg" width="26" alt=""></picture> Work in Julia | [**`Otwin.jl`**](https://github.com/otwin-core/otwin/tree/main/julia/Otwin.jl), the same implementation with Julia types in and out |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-fielddata-dark.svg"><img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-fielddata.svg" width="26" alt=""></picture> Connect a twin to the plant | [**`otwin`**](https://github.com/otwin-core/otwin) with the `modbus`, `sunspec` or `opcua` extras |
| <picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-refusal-dark.svg"><img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/brand/icons/icon-refusal.svg" width="26" alt=""></picture> Verify an implementation of the model format | [**`otwin-spec`**](https://github.com/otwin-core/otwin-spec), the specification and its test suite |

<br>

<div align="center">

<img src="assets/gifs/otwin-battery-twin.gif" width="90%" alt="A battery cell on a cycler. The twin follows its capacity cycle by cycle, forecasts it with a 90 % range, and asks for a replacement before the cell reaches end of life.">

<sub>Real data from 44 cells the twin had never seen (Severson et al., 2019). On every one of them the replacement order came before end of life, a median of 76 cycles ahead. [Script](assets/gifs/battery_twin.py)</sub>

</div>

<br>

# Repositories

| Repository | What it is |
|---|---|
| [**`otwin`**](https://github.com/otwin-core/otwin) | The library: components in six physical domains, the port-Hamiltonian compiler, the Rust engine, estimation, forecasting, auditing and field connectors — and `Otwin.jl` inside it |
| [**`otwin-spec`**](https://github.com/otwin-core/otwin-spec) | What an Otwin model means, written down, with a test suite any implementation must pass |
| [**`otwin-hybrid`**](https://github.com/otwin-core/otwin-hybrid) | A complete example: a battery degradation twin that combines physics and machine learning |
| [**`otwin-systems`**](https://github.com/otwin-core/otwin-systems) | A growing catalogue of physical systems with known reference results |

<br>

# About the project

The code behind Otwin has been public for more than eight years. It began with a Towards Data Science article, at a time when very little open software for digital twins existed, and has grown since then into the library, the specification and the examples above. In 2026 the project was presented at the IEEE PES General Meeting, in a panel on digital twins, at the invitation of Sandia National Laboratories.

<div align="center">

[![IEEE PES General Meeting 2026](https://img.shields.io/badge/IEEE%20PES%20General%20Meeting%202026-invited%20panel-00629B?logo=ieee&logoColor=white)](https://pes-gm.org/)
[![Towards Data Science](https://img.shields.io/badge/Towards%20Data%20Science-the%20original%20article-12100E?logo=medium&logoColor=white)](https://towardsdatascience.com/)

</div>

Every claim on these pages can be checked: the printed numbers in the tutorials are verified in CI, the drawings are produced by the scripts linked beside them, and another implementation of the same model must give the same answer as the specification's test suite.

<br>

# Resources

Documentation: [otwin.readthedocs.io](https://otwin.readthedocs.io) · Where the project is going: [ROADMAP.md](https://github.com/otwin-core/otwin/blob/main/ROADMAP.md) · Questions and ideas: [Discussions](https://github.com/otwin-core/otwin/discussions) · Bugs and agreed work: [Issues](https://github.com/otwin-core/otwin/issues) · A new component, a system or an example is the easiest way to contribute: [Contributing guide](https://github.com/otwin-core/otwin/blob/main/CONTRIBUTING.md)

<br>

<div align="center">

<sub> Each repository includes a `CITATION.cff`. Otwin is released under the [Apache License 2.0](https://github.com/otwin-core/otwin/blob/main/LICENSE). Copyright Javier Marín, 2026</sub>

</div>
