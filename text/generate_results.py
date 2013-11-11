#!/usr/bin/env python

import os
import re
import sys

def findModel(*frags):
    rfrags = map(lambda x: re.compile(x), frags)
    res = []
    root = os.path.join(path, "ModelicaByExample")
    for ent in os.walk(root):
        for f in ent[2]:
            if f=="package.mo":
                continue
            match = True
            full = os.path.join(ent[0], f)
            rel = full[(len(root)+1):]
            modname = rel[:-3].replace("/",".")
            for rfrag in rfrags:
                if len(rfrag.findall(modname))==0:
                    match = False
            if match:
                res.append((full, rel, modname))
    if len(res)==1:
        return res[0]
    else:
        print "Unable to find a unique match for "+str(frags)+" matches include:"
        for r in res:
            print str(r)
        sys.exit(1)

def add_case(*frags, **kwargs):
    mod = findModel(*frags)
    data = kwargs.copy()
    data["name"] = mod[2]
    if not "short" in data:
        print "Error, not short hand name associated with pattern: "+str(frags)
        sys.exit(1)
    short = data["short"]
    if short in shorts:
        print "Error, multiple cases using the same short hand name "+short
        sys.exit(1)
    shorts.add(short)
    models.append(data)

models = []
shorts = set()
path = os.path.abspath("..");
results = default=os.path.abspath("./results")

# This is the list of things I need to simulate

## Simple Examples
add_case("SimpleExample", "FirstOrder$", stopTime=10,
         short="FO", vars=["x"]);
add_case("SimpleExample", "FirstOrderInitial", stopTime=10,
         short="FOI", vars=["x"]);
add_case("SimpleExample", "FirstOrderSteady", stopTime=10,
         short="FOS", vars=["x"]);

## Cooling Example
add_case("NewtonCoolingWithDefaults", stopTime=10,
         short="NC1", vars=["T"])

## RLC
add_case("RLC1", stopTime=10, short="RLC1")

## RotationalSMD
add_case("SecondOrderSystemInitParams", stopTime=1, short="SOSIP")
add_case("SecondOrderSystemInitParams", stopTime=1, short="SOSIP1", mods={"phi1": 1.0})

## LotkaVolterra
add_case("ClassicModel$", stopTime=1, short="LVCM")
add_case("QuiescientModel$", stopTime=1, short="LVQM")
add_case("QuiescientModelUsingStart", stopTime=1, short="LVQMUS")

def genPlotScripts():
    simplePlot = """
# Autogenerated script to plot results for model
# %s
from xogeny.plot_utils import render_simple_plot
render_simple_plot("%s", %s)
""";
    for model in models:
        dotname = model["name"]
        short = model["short"]
        dashname = dotname.replace(".", "_")
        with open(os.path.join("plots", short+".py"), "w+") as fp:
            if "vars" in model:
                fp.write(simplePlot % (dotname, dashname, repr(model["vars"])))
                fp.close()
                

def genSimScript():
    preamble = """
    loadModel(ModelicaServices);
    loadModel(Modelica);
    setModelicaPath(getModelicaPath()+":"+"%s");
    loadModel(ModelicaByExample);
    """ % (path,)

    cmd = preamble

    for model in models:
        dotname = model["name"]
        stop_time = model["stopTime"]
        dashname = dotname.replace(".", "_")
        mods = model.get("mods", {})
        modstr = ",".join(map(lambda x: x+"="+str(mods[x]), mods))

        if stop_time==None:
            cmd = cmd+"""
    simulate(ModelicaByExample.%s, tolerance=1e-3, numberOfIntervals=500, fileNamePrefix="%s");
    """ % (dotname, dashname)
        else:
            cmd = cmd+"""
    simulate(ModelicaByExample.%s, stopTime=%s, tolerance=1e-3, numberOfIntervals=500, fileNamePrefix="%s");
    """ % (dotname, stop_time, dashname)

    with open("simulateAll.mos", "w+") as fp:
        fp.write(cmd)

genSimScript()
genPlotScripts()
