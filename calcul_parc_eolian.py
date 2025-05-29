import numpy as np

# CONSTANTE fizice
rho = 1.3  # densitatea aerului kg/m³
Cp = 0.593  # coeficient de putere maximă
eta_m = 0.98  # randament mecanic
eta_g = 0.99  # randament generator
t = 1  # timp de funcționare orară

def calculeaza_energie(viteze, suprafata_rotor, numar_turbine):
    """
    Calculează energia totală anuală pentru un parc eolian.
    """
    Pm = 0.5 * rho * suprafata_rotor * (viteze ** 3) * Cp
    Pe = Pm * eta_m * eta_g
    We = Pe * t
    We_parc = We * numar_turbine
    energie_totala_MWh = We_parc.sum() / 1000000  # conversie în MWh
    return energie_totala_MWh

