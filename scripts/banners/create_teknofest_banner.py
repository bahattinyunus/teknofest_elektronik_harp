import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from matplotlib.patches import Polygon, Rectangle
import os

def create_teknofest_banner():
    # Setup canvas
    fig, ax = plt.subplots(figsize=(24, 7), dpi=100)
    fig.patch.set_facecolor('#040B16') # Very dark navy blue
    ax.set_facecolor('#040B16')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # 1. Background Grid & Glow (Cyber/Tech feel)
    x = np.linspace(0, 24, 120)
    for i in x:
        ax.axvline(i, color='#00f2ff', alpha=0.04, linewidth=0.5)
    y = np.linspace(0, 7, 35)
    for i in y:
        ax.axhline(i, color='#00f2ff', alpha=0.04, linewidth=0.5)

    # Deep Red and Blue ambient glows (Turkish flag colors + Tech colors)
    xx, yy = np.meshgrid(np.linspace(0, 24, 300), np.linspace(0, 7, 100))
    dist_center = np.sqrt((xx - 12)**2 + (yy - 3.5)**2)
    glow_blue = np.exp(-dist_center/10)
    ax.imshow(glow_blue, extent=[0, 24, 0, 7], aspect='auto', cmap='Blues', alpha=0.15, zorder=0)

    # 2. Dynamic Signal Waveforms
    t = np.linspace(0, 24, 2000)
    # LPI Radar FMCW representation (Chirp)
    chirp = 0.5 + 0.3 * np.cos(2 * np.pi * (0.5 * t + 0.1 * t**2))
    ax.plot(t, chirp, color='#00f2ff', alpha=0.2, linewidth=1)
    
    # Jamming representation (Noise/Barrage)
    noise = 6.0 + np.random.normal(0, 0.15, len(t))
    ax.plot(t, noise, color='#E30A17', alpha=0.4, linewidth=1) # E30A17 is a stark red

    # 3. Main TEKNOFEST 2026 Header
    title = ax.text(12, 4.5, 'TEKNOFEST 2026', 
                    fontsize=55, fontweight='900', color='white',
                    ha='center', va='center', fontfamily='sans-serif',
                    zorder=10)
    title.set_path_effects([
        path_effects.withStroke(linewidth=4, foreground='#E30A17', alpha=0.8),
        path_effects.Normal()
    ])

    subtitle1 = ax.text(12, 3.2, 'ELEKTRONİK HARP YARIŞMASI', 
                    fontsize=28, fontweight='bold', color='#00f2ff',
                    ha='center', va='center', fontfamily='monospace',
                    zorder=10)

    title2 = ax.text(12, 1.8, 'AEGIS - AI', 
                    fontsize=60, fontweight='bold', color='white',
                    ha='center', va='center', fontfamily='Orbitron',
                    zorder=10, style='italic')
    title2.set_path_effects([
        path_effects.withStroke(linewidth=6, foreground='#00f2ff', alpha=0.4),
        path_effects.Normal()
    ])

    sub_aegis = ax.text(12, 0.8, 'OTONOM SİNYAL İSTİHBARATI & TAARRUZ SİSTEMİ',
                       fontsize=16, fontweight='bold', color='#E30A17',
                       ha='center', va='center', fontfamily='monospace',
                       alpha=0.9, zorder=11)

    # 4. Tech Accents (Hex/Binary Data blocks on sides)
    for _ in range(15):
        rx, ry = np.random.uniform(0.5, 4), np.random.uniform(1, 6)
        ax.text(rx, ry, hex(np.random.randint(0, 0xFFFF)), fontsize=9, color='#00f2ff', alpha=0.4, family='monospace')
        
    for _ in range(15):
        rx, ry = np.random.uniform(20, 23.5), np.random.uniform(1, 6)
        ax.text(rx, ry, bin(np.random.randint(0, 255))[2:].zfill(8), fontsize=9, color='#E30A17', alpha=0.3, family='monospace')

    # 5. Corner Target Reticles
    for cx, cy in [(1.5, 5.5), (22.5, 5.5), (1.5, 1.5), (22.5, 1.5)]:
        ax.plot([cx-0.4, cx-0.1], [cy, cy], color='#00f2ff', lw=2, alpha=0.7)
        ax.plot([cx+0.1, cx+0.4], [cy, cy], color='#00f2ff', lw=2, alpha=0.7)
        ax.plot([cx, cx], [cy-0.4, cy-0.1], color='#00f2ff', lw=2, alpha=0.7)
        ax.plot([cx, cx], [cy+0.1, cy+0.4], color='#00f2ff', lw=2, alpha=0.7)
        circle = plt.Circle((cx, cy), 0.2, fill=False, color='#E30A17', lw=1, alpha=0.5)
        ax.add_artist(circle)

    # Frame/Border
    rect = Rectangle((0.2, 0.2), 23.6, 6.6, fill=False, edgecolor='#00f2ff', lw=1, alpha=0.3, linestyle='-.')
    ax.add_patch(rect)

    # Save to assets
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # Using banner_teknofest.png to replace the existing one linked in README
    output_path = 'assets/banner_teknofest_2026.png'
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, facecolor='#040B16')
    plt.close()
    print(f"TEKNOFEST banner saved to {output_path}")

if __name__ == "__main__":
    create_teknofest_banner()
