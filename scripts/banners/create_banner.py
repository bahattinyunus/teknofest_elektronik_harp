"""
Banner generator for Aegis-AI project.
Generates a futuristic banner and saves it to assets/banner.png
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# --- Canvas Setup ---
fig, ax = plt.subplots(figsize=(16, 4.5))
fig.patch.set_facecolor('#020B18')
ax.set_facecolor('#020B18')
ax.set_xlim(0, 16)
ax.set_ylim(0, 4.5)
ax.axis('off')

# --- Background Gradient (subtle) ---
bg_grad = np.linspace(0, 1, 500).reshape(1, -1)
ax.imshow(bg_grad, extent=[0, 16, 0, 4.5], aspect='auto',
          cmap=LinearSegmentedColormap.from_list('bg', ['#020B18', '#061428', '#020B18']),
          alpha=0.8, zorder=0)

# --- Radar Waves ---
center_x, center_y = 2.5, 2.25
for i, r in enumerate(np.linspace(0.3, 2.8, 8)):
    alpha = max(0.05, 0.35 - i * 0.04)
    color = '#00F5FF' if i % 2 == 0 else '#7B2FBE'
    circle = plt.Circle((center_x, center_y), r, color=color,
                         fill=False, linewidth=0.8, alpha=alpha, zorder=1)
    ax.add_patch(circle)

# --- Radar Sweep Line ---
angle = np.radians(45)
sweep_x = [center_x, center_x + 2.8 * np.cos(angle)]
sweep_y = [center_y, center_y + 2.8 * np.sin(angle)]
ax.plot(sweep_x, sweep_y, color='#00F5FF', linewidth=1.5, alpha=0.6, zorder=2)

# --- Spectrum Graph (bottom strip) ---
x_spec = np.linspace(5.5, 15.5, 400)
noise = np.random.normal(0, 0.04, len(x_spec))
spectrum = 0.15 + noise
# add signal peaks
for peak_center, peak_height in [(7.5, 0.6), (9.2, 0.45), (11.8, 0.8), (13.5, 0.35), (14.8, 0.55)]:
    sigma = 0.15
    spectrum += peak_height * np.exp(-((x_spec - peak_center)**2) / (2*sigma**2))

spectrum = np.clip(spectrum, 0, None)
base_y = 0.4
ax.fill_between(x_spec, base_y, base_y + spectrum * 0.9,
                color='#00F5FF', alpha=0.15, zorder=1)
ax.plot(x_spec, base_y + spectrum * 0.9,
        color='#00F5FF', linewidth=0.8, alpha=0.7, zorder=2)

# --- HUD grid lines ---
for y_line in np.linspace(0.5, 4.0, 8):
    ax.axhline(y_line, color='#0D3B5E', linewidth=0.3, alpha=0.4, zorder=0)
for x_line in np.linspace(5.2, 16, 18):
    ax.axvline(x_line, color='#0D3B5E', linewidth=0.3, alpha=0.4, zorder=0)

# --- Main Title ---
ax.text(9.5, 2.9, 'AEGIS-AI',
        fontsize=64, fontweight='bold',
        color='white', ha='center', va='center',
        fontfamily='DejaVu Sans',
        zorder=5,
        alpha=0.95)

# Title glow effect (shadow layers)
for offset, alpha in [(0.06, 0.3), (0.03, 0.15)]:
    ax.text(9.5 + offset, 2.9 - offset, 'AEGIS-AI',
            fontsize=64, fontweight='bold',
            color='#00F5FF', ha='center', va='center',
            fontfamily='DejaVu Sans',
            zorder=4, alpha=alpha)

# --- Subtitle ---
ax.text(9.5, 2.0,
        'Otonom Sinyal İstihbaratı  ·  Elektronik Taarruz Paketi',
        fontsize=14, color='#8ECAE6',
        ha='center', va='center',
        fontfamily='DejaVu Sans',
        zorder=5, alpha=0.9)

# --- Tag line ---
ax.text(9.5, 1.3,
        'TEKNOFEST 2026  |  Electronic Warfare  |  AI-Driven Spectrum Dominance',
        fontsize=10, color='#4A90A4',
        ha='center', va='center',
        fontfamily='DejaVu Sans',
        zorder=5, alpha=0.8)

# --- Divider line ---
ax.plot([5.5, 13.5], [1.65, 1.65], color='#00F5FF', linewidth=0.5, alpha=0.4, zorder=3)

# --- Corner brackets (HUD feel) ---
bracket_color = '#00F5FF'
bracket_alpha = 0.5
bw = 0.5  # bracket width
for bx, by, dx, dy in [(0.2, 4.1, 1, -1), (15.8, 4.1, -1, -1),
                         (0.2, 0.4, 1, 1), (15.8, 0.4, -1, 1)]:
    ax.plot([bx, bx + dx * bw, bx + dx * bw], [by, by, by + dy * bw],
            color=bracket_color, linewidth=1.5, alpha=bracket_alpha, zorder=5)

# --- Save ---
plt.tight_layout(pad=0)
plt.savefig('assets/banner.png', dpi=150, bbox_inches='tight',
            facecolor='#020B18', edgecolor='none')
plt.close()
print("Banner successfully created at assets/banner.png")
