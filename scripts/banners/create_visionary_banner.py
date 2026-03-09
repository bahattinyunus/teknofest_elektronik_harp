"""
Visionary Banner Generator for Aegis-AI.
Creates a high-end, premium aesthetic banner using advanced matplotlib techniques.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from matplotlib.patches import Polygon
import warnings
warnings.filterwarnings('ignore')

def create_visionary_banner():
    # Canvas setup
    fig, ax = plt.subplots(figsize=(20, 5.5), dpi=150)
    fig.patch.set_facecolor('#010409')
    ax.set_facecolor('#010409')
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # 1. Background Pulse (Circular Gradient)
    x = np.linspace(0, 20, 400)
    y = np.linspace(0, 5.5, 110)
    X, Y = np.meshgrid(x, y)
    
    # Distance from three "hubs"
    d1 = np.sqrt((X - 2)**2 + (Y - 2.75)**2)
    d2 = np.sqrt((X - 10)**2 + (Y - 2.75)**2)
    d3 = np.sqrt((X - 18)**2 + (Y - 2.75)**2)
    
    pulse = np.exp(-d1/3) * 0.2 + np.exp(-d2/5) * 0.15 + np.exp(-d3/3) * 0.2
    
    cmap_bg = LinearSegmentedColormap.from_list('vision', ['#010409', '#020C1F', '#0D1117'])
    ax.imshow(pulse, extent=[0, 20, 0, 5.5], aspect='auto', cmap=cmap_bg, alpha=0.9, zorder=0)

    # 2. Particle Field (Stars/Data points)
    n_points = 600
    px = np.random.uniform(0, 20, n_points)
    py = np.random.uniform(0, 5.5, n_points)
    psizes = np.random.uniform(0.1, 1.2, n_points)
    palphas = np.random.uniform(0.1, 0.4, n_points)
    ax.scatter(px, py, s=psizes, c='#89D1FF', alpha=palphas, edgecolors='none', zorder=1)

    # 3. Frequency Rhythms (Sine waves with variable phase and frequency)
    t = np.linspace(0, 20, 1000)
    for i in range(12):
        freq = 0.5 + i * 0.15
        phase = i * 0.5
        y_off = 2.75 + np.sin(t * 0.2 + phase) * 0.5
        amplitude = 0.1 + (i % 3) * 0.1
        alpha = 0.05 + (i / 30)
        color = '#00F5FF' if i % 2 == 0 else '#B026FF'
        
        ax.plot(t, y_off + amplitude * np.sin(t * freq + phase), 
                color=color, linewidth=0.6, alpha=alpha, zorder=2)

    # 4. Central HUD Hexagon (Geometric Vision)
    cx, cy = 10, 2.75
    r = 2.0
    theta = np.linspace(0, 2*np.pi, 7)
    hx = cx + r * np.cos(theta)
    hy = cy + r * np.sin(theta)
    ax.plot(hx, hy, color='#00F5FF', linewidth=1.2, alpha=0.3, zorder=3)
    
    # Inner hexagon
    r_in = 1.8
    hx_in = cx + r_in * np.cos(theta)
    hy_in = cy + r_in * np.sin(theta)
    ax.plot(hx_in, hy_in, color='#B026FF', linewidth=0.8, alpha=0.2, zorder=3)

    # 5. Main Title with Advanced Path Effects (Glow)
    title_text = ax.text(cx, cy + 0.1, 'AEGIS - AI', 
                         fontsize=68, fontweight='bold', color='white',
                         ha='center', va='center', fontfamily='sans-serif',
                         zorder=10)
    
    title_text.set_path_effects([
        path_effects.withStroke(linewidth=4, foreground='#00F5FF', alpha=0.2),
        path_effects.Normal()
    ])

    # 6. Visionary Slogan
    ax.text(cx, cy - 1.1, 'BEYOND THE SPECTRUM: AUTONOMOUS ELECTRONIC SUPREMACY', 
            fontsize=13, fontweight='medium', color='#70D7FF',
            ha='center', va='center', fontfamily='sans-serif',
            alpha=0.8, zorder=11)

    # 7. Data Flow Lines (Diagonal)
    for _ in range(15):
        lx = np.random.uniform(0, 20)
        ly = np.random.uniform(0, 5.5)
        length = np.random.uniform(1, 3)
        ax.plot([lx, lx + length], [ly, ly + length * 0.3], 
                color='#00F5FF', linewidth=0.4, alpha=0.1, zorder=1)

    # 8. HUD Corner Accents
    # Top Left
    ax.plot([0.5, 1.5], [5.0, 5.0], color='#00F5FF', linewidth=1.5, alpha=0.6)
    ax.plot([0.5, 0.5], [5.0, 4.0], color='#00F5FF', linewidth=1.5, alpha=0.6)
    # Bottom Right
    ax.plot([18.5, 19.5], [0.5, 0.5], color='#B026FF', linewidth=1.5, alpha=0.6)
    ax.plot([19.5, 19.5], [0.5, 1.5], color='#B026FF', linewidth=1.5, alpha=0.6)

    # Final adjustments and save
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig('assets/banner_visionary.png', dpi=200, bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close()
    print("Visionary banner created: assets/banner_visionary.png")

if __name__ == "__main__":
    create_visionary_banner()
