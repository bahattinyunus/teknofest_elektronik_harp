import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from matplotlib.patches import Polygon, Rectangle
import warnings
import os

warnings.filterwarnings('ignore')

def create_ultimate_teknofest_banner():
    # Canvas setup
    fig, ax = plt.subplots(figsize=(24, 7), dpi=150)
    
    # Dark modern background
    bg_color = '#020611' # Very dark blue/black
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # 1. Background Pulse (Circular Gradient)
    x = np.linspace(0, 24, 400)
    y = np.linspace(0, 7, 150)
    X, Y = np.meshgrid(x, y)
    
    # Distance from center
    d_center = np.sqrt((X - 12)**2 + (Y - 3.5)**2)
    # Distance from sides
    d_left = np.sqrt((X - 3)**2 + (Y - 3.5)**2)
    d_right = np.sqrt((X - 21)**2 + (Y - 3.5)**2)
    
    pulse = np.exp(-d_center/6) * 0.25 + np.exp(-d_left/5) * 0.15 + np.exp(-d_right/5) * 0.15
    
    # Deep red and cyan mix
    cmap_bg = LinearSegmentedColormap.from_list('tekno', ['#020611', '#0a1930', '#1a0505'])
    ax.imshow(pulse, extent=[0, 24, 0, 7], aspect='auto', cmap=cmap_bg, alpha=0.9, zorder=0)

    # 2. Tech Grid
    x_grid = np.linspace(0, 24, 120)
    for i in x_grid:
        ax.axvline(i, color='#00f2ff', alpha=0.03, linewidth=0.5)
    y_grid = np.linspace(0, 7, 35)
    for i in y_grid:
        ax.axhline(i, color='#00f2ff', alpha=0.03, linewidth=0.5)

    # 3. Dynamic Signal Waveforms (Red and Cyan)
    t = np.linspace(0, 24, 2000)
    for i in range(8):
        freq = 0.5 + i * 0.1
        phase = i * 0.5
        y_off = 3.5 + np.sin(t * 0.1 + phase) * 0.8
        amplitude = 0.2 + (i % 3) * 0.15
        alpha = 0.1 + (i / 20)
        
        # Alternate between Cyan (#00f2ff) and Turkish Red (#E30A17)
        color = '#00f2ff' if i % 2 == 0 else '#E30A17'
        
        ax.plot(t, y_off + amplitude * np.sin(t * freq + phase), 
                color=color, linewidth=1.0, alpha=alpha, zorder=2)

    # 4. Digital Noise / Jamming effect
    noise_idx = np.random.choice(len(t), 300, replace=False)
    ax.scatter(t[noise_idx], 3.5 + np.random.normal(0, 1.5, 300), 
               s=np.random.uniform(1, 5, 300), color='#E30A17', alpha=0.4, zorder=3)
    ax.scatter(t[noise_idx], 3.5 + np.random.normal(0, 1.5, 300), 
               s=np.random.uniform(1, 5, 300), color='#00f2ff', alpha=0.4, zorder=3)

    # 5. Radar / Target Reticles
    for cx, cy in [(3, 3.5), (21, 3.5)]:
        for r in [1, 1.5, 2]:
            circle = plt.Circle((cx, cy), r, color='#00f2ff', fill=False, alpha=0.15, linestyle='--', lw=1.5)
            ax.add_artist(circle)
        # Crosshairs
        ax.plot([cx-2.5, cx+2.5], [cy, cy], color='#00f2ff', lw=1, alpha=0.3)
        ax.plot([cx, cx], [cy-2.5, cy+2.5], color='#00f2ff', lw=1, alpha=0.3)

    # 6. Main Typography
    # TEKNOFEST Title
    title_tf = ax.text(12, 5.2, 'TEKNOFEST 2026', 
                     fontsize=50, fontweight='900', color='white',
                     ha='center', va='center', fontfamily='sans-serif',
                     zorder=10)
    title_tf.set_path_effects([
        path_effects.withStroke(linewidth=5, foreground='#E30A17', alpha=0.7),
        path_effects.Normal()
    ])

    # Category Subtitle
    sub_category = ax.text(12, 4.3, 'ELEKTRONİK HARP YARIŞMASI', 
                        fontsize=22, fontweight='bold', color='#00f2ff',
                        ha='center', va='center', fontfamily='monospace',
                        zorder=10)

    # Project Name
    title_aegis = ax.text(12, 2.8, 'MERGEN - AI', 
                         fontsize=80, fontweight='bold', color='white',
                         ha='center', va='center', fontfamily='monospace',
                         style='italic', zorder=10)
    title_aegis.set_path_effects([
        path_effects.withStroke(linewidth=8, foreground='#00f2ff', alpha=0.5),
        path_effects.withStroke(linewidth=15, foreground='#00f2ff', alpha=0.1),
        path_effects.Normal()
    ])

    # Slogan
    slogan = ax.text(12, 1.5, 'OTONOM SİNYAL İSTİHBARATI & ELEKTRONİK TAARRUZ SİSTEMİ', 
                    fontsize=16, fontweight='bold', color='#E30A17',
                    ha='center', va='center', fontfamily='sans-serif',
                    alpha=0.9, zorder=11)

    # Data Streams (Hex/Bin on sides)
    for _ in range(25):
        rx, ry = np.random.uniform(0.5, 4.5), np.random.uniform(1, 6)
        ax.text(rx, ry, hex(np.random.randint(0, 0xFFFFF)).upper(), fontsize=10, color='#00f2ff', alpha=0.3, family='monospace', rotation=90)
        
    for _ in range(25):
        rx, ry = np.random.uniform(19.5, 23.5), np.random.uniform(1, 6)
        ax.text(rx, ry, bin(np.random.randint(0, 255))[2:].zfill(8), fontsize=10, color='#E30A17', alpha=0.2, family='monospace', rotation=270)

    # Frame Corners
    c_len = 1.5
    lw_c = 3
    # TL
    ax.plot([0.5, 0.5+c_len], [6.5, 6.5], color='#00f2ff', lw=lw_c, alpha=0.8)
    ax.plot([0.5, 0.5], [6.5, 6.5-c_len], color='#00f2ff', lw=lw_c, alpha=0.8)
    # TR
    ax.plot([23.5, 23.5-c_len], [6.5, 6.5], color='#E30A17', lw=lw_c, alpha=0.8)
    ax.plot([23.5, 23.5], [6.5, 6.5-c_len], color='#E30A17', lw=lw_c, alpha=0.8)
    # BL
    ax.plot([0.5, 0.5+c_len], [0.5, 0.5], color='#E30A17', lw=lw_c, alpha=0.8)
    ax.plot([0.5, 0.5], [0.5, 0.5+c_len], color='#E30A17', lw=lw_c, alpha=0.8)
    # BR
    ax.plot([23.5, 23.5-c_len], [0.5, 0.5], color='#00f2ff', lw=lw_c, alpha=0.8)
    ax.plot([23.5, 23.5], [0.5, 0.5+c_len], color='#00f2ff', lw=lw_c, alpha=0.8)

    # Save to assets
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    output_path = 'assets/banner_teknofest_ultimate.png'
    plt.savefig(output_path, dpi=200, bbox_inches='tight', pad_inches=0, facecolor=bg_color)
    plt.close()
    print(f"Ultimate TEKNOFEST banner saved to {output_path}")

if __name__ == "__main__":
    create_ultimate_teknofest_banner()
