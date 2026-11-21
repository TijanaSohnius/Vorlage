import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#Auswertung einseitige Aufhängung
# Stab 1 (eckig)
x1_cm = np.array([5, 10, 15, 20, 25, 30, 35, 40], dtype=float)     # in cm
D1_mm = np.array([0.17, 0.5, 1.09, 1.79, 2.63, 3.60, 4.63, 5.81])  # in mm

# Stab 2 (rund)
x2_cm = np.array([5, 10, 15, 20, 25, 30, 35, 40], dtype=float)      # in cm
D2_mm = np.array([0.16, 0.46, 0.92, 1.51, 2.23, 3.08, 3.93, 4.86])  # in mm

L1 = 0.60  # m, Stab 1
L2 = 0.59  # m, Stab 2

dD = np.sqrt(2) * 0.005e-3  # m, Unsicherheit von D


def auswerten(x_cm, D_mm, L, name, farbe):
    x = x_cm * 1e-2  # m
    D = D_mm * 1e-3  # m
    z = L * x**2 - x**3 / 3  # m^3

    modell = lambda z, k: k * z
    popt, pcov = curve_fit(modell, z, D, sigma=np.full_like(D, dD),
                           absolute_sigma=True)
    k, dk = popt[0], np.sqrt(pcov[0, 0])
    print(f"{name}: k = {k:.6e} ± {dk:.2e} 1/m^2")

    zz = np.linspace(0, z.max() * 1.05, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(z * 1e3, D * 1e3, yerr=dD * 1e3, fmt="o", color=farbe,
                capsize=3, label="Messwerte")
    ax.plot(zz * 1e3, modell(zz, k) * 1e3, "k-",
            label=rf"Fit: $k = ({k:.3g} \pm {dk:.1g})\,\mathrm{{m^{{-2}}}}$")
    ax.set_xlabel(r"$z = Lx^2 - x^3/3 \;/\; 10^{-3}\,\mathrm{m^3}$")
    ax.set_ylabel(r"$D \,/\, \mathrm{mm}$")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"build/{name.replace(' ', '_')}.pdf")
    plt.close(fig)


auswerten(x1_cm, D1_mm, L1, "Stab 1", "tab:blue")
auswerten(x2_cm, D2_mm, L2, "Stab 2", "tab:red")

#Auswertung zweiseitige Aufhängung
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

dD = np.sqrt(2) * 0.005e-3   # m, Unsicherheit von D
modell = lambda z, k: k * z

# ---------------- Zweiseitige Auflage (Stab 1) ----------------
L3 = 0.55   # m, Abstand der Auflager (ANNAHME, bitte prüfen!)

# Messuhr 3 (links von der Last)
x3_cm = np.array([5, 10, 12.5, 15, 17.5, 20])
D3_mm = np.array([0.03, 0.08, 0.13, 0.17, 0.15, 0.22])

# Messuhr 4 (rechts von der Last)
x4_cm = np.array([50, 45, 42.5, 40, 37.5, 35])
D4_mm = np.array([0.09, 0.17, 0.22, 0.24, 0.36, 0.28])

# ---------------- Funktionen z(x) ----------------
def z_links(x, L):
    return 3 * L**2 * x - 4 * x**3                          # 0 <= x <= L/2

def z_rechts(x, L):
    return 4 * x**3 - 12 * L * x**2 + 9 * L**2 * x - L**3   # L/2 <= x <= L

# ---------------- Auswertung ----------------
def auswerten(x_cm, D_mm, L, zfunc, name, farbe, dateiname, xlabel):
    x = x_cm * 1e-2   # m
    D = D_mm * 1e-3   # m
    z = zfunc(x, L)   # m^3

    popt, pcov = curve_fit(modell, z, D, sigma=np.full_like(D, dD),
                           absolute_sigma=True)
    k, dk = popt[0], np.sqrt(pcov[0, 0])
    print(f"{name}: k = {k:.6e} ± {dk:.2e} 1/m^2")

    zz = np.linspace(0, z.max() * 1.05, 200)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(z * 1e3, D * 1e3, yerr=dD * 1e3, fmt="o", color=farbe,
                capsize=3, label="Messwerte")
    ax.plot(zz * 1e3, modell(zz, k) * 1e3, "k-",
            label=rf"Fit: $k = ({k:.3g} \pm {dk:.1g})\,\mathrm{{m^{{-2}}}}$")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"$D \,/\, \mathrm{mm}$")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"build/{dateiname}.pdf")
    plt.close(fig)
    return k, dk

xl_lin = r"$z = 3L^2x - 4x^3 \;/\; 10^{-3}\,\mathrm{m^3}$"
xl_re  = r"$z = 4x^3 - 12Lx^2 + 9L^2x - L^3 \;/\; 10^{-3}\,\mathrm{m^3}$"

k3, dk3 = auswerten(x3_cm, D3_mm, L3, z_links, "Messuhr 3 (links)",
                    "tab:blue", "zweiseitig_3", xl_lin)
k4, dk4 = auswerten(x4_cm, D4_mm, L3, z_rechts, "Messuhr 4 (rechts)",
                    "tab:red", "zweiseitig_4", xl_re)