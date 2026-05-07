"""
Lotka-Volterra Predator-Prey simulation using PySD.
Reads a Vensim .mdl file and runs the model with adjustable parameters.
"""

import pysd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

# ── Parameters (edit here or pass as CLI args) ──────────────────────────────
DEFAULTS = dict(
    alpha=0.8,    # prey birth rate
    beta=0.1,     # predation rate
    delta=0.07,   # predator conversion efficiency
    gamma=0.6,    # predator death rate
    x0=20.0,      # initial prey
    y0=5.0,       # initial predator
    final_time=40,
)

def run(params):
    model = pysd.read_vensim('lotka_volterra.mdl')

    result = model.run(
        params={
            'alpha':      params['alpha'],
            'beta':       params['beta'],
            'delta':      params['delta'],
            'gamma':      params['gamma'],
            'FINAL TIME': params['final_time'],
        },
        initial_condition=(
            0,
            {'Prey': params['x0'], 'Predator': params['y0']}
        ),
        return_columns=['Prey', 'Predator'],
    )

    return result

def plot(result, out='lotka_volterra.png'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    fig.patch.set_facecolor('#0d1117')
    for ax in (ax1, ax2):
        ax.set_facecolor('#161b22')
        ax.tick_params(colors='#8b949e', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#2a2a2a')

    # Time series
    ax1.plot(result.index, result['Prey'],     color='#b7e4c7', lw=1.5, label='Prey')
    ax1.plot(result.index, result['Predator'], color='#f4a261', lw=1.5, label='Predator')
    ax1.set_xlabel('Time (years)', color='#8b949e', fontsize=9)
    ax1.set_ylabel('Population',   color='#8b949e', fontsize=9)
    ax1.set_title('Population vs Time', color='#ddd', fontsize=10)
    ax1.legend(fontsize=8, facecolor='#1e1e1e', labelcolor='#ddd', edgecolor='#333')
    ax1.grid(True, color='#2a2a2a', linewidth=0.5)

    # Phase portrait
    ax2.plot(result['Prey'], result['Predator'], color='#7bc8a0', lw=1.2, alpha=0.8)
    ax2.plot(result['Prey'].iloc[0], result['Predator'].iloc[0],
             'o', color='#b7e4c7', ms=6, label='Start')
    ax2.set_xlabel('Prey',     color='#8b949e', fontsize=9)
    ax2.set_ylabel('Predator', color='#8b949e', fontsize=9)
    ax2.set_title('Phase Portrait', color='#ddd', fontsize=10)
    ax2.legend(fontsize=8, facecolor='#1e1e1e', labelcolor='#ddd', edgecolor='#333')
    ax2.grid(True, color='#2a2a2a', linewidth=0.5)

    fig.suptitle('Lotka–Volterra Predator–Prey', color='#e6edf3', fontsize=12, y=1.01)
    plt.tight_layout()
    plt.savefig(out, dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"Plot saved → {out}")

def main():
    parser = argparse.ArgumentParser(description='Lotka-Volterra via PySD')
    for k, v in DEFAULTS.items():
        parser.add_argument(f'--{k}', type=float, default=v,
                            help=f'{k} (default: {v})')
    parser.add_argument('--out', default='lotka_volterra.png')
    args = parser.parse_args()

    params = {k: getattr(args, k) for k in DEFAULTS}
    print("Running with parameters:")
    for k, v in params.items():
        print(f"  {k:12s} = {v}")

    result = run(params)
    print(f"\nSimulated {len(result)} time steps")
    print(f"  Prey     — final: {result['Prey'].iloc[-1]:.2f}  peak: {result['Prey'].max():.2f}")
    print(f"  Predator — final: {result['Predator'].iloc[-1]:.2f}  peak: {result['Predator'].max():.2f}")

    plot(result, args.out)

if __name__ == '__main__':
    main()