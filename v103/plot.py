import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ------------------------------------------------------------
# Messwerte (PLATZHALTER, durch eigene Werte ersetzen)
# ------------------------------------------------------------
# Stab 1 (eckig)
x1_cm = np.array([5, 10, 15, 20, 25, 30, 35, 40], dtype=float)        # cm
D1_mm = np.array([0.17, 0.5, 1.09, 1.79, 2.63, 3.60, 4.63, 5.81])  # mm

# Stab 2 (rund)
x2_cm = np.array([5, 10, 15, 20, 25, 30, 35, 40], dtype=float)        # cm
D2_mm = np.array([0.16, 0.46, 0.92, 1.51, 2.23, 3.08, 3.93, 4.86])  # mm

L1 = 0.60  # m, Stablänge Stab 1
L2 = 0.59  # m, Stablänge Stab 2

dD = np.sqrt(2) * 0.005e-3  # m, Unsicherheit von D (zwei Ablesungen)


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