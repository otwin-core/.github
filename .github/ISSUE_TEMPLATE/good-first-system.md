---
name: "Contribute a physical system"
about: "Add a new model to otwin-systems. No Otwin knowledge required — just your domain."
title: "System: <name>"
labels: ["good-first-system", "enhancement"]
---

## The system

<!-- One or two sentences. What is it, and who would want a twin of it? -->

## The energy structure

A port-Hamiltonian model is four functions. Write them however you like —
LaTeX, plain text, a photo of a napkin.

- **State** `x` = <!-- the energy variables, e.g. [flux linkage, angular momentum] -->
- **`H(x)`** — the energy stored = <!-- ... -->
- **`J(x)`** — what is routed losslessly (must satisfy `J = -Jᵀ`) = <!-- ... -->
- **`R(x)`** — what is dissipated (must be positive semidefinite) = <!-- ... -->
- **`g(x)`** — the port: how input enters and output is read = <!-- ... -->

If your system only *degrades* — capacity fade, wear, fatigue, corrosion — it
has no energy function and no port. That is fine and common. Say so here, and
give the trend law instead; it belongs in the empirical-law family, not this one.

## The closed-form check

**This is the important part.** What is one thing about this system whose answer
you know in advance, without fitting anything?

Good examples from existing models:

- a **steady state**: the DC motor must converge to `ω_ss = VK/(R_e·b + K²)`
- a **conservation law**: a sealed pumped-hydro store must hold its energy
- an **efficiency**: round-trip must equal `η_pump · η_turbine`
- an **exact solution**: a draining tank must follow `h(t) = (√h₀ − c_d·a·√(2g)·t/2A)²`

<!-- Yours: -->

- Quantity:
- Closed-form value:
- Reasonable tolerance:

## The reference

<!-- Where does this model come from? A paper, a textbook, a standard. If it is
your own derivation, say so — that is fine, it just gets reviewed differently. -->

## Checklist

- [ ] I have stated `H`, `J`, `R`, `g` (or the trend law)
- [ ] I have one closed-form result the model must reproduce
- [ ] I have a reference, or have said the derivation is mine

---

**What happens next.** Someone will confirm the structure looks right, then you
open a PR against [`otwin-systems`](https://github.com/otwin-core/otwin-systems)
adding the model and its test. CI proves `J` is skew, `R` is PSD, and your
closed-form check holds — so review is a short conversation, not an audit.

The worked example to copy is `water_tank`: a complete system in about forty
lines, with its exact solution as the test.
