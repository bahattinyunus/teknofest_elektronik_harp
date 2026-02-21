import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from matplotlib.patches import RegularPolygon
import os

def create_premium_banner():
    # Setup canvas
    fig, ax = plt.subplots(figsize=(24, 6), dpi=100)
    fig.patch.set_facecolor('#050a14')
    ax.set_facecolor('#050a14')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # 1. Background Grid & Glow
    x = np.linspace(0, 24, 100)
    for i in x:
        ax.axvline(i, color='#00f2ff', alpha=0.03, linewidth=0.5)
    y = np.linspace(0, 6, 30)
    for i in y:
        ax.axhline(i, color='#00f2ff', alpha=0.03, linewidth=0.5)

    # Gradient Glow in center
    xx, yy = np.meshgrid(np.linspace(0, 24, 300), np.linspace(0, 6, 100))
    dist = np.sqrt((xx - 12)**2 + (yy - 3)**2)
    glow = np.exp(-dist/8)
    ax.imshow(glow, extent=[0, 24, 0, 6], aspect='auto', cmap='Blues', alpha=0.15, zorder=0)

    # 2. Digital Waveforms (Top and Bottom)
    t = np.linspace(0, 24, 1000)
    for i in range(5):
        alpha = 0.1 + (i * 0.05)
        lw = 0.5 + (i * 0.2)
        ax.plot(t, 5.5 + 0.2 * np.sin(t * (0.5 + i*0.1) + i), color='#00f2ff', alpha=alpha, linewidth=lw)
        ax.plot(t, 0.5 + 0.2 * np.cos(t * (0.5 + i*0.1) - i), color='#ff3c3c', alpha=alpha, linewidth=lw)

    # 3. Radar Scanning Effect (Polygons)
    cx, cy = 4, 3
    for r in [0.5, 1.0, 1.5]:
        circle = plt.Circle((cx, cy), r, color='#00f2ff', fill=False, alpha=0.2, linestyle='--')
        ax.add_artist(circle)
    ax.plot([cx, cx+1.4], [cy, cy+0.5], color='#00f2ff', alpha=0.6, linewidth=2)

    # 4. Main Title
    title = ax.text(12, 3.2, 'AEGIS - AI', 
                    fontsize=80, fontweight='bold', color='white',
                    ha='center', va='center', fontfamily='monospace',
                    zorder=10)
    title.set_path_effects([
        path_effects.withStroke(linewidth=8, foreground='#00f2ff', alpha=0.3),
        path_effects.Normal()
    ])

    subtitle = ax.text(12, 1.8, 'NEXT-GEN AUTONOMOUS ELECTRONIC WARFARE SYSTEM',
                       fontsize=16, fontweight='bold', color='#00f2ff',
                       ha='center', va='center', fontfamily='monospace',
                       alpha=0.8, zorder=11)
    
    # 5. Technical Data Accents
    for _ in range(20):
        rx, ry = np.random.uniform(18, 23), np.random.uniform(1, 5)
        ax.text(rx, ry, hex(np.random.randint(0, 0xFFFFF)), fontsize=8, color='#00f2ff', alpha=0.3, family='monospace')

    # 6. Border decoration
    ax.plot([0.5, 23.5, 23.5, 0.5, 0.5], [0.5, 0.5, 5.5, 5.5, 0.5], color='#00f2ff', alpha=0.2, linewidth=1)

    # Save to assets
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig('assets/banner_premium.png', bbox_inches='tight', pad_inches=0, facecolor='#050a14')
    plt.close()
    print("Premium banner saved to assets/banner_premium.png")

if __name__ == "__main__":
    create_premium_banner()
