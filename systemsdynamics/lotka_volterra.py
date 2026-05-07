"""
Python model 'lotka_volterra.py'
Translated using PySD
"""

from pathlib import Path

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 40,
    "time_step": lambda: 0.05,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    return __data["time"].initial_time()


@component.add(
    name="TIME STEP", units="year", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Prey",
    units="animals",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_prey": 1},
    other_deps={
        "_integ_prey": {"initial": {}, "step": {"prey_births": 1, "predation": 1}}
    },
)
def prey():
    return _integ_prey()


_integ_prey = Integ(lambda: prey_births() - predation(), lambda: 20, "_integ_prey")


@component.add(
    name="Predator",
    units="animals",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_predator": 1},
    other_deps={
        "_integ_predator": {"initial": {}, "step": {"pred_births": 1, "pred_deaths": 1}}
    },
)
def predator():
    return _integ_predator()


_integ_predator = Integ(
    lambda: pred_births() - pred_deaths(), lambda: 5, "_integ_predator"
)


@component.add(
    name="alpha", units="1/year", comp_type="Constant", comp_subtype="Normal"
)
def alpha():
    """
    Prey birth rate
    """
    return 0.8


@component.add(
    name="beta", units="1/(year*animals)", comp_type="Constant", comp_subtype="Normal"
)
def beta():
    """
    Predation rate
    """
    return 0.1


@component.add(
    name="delta", units="dimensionless", comp_type="Constant", comp_subtype="Normal"
)
def delta():
    """
    Predator conversion efficiency
    """
    return 0.07


@component.add(
    name="gamma", units="1/year", comp_type="Constant", comp_subtype="Normal"
)
def gamma():
    """
    Predator death rate
    """
    return 0.6


@component.add(
    name="prey_births",
    units="animals/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alpha": 1, "prey": 1},
)
def prey_births():
    return alpha() * prey()


@component.add(
    name="predation",
    units="animals/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"beta": 1, "prey": 1, "predator": 1},
)
def predation():
    return beta() * prey() * predator()


@component.add(
    name="pred_births",
    units="animals/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"delta": 1, "beta": 1, "prey": 1, "predator": 1},
)
def pred_births():
    return delta() * beta() * prey() * predator()


@component.add(
    name="pred_deaths",
    units="animals/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gamma": 1, "predator": 1},
)
def pred_deaths():
    return gamma() * predator()
