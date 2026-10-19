"""Battery health twin on real cells (Severson et al. 2019, MATR data).

Two-term fade law with fleet exponents, refitted as cycles arrive; a 90 % band
from out-of-sample rolling-origin residuals on 126 cells from three batches; scored on
44 cells of a fourth batch (b180412) the twin never saw.

Data: matr_cells.npz is the per-cycle discharge capacity and resistance of the
187 cells published by Severson et al., Nature Energy 4, 383 (2019),
https://data.matr.io/1/ (CC BY 4.0), reduced to one file.
"""
import json, numpy as np
from scipy.optimize import nnls
from otwin.forecast import rolling_origin_residuals, horizon_conformal, picp

EOL, N_REF, Z1, Z2, HOLDOUT, LEAD, HMAX = 0.88, 1000.0, 0.25, 2.80, "b180412", 100, 600

def clean(qd):                      # sensor dropouts (readings below half of EOL) hold the last good value
    q = qd.astype(float).copy()
    for i in range(1, q.size):
        if q[i] < 0.5 * EOL: q[i] = q[i - 1]
    return q

def life(q):                        # first cycle whose 5-point running median reaches the campaign's 0.88 Ah
    pad = np.r_[np.repeat(q[0], 2), q, np.repeat(q[-1], 2)]
    sm = np.median(np.lib.stride_tricks.sliding_window_view(pad, 5), axis=1)
    j = np.where((np.arange(q.size) >= 10) & (sm <= EOL * 1.01))[0]
    return int(j[0] + 1) if j.size else None

def X(n):
    x = np.asarray(n, float) / N_REF
    return np.column_stack([x ** Z1, x ** Z2])

def fit(history):                   # the twin: Q(n) = Q0 [1 - c1 (n/1000)^0.25 - c2 (n/1000)^2.8]
    n = np.arange(1, history.size + 1)
    pad = np.r_[np.repeat(history[0], 2), history, np.repeat(history[-1], 2)]
    q0 = float(np.median(np.lib.stride_tricks.sliding_window_view(pad, 5), axis=1).max())
    (c1, c2), _ = nnls(X(n[1:]), 1 - history[1:] / q0)
    return q0, c1, c2

def curve(p, n):
    q0, c1, c2 = p
    return q0 * (1 - np.clip(X(n) @ np.array([c1, c2]), 0, 1))

def twin(history, horizon):         # refit on everything seen so far, forecast `horizon` cycles ahead
    k = history.size
    return curve(fit(history), np.arange(k + 1, k + horizon + 1))

if __name__ == "__main__":
    z = np.load("matr_cells.npz")
    cells = []
    for i, cid in enumerate(z["ids"]):
        q = clean(z[f"{i}_qd"]); L = life(q)
        if L is None or q.size < 60 or 0.4 * L < 60: continue
        cells.append(dict(id=str(cid), batch=str(z["batches"][i]), q=q[:L], eol=L, ir=z[f"{i}_ir"][:L].astype(float)))
    train = [c for c in cells if c["batch"] != HOLDOUT]; test = [c for c in cells if c["batch"] == HOLDOUT]

    R, H = [], []
    for c in train:
        r, h = rolling_origin_residuals(twin, c["q"], step=10, min_train=100, max_horizon=HMAX)
        R.append(r); H.append(h)
    band = horizon_conformal(np.concatenate(R), np.concatenate(H), level=0.9, max_horizon=HMAX)
    hw = np.asarray(band.half_width)

    # coverage of the band on the held-out batch
    Y, Lo, Up = [], [], []
    for c in test:
        for k in range(100, c["q"].size, 10):
            h = min(HMAX, c["q"].size - k); f = twin(c["q"][:k], h)
            Y.append(c["q"][k:k + h]); Lo.append(f - hw[:h]); Up.append(f + hw[:h])
    cov = picp(np.concatenate(Y), np.concatenate(Lo), np.concatenate(Up))

    # the decision rule: order the replacement when the band's lower edge touches 0.88 Ah within LEAD cycles
    def first_warning(q):
        for k in range(100, q.size, 10):
            if (twin(q[:k], LEAD) - hw[:LEAD]).min() <= EOL: return k
        return None
    leads = []
    for c in test:
        k = first_warning(c["q"]); c["warn"] = k; leads.append(c["eol"] - k if k else -1)
    leads = np.array(leads)
    print(f"train {len(train)} cells, held-out {len(test)}; band coverage on held-out {cov:.3f}")
    print(f"warned before end of life on {(leads > 0).sum()}/{len(leads)}; median lead {np.median(leads):.0f} cycles, 10th pct {np.percentile(leads,10):.0f}")
    pick = min(test, key=lambda c: abs((c["eol"] - c["warn"]) - np.median(leads)) + abs(c["eol"] - 1000) / 1000)
    print("cell", pick["id"], "eol", pick["eol"], "warn", pick["warn"])
    json.dump(dict(hw=hw.tolist(), cov=float(cov), n_train=len(train), n_test=len(test),
                   warned=int((leads > 0).sum()), lead_med=float(np.median(leads)), lead_p10=float(np.percentile(leads, 10)),
                   cell=dict(id=pick["id"], eol=pick["eol"], warn=pick["warn"], q=pick["q"].tolist(), ir=pick["ir"].tolist())),
              open("battery.json", "w"))
