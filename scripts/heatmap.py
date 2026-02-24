import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy.ndimage import gaussian_filter

def generate_heatmap(coordinates, field_length, field_width, output_path='heatmap.png'):
    x_coord = coordinates['x'].values
    y_coord = coordinates['y'].values

    # creating mpl figure along with axis
    fig, axi = plt.subplots(figsize=(10,7))

    # creating heatmap data as numpy histogram from coordinates of size via field dimensions
    heatmap, _, _ = np.histogram2d(
        x_coord, y_coord,
        bins=[100,100],
        range=[[0, field_length], [0, field_width]]
    )

    # gaussian filter for smoothing image of heatmap
    heatmap = gaussian_filter(heatmap, sigma=5)

    # displaying heatmap image
    display = axi.imshow(
        heatmap.T,
        origin='lower',
        extent=[0, field_length, 0, field_width],
        cmap='YlOrRd',
        alpha=0.4,
        aspect='auto'
    )

    # halfway line
    axi.plot(
        (field_length / 2, field_length / 2), (0, field_width),
        'white', linewidth=2
    )

    # center circle
    circle = patches.Ellipse(
        (field_length / 2, field_width / 2),
        field_length * 0.16,
        field_width  * 0.14,
        fill=False, edgecolor='white', linewidth=2
    )

    # 18 yard relative dimensions for scaling
    box_len = field_length * 0.20
    box_wid = field_width * 0.20
    box_y = (field_width - box_wid) / 2

    # plotting boxes
    left_18box  = patches.Rectangle(
        (0, box_y),
        box_len, box_wid,
        fill=False, edgecolor='white', linewidth=2
    )
    right_18box = patches.Rectangle(
        (field_length - box_len, box_y),
        box_len, box_wid,
        fill=False, edgecolor='white', linewidth=2
    )

    # create patches
    axi.add_patch(circle)
    axi.add_patch(left_18box)
    axi.add_patch(right_18box)

    # finalize graph
    plt.colorbar(display, ax=axi, label='Player Position Frequency')
    axi.set_title('SoccerSense Heatmap', fontsize=16, fontweight='bold')
    axi.set_xlabel('Length (meters)', fontsize=12)
    axi.set_ylabel('Width (meters)', fontsize=12)
    axi.set_xlim(0, field_length)
    axi.set_ylim(0, field_width)
    axi.set_facecolor("#004813")

    print('Generating Heatmap.')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)