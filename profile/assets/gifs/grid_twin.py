"""Grid inertia twin: swing equation from otwin rotational parts, inertia estimated
from every small disturbance, low point of frequency forecast for the largest-unit trip.
The grid is simulated, with PMU noise. Numbers are illustrative of a mid-size grid."""
import json, warnings, numpy as np, otwin
from otwin.system import System
from otwin.components.rotational import Inertia, RotationalDamper, TorsionSpring, TorqueSource, Housing
from otwin.forecast import split_conformal
warnings.filterwarnings("ignore")
F0, LIMIT, TRIP, BAT = 50.0, -0.8, 1000.0, 600.0     # Hz, design limit 49.2 Hz, largest unit MW, battery MW/Hz-equivalent sizing below

def grid(battery=False):
    g = Inertia(4000.0, name="grid")                       # M = 2 E / f0   [MW s / Hz]
    load = RotationalDamper(500.0, name="load")            # load self-regulation [MW / Hz]
    gov = RotationalDamper(2200.0, name="governor")        # droop of the plants on primary control
    turb = TorsionSpring(2200.0 / 7.0, name="turbine")     # with a 7 s turbine lag
    ev = TorqueSource(None, name="event"); ref = Housing(name="ref")
    parts = [g, load, gov, turb, ev, ref]
    if battery:
        bd = RotationalDamper(BAT / 0.6, name="battery"); bs = TorsionSpring(BAT / 0.6 / 0.3, name="inverter")   # 600 MW at a 0.6 Hz dip, 0.3 s response
        parts += [bd, bs]
    s = System(*parts, name="grid")
    s.connect(g.shaft, load.a, gov.a, ev.shaft); s.connect(gov.b, turb.a)
    if battery: s.connect(g.shaft, bd.a); s.connect(bd.b, bs.a); s.connect(bs.b, load.b, turb.b, ref.port)
    else: s.connect(load.b, turb.b, ref.port)
    return otwin.compile(s)

M_of = lambda E: 2 * E * 1000 / F0                       # E in GW s
T = np.arange(0, 30, 0.05)
def nadir(model, E):
    tr = model.with_parameters({"grid.inertia": M_of(E)}).simulate(t=T, inputs=np.where(T >= 1, -TRIP, 0.0)[:, None])
    return float(np.asarray(tr["grid.angular_velocity"]).min())

if __name__ == "__main__":
    rng = np.random.default_rng(11)
    base, withbat = grid(), grid(battery=True)
    EG = np.arange(30, 171, 2.0)
    NAD = [nadir(base, e) for e in EG]; NADB = [nadir(withbat, e) for e in EG]
    # day-ahead plan of synchronous kinetic energy, from unit status (GW s), 05:00..21:00
    steps = [(5, 150), (7.5, 138), (8.5, 124), (9.5, 108), (10.5, 94), (11.5, 84), (12.5, 76), (15.5, 84), (16.5, 98), (17.5, 114), (18.5, 130), (19.5, 144)]
    def plan(h): return [v for t0, v in steps if t0 <= h + 1e-9][-1]
    ratio = lambda h: 0.83 + 0.02 * np.sin(h / 2.3)            # the real grid holds less than the plan says
    true = lambda h: plan(h) * ratio(h)
    # disturbances: every ~22 minutes a small loss or gain of 120-350 MW, seen by a PMU at 10 Hz
    ev_h = np.cumsum(rng.exponential(22 / 60, 80)) + 5.1; ev_h = ev_h[ev_h < 20.8]
    t = np.arange(0, 20, 0.1); events = []
    for h in ev_h:
        dp = rng.choice([-1, 1]) * rng.uniform(120, 350); u = np.where(t >= 2, dp, 0.0)[:, None]
        clean = np.asarray(base.with_parameters({"grid.inertia": M_of(true(h))}).simulate(t=t, inputs=u)["grid.angular_velocity"])
        e = rng.normal(0, 0.004, t.size); n = np.zeros_like(e)
        for i in range(1, t.size): n[i] = 0.7 * n[i - 1] + e[i]
        f = clean + n
        fit = otwin.fit_parameters(base, t, {"grid.angular_velocity": f}, ["grid.inertia"], inputs=u, bounds={"grid.inertia": (300, 20000)})
        Ehat = fit.model.parameters["grid.inertia"] * F0 / 2 / 1000
        events.append(dict(h=float(h), dp=float(dp), E_true=float(true(h)), E_plan=float(plan(h)), E_hat=float(Ehat),
                           f=f.tolist(), f_twin=np.asarray(fit.model.simulate(t=t, inputs=u)["grid.angular_velocity"]).tolist()))
    err = np.array([abs(e["E_hat"] - e["E_true"]) / e["E_true"] for e in events])
    print(f"{len(events)} disturbances; inertia estimate error median {np.median(err)*100:.1f} %, max {err.max()*100:.1f} %")
    json.dump(dict(EG=EG.tolist(), NAD=NAD, NADB=NADB, steps=steps, events=events, t=t.tolist()), open("grid.json", "w"))
