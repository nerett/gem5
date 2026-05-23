import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

PLOT_FILE = Path(__file__).parent / "1_eas.png"

def get_voltage(f):
    # Umin = 1.0, f_min = 0.8
    return np.maximum(1.0, f + 0.2)

def power_e(perf):
    f = perf / 1.0 # IPC = 1
    u = get_voltage(f)
    return 1.0 * f * u**2 # Cdyn = 1

def power_p(perf):
    f = perf / 2.0 # IPC = 2
    u = get_voltage(f)
    return 4.0 * f * u**2 # Cdyn = 4

perf = np.linspace(0.5, 2.5, 500)
pow_e = power_e(perf)
pow_p = power_p(perf)
pow_opt = np.minimum(pow_e, pow_p)

plt.figure(figsize=(10, 6))
plt.plot(perf, pow_e, 'b--', linewidth=2, label='Efficient core')
plt.plot(perf, pow_p, 'r--', linewidth=2, label='Performance core')
plt.plot(perf, pow_opt, 'g-', linewidth=4, alpha=0.5, label='Optimal execution curve')

plt.title('Power vs performance for heterogeneous architecture', fontsize=14)
plt.xlabel('Performance (relative units)', fontsize=12)
plt.ylabel('Power (relative units)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.savefig(PLOT_FILE)
