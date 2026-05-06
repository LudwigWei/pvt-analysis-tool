import math
import pandas as pd

# PVT Correlations based on Standing's method and related empirical formulas
def calc_rs(api, gg, t, p):
    x = 0.0125 * api - 0.00091 * (t - 460)
    val = gg * math.pow((p / 18.2 + 1.4) * math.pow(10, x), 1.205)
    return max(val, 0)

# Bo correlation based on Standing's method, adjusted for gas gravity and solution GOR
def calc_bo(api, gg, rs, t):
    go = api / (131.5 + api)
    f = rs * math.sqrt(gg / go) + 1.25 * (t - 460)
    return 0.9759 + 0.000120 * math.pow(f, 1.2)

# Oil viscosity correlation based on Standing's method, adjusted for solution GOR and temperature
def calc_muo(api, t, rs):
    x = math.pow(t - 460, -1.163) * math.exp(6.9824 - 0.04463 * api)
    dead = math.pow(10, x) - 1
    a = 10.715 * math.pow(rs + 100, -0.515)
    b = 5.44 * math.pow(rs + 150, -0.338)
    return max(a * math.pow(max(dead, 0.001), b), 0.01)

# Oil compressibility correlation based on Standing's method, adjusted for gas gravity, solution GOR, and pressure
def calc_co(api, gg, rs, t, p, bo):
    numerator = 5.615 * rs + 17.2 * (t - 460) - 1180 * gg + 12.61 * api - 1433
    return abs(numerator / (1e5 * p * bo))

# Pseudocritical properties based on gas gravity, used for Z-factor and gas compressibility calculations
def calc_pseudo(gg):
    tpc = 168 + 325 * gg - 12.5 * gg * gg
    ppc = 677 + 15 * gg - 37.5 * gg * gg
    return tpc, ppc

# Z-factor correlation based on Dranchuk and Abou-Kassem's method, adjusted for reduced pressure and temperature
def calc_z(ppr, tpr):
    val = 1 - (3.52 * ppr) / math.pow(10, 0.9813 * tpr) + (0.274 * ppr * ppr) / math.pow(10, 0.8157 * tpr)
    return max(val, 0.1)

# Gas formation volume factor correlation based on ideal gas law, adjusted for Z-factor and temperature
def calc_bg(t, p, z):
    return 0.00504 * z * t / p

# Gas viscosity correlation based on Lee, Gonzalez, and Eakin's method, adjusted for temperature, pressure, gas gravity, and Z-factor
def calc_mug(t, p, gg, z):
    mg = 28.97 * gg
    rho = (p * mg) / (z * 10.73 * t)
    k = ((9.4 + 0.02 * mg) * math.pow(t, 1.5)) / (209 + 19 * mg + t)
    x = 3.5 + 986 / t + 0.01 * mg
    y = 2.4 - 0.2 * x
    return max(1e-4 * k * math.exp(x * math.pow(max(rho / 62.4, 0.001), y)), 0.005)

# Fluid classification based on producing GOR, with descriptions for each category
def classify_fluid(api, gor):
    if gor > 100000:
        return {'name': 'Dry Gas', 'desc': 'Non-condensable gas reservoir. No liquid production at surface conditions.'}
    if gor > 50000:
        return {'name': 'Wet Gas', 'desc': 'Gas with minor surface condensate. API typically above 60°.'}
    if gor > 3300:
        return {'name': 'Gas Condensate / Retrograde Gas', 'desc': 'Rich gas system. Liquid retrograde condensation occurs as pressure drops below dew point.'}
    if gor > 2000:
        return {'name': 'Near-Critical / Volatile Oil', 'desc': 'High-shrinkage oil near the critical point. Properties are very sensitive to pressure changes.'}
    if api >= 40:
        return {'name': 'Black Oil — Light Crude', 'desc': 'Light crude oil. Low viscosity, high API gravity, good mobility.'}
    if api >= 25:
        return {'name': 'Black Oil — Medium Crude', 'desc': 'Medium gravity crude oil. Solution gas drive commonly dominant.'}
    
    return {'name': 'Heavy Oil', 'desc': 'Low API gravity, high viscosity crude. May require enhanced recovery methods.'}

# Main function to generate PVT table based on input parameters, using the defined correlations and classifications
def generate_pvt_table(api, gg, tf, pb, rs_pb, steps=10):
    t_rankine = tf + 460
    tpc, ppc = calc_pseudo(gg)
    tpr = t_rankine / tpc
    
    rows = []
    for i in range(steps + 1):
        # Pressure steps down from Pb to 100 psia
        p = max(pb * (1 - i / steps), 100)
        rs = min(calc_rs(api, gg, t_rankine, p), rs_pb)
        bo = calc_bo(api, gg, rs, t_rankine)
        muo = calc_muo(api, t_rankine, rs)
        co = calc_co(api, gg, rs, t_rankine, p, bo)
        z = calc_z(p / ppc, tpr)
        bg = calc_bg(t_rankine, p, z)
        mug = calc_mug(t_rankine, p, gg, z)
        
        rows.append({
            "P (psia)": round(p, 1),
            "Rs (scf/STB)": round(rs, 2),
            "Bo (RB/STB)": round(bo, 5),
            "muo (cp)": round(muo, 4),
            "co (psi-1)": format(co, '.3e'),
            "Z-factor": round(z, 4),
            "Bg (RB/Mscf)": round(bg, 5),
            "mug (cp)": round(mug, 5)
        })
        
    return pd.DataFrame(rows)