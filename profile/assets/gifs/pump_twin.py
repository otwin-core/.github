"""Pump and filter-press twin: the plant is simulated with otwin, the sensor gets 2 % noise,
and otwin.fit_parameters recovers the cloth fouling from the pressure drop alone."""
# ---- part 1: simulate the line month by month (writes frame.json)
import json, warnings, otwin, numpy as np
warnings.filterwarnings("ignore")
from otwin.components.hydraulic import Atmosphere, Filter, Pipe, Pump, Tank
pump=Pump(shutoff=4.0e5,max_flow=0.08,name="pump")
model=otwin.compile(Tank(area=5000.0,level=3.0,name="tank")>>Pipe(resistance=5e5,name="suction")>>pump>>Filter(resistance=2.0e6,name="filter")>>Atmosphere(name="outfall"),dt=1.0)
def at(s,f): return model.with_parameters({"pump.head.pressure":s*s*pump.shutoff,"filter.fouling":f})
def op(m,n=600):
    st=m.initial_state()
    for _ in range(n): st=m.step(st)
    return m.outputs(st)
clean=op(at(0.75,0.0)); Q0=clean["pump.flow"]; P0=clean["pump.hydraulic_power"]
def solve(f):
    lo,hi=0.75,1.0
    if op(at(1.0,f))["pump.flow"]<Q0: return 1.0, op(at(1.0,f))
    for _ in range(14):
        s=(lo+hi)/2
        if op(at(s,f))["pump.flow"]<Q0: lo=s
        else: hi=s
    return hi, op(at(hi,f))
keys=[k for k in clean if "filter" in k or "pump" in k]
out={"Q0":Q0*3600,"P0":P0/1e3,"outputs":keys}
for g in (1.12,1.15,1.18):
    rows=[];spent=0.0;step=0.5;m=0.0
    while m<=12.0001:
        f=g**m-1; s,o=solve(f); kw=o["pump.hydraulic_power"]
        if m>0: spent+=(kw-P0)*24*30*step/1e6*120
        rows.append(dict(month=m,fouling=f,speed=s,kw=kw/1e3,eur=spent,flow=o["pump.flow"]*3600,
                         rise=o["pump.pressure_rise"]/1e5,
                         dpf={k:v for k,v in o.items() if k.startswith("filter")}))
        m+=step
    out[str(g)]=rows
json.dump(out,open("frame.json","w"),default=float)
print(keys)
print([ (r["month"],round(r["speed"],3),round(r["eur"])) for r in out["1.15"][::2]])
print(out["1.15"][12]["dpf"])

# ---- part 2: estimate the fouling from the noisy pressure-drop sensor (writes fit.json)
C=out["1.15"]
def interp(m):
    i=max(0,min(len(C)-2,int(m/0.5))); a,b=C[i],C[i+1]; t=(m-a["month"])/0.5
    return a["speed"]+t*(b["speed"]-a["speed"]), (1.15**m-1)
rng=np.random.default_rng(11); t=np.arange(0,240.0,1.0); out=[]
for m in np.arange(0,8.0001,0.25):
    s,f=interp(m)
    truth=model.with_parameters({"pump.head.pressure":s*s*4e5,"filter.fouling":f})
    st=truth.initial_state(); dp=[]
    for _ in t: st=truth.step(st); dp.append(truth.outputs(st)["filter.pressure_drop"])
    dp=np.array(dp)*(1+rng.normal(0,0.02,len(t)))           # the sensor: 2 % noise
    guess=model.with_parameters({"pump.head.pressure":s*s*4e5,"filter.fouling":0.3})
    r=otwin.fit_parameters(guess,t,{"filter.pressure_drop":dp},["filter.fouling"],bounds={"filter.fouling":(0,10)})
    est=float(r.model.parameters["filter.fouling"])
    out.append(dict(month=float(m),true=f,est=est)); print(round(m,2),round(f,3),round(est,3),flush=True)
json.dump(out,open("fit.json","w"))
