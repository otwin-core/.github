<div align="center">

<img src="https://raw.githubusercontent.com/otwin-core/.github/main/profile/assets/otwin_header.png">

# Otwin: open-source physics for Digital Twins

[![License](https://img.shields.io/badge/license-Apache%202.0-brightgreen.svg?style=flat-square)](https://opensource.org/license/apache-2-0)
[![Python](https://img.shields.io/github/actions/workflow/status/otwin-core/otwin/ci.yml?branch=main\&label=python\&logo=github)](https://github.com/otwin-core/otwin/actions/workflows/ci.yml)
[![Rust](https://img.shields.io/github/actions/workflow/status/otwin-core/otwin/rust.yml?branch=main\&label=rust\&logo=github)](https://github.com/otwin-core/otwin/actions/workflows/rust.yml)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/14061/badge)](https://www.bestpractices.dev/projects/14061)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/otwin-core/otwin/badge)](https://scorecard.dev/viewer/?uri=github.com/otwin-core/otwin)
[![REUSE status](https://api.reuse.software/badge/github.com/otwin-core/otwin)](https://api.reuse.software/info/github.com/otwin-core/otwin)
[![SLSA 2](https://slsa.dev/images/gh-badge-level2.svg)](https://github.com/otwin-core/otwin/attestations)

</div>

<br>

<img src="assets/gifs/otwin-battery-twin.gif" width="100%" alt="A battery cell on a cycler. The twin follows its capacity cycle by cycle, forecasts it with a 90 % range, and asks for a replacement before the cell reaches end of life.">

<sub>Real data from 44 cells the twin had never seen (Severson et al., 2019). On every one of them the replacement order came before end of life, a median of 76 cycles ahead. [Script](assets/gifs/battery_twin.py)</sub>

# The idea

A model of a battery, a pump or a power grid is useful on paper. It becomes a **Digital Twin** when it stays connected to the real equipment, learns what cannot be measured from what can, and says what is likely to happen next, with a range and a clear limit on what it does not know.

Otwin is the open-source toolkit for that. You describe the equipment with physical parts (masses, springs, pipes, pumps, cells, inertias). Otwin turns them into a model that cannot create energy out of nothing, fits it to your sensors, and forecasts with a range that was tested on data the model never saw.

```bash
pip install otwin
```

# Three twins, three decisions

<img src="assets/gifs/otwin-grid-twin.gif" width="100%" alt="A power grid twin estimates the real inertia of the grid from every small disturbance and warns two hours ahead that a large trip could push frequency below 49.2 Hz.">

<sub>**Power grid.** Every small disturbance tells the twin how much spinning mass is holding the frequency. The operator's plan says the grid is safe at midday. The measured grid is lighter, so the twin asks for battery fast response two hours ahead. Simulated grid with PMU noise. [Script](assets/gifs/grid_twin.py)</sub>

<br>

<img src="assets/gifs/otwin-pump-twin.gif" width="100%" alt="A pump feeding a filter press. The twin estimates cloth fouling from the pressure drop and shows when cleaning becomes cheaper than the extra energy.">

<sub>**Pump and filter press.** Nobody can measure how fouled the filter cloths are. The twin estimates it from the pressure drop and says when cleaning costs less than the extra energy the pump is burning. Simulated plant with sensor noise. [Script](assets/gifs/pump_twin.py)</sub>

The code under each drawing is the code that produced its numbers.

# From a model to a twin

```mermaid
flowchart LR
    A["Equipment"] <--> B["Sensors"]
    C["Physical model"] --> D["What cannot be measured"]
    B --> D
    D --> E["Forecast with a range"]
    E --> F["Tested on unseen data"]
    F --> G["A decision you can defend"]
```

Every step is in the open, and every claim can be checked: another implementation of the same model must give the same answer, and the [specification](https://github.com/otwin-core/otwin-spec) has the tests to prove it.

# Repositories

| Repository | What it is |
|---|---|
| [**`otwin`**](https://github.com/otwin-core/otwin) | The Python library: build, run, fit, forecast and check physical models, and connect them to field data |
| [**`otwin-spec`**](https://github.com/otwin-core/otwin-spec) | What an Otwin model means, written down, with a test suite any implementation must pass |
| [**`otwin-hybrid`**](https://github.com/otwin-core/otwin-hybrid) | A complete example: a battery degradation twin that mixes physics and machine learning |
| [**`otwin-systems`**](https://github.com/otwin-core/otwin-systems) | A growing catalogue of physical systems with known reference results |

# Where to start

| I want to... | Go to |
|---|---|
| See a complete twin | [`otwin-hybrid`](https://github.com/otwin-core/otwin-hybrid) |
| Build my own | [`otwin`](https://github.com/otwin-core/otwin) |
| Check an implementation | [`otwin-spec`](https://github.com/otwin-core/otwin-spec) |
| Contribute a system, a test or an example | [Contributing guide](https://github.com/otwin-core/otwin/blob/main/CONTRIBUTING.md) |

<br>

<div align="center">

#### A twin should not only predict. It should show why its prediction can be trusted, and say so when the evidence is not there.

Otwin, 2026 · Apache 2.0

</div>
