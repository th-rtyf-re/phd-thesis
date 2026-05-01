# -*-coding:utf8-*-

import gudhi as gd
import itertools as it
import miniball

import numpy as np
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.collections as mc
from matplotlib.widgets import Slider

import shapely

import bisect

from matplotlib import font_manager

font_path = "/Users/rtyf/Library/Fonts/Figtree-Regular.ttf" # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

font_path = "/Users/rtyf/Library/Fonts/XCharter-Math.otf" # Your font path goes here
# font_path = "/usr/local/texlive/2025/texmf-dist/fonts/opentype/public/xcharter-math/XCharter-Math.otf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = "Figtree"
plt.rcParams['font.serif'] = "XCharter Math"
plt.rcParams['mathtext.fontset'] = "custom"
plt.rcParams['mathtext.it'] = "serif"
plt.rcParams['mathtext.rm'] = "serif"

"""
list of tuples (name, right ascension, declination, visible magnitude).
"""
data = [
    ("alpha",   (10,  8, 22.46), (11, 58,  1.9), 1.36),
    ("beta",    (11, 49,  3.88), (14, 34, 20.4), 2.14),
    ("gamma",   (10, 19, 58.16), (19, 50, 30.7), 2.37),
    ("delta",   (11, 14,  6.41), (20, 31, 26.5), 2.56),
    ("epsilon", (9,  45, 51.10), (23, 46, 27.4), 2.97),
    ("theta",   (11, 14, 14.44), (15, 25, 47.1), 3.33),
    ("zeta",    (10, 16, 41.40), (23, 25,  2.4), 3.33),
    ("eta",     (10,  7, 19.95), (16, 45, 45.6), 3.43),
    ("omicron", (9,  41,  9.12), ( 9, 53, 32.6), 3.52),
    ("rho",     (10, 32, 48.68), ( 9, 18, 23.7), 3.84),
    ("mu",      (9,  52, 45.96), (26,  0, 25.5), 3.88),
    ("iota",    (11, 23, 55.37), (10, 31, 46.9), 4.00),
    ("sigma",   (11, 21,  8.25), ( 6,  1, 45.7), 4.05),
    ("54",      (10, 55, 36.85), (24, 44, 59.1), 4.30),
    ("lambda",  (9,  31, 43.24), (22, 58,  5.0), 4.32),
    ("kappa",   (9,  24, 39.28), (26, 10, 56.8), 4.47),
    ("chi",     (11,  5,  1.23), ( 7, 20, 10.0), 4.63)
]
normalized_coords = []
for _, ra, dec, _ in data:
    h, m, s = ra
    ra_seconds = 3600 * h + 60 * m + s
    h, m, s = dec
    dec_seconds = 3600 * h + 60 * m + s
    normalized_coords.append((-ra_seconds / 3600 * 15, dec_seconds / 3600))

n_stars = len(data)
coords = np.array(normalized_coords, dtype=float) * 2  # manual scaling factor
dist = squareform(pdist(coords))

magnitude = (8. - np.array([d[3] for d in data], dtype=float)) / 4.

triangles = np.zeros((n_stars, n_stars, n_stars), dtype=float)
for s0 in range(n_stars):
    for s1 in range(s0 + 1, n_stars):
        for s2 in range(s1 + 1, n_stars):
            # Vietoris-Rips
            # triangles[s0, s1, s2] = max(dist[s0, s1], dist[s0, s2], dist[s1, s2])
            # Čech
            # check if obtuse
            a, b, c = sorted((dist[s0, s1], dist[s0, s2], dist[s1, s2]))
            if c * c > a * a + b * b:  # obtuse: half of biggest side
                triangles[s0, s1, s2] = c / 2
            else: # acute: compute circumradius
                x0, y0 = coords[s0]
                x1, y1 = coords[s1]
                x2, y2 = coords[s2]
                area = np.abs((x0 - x2) * (y1 - y0) - (x0 - x1) * (y2 - y0)) / 2  # from Wikipedia
                triangles[s0, s1, s2] = dist[s0, s1] * dist[s1, s2] * dist[s0, s2] / (4 * area)

def visualize():
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.set_title("The Leo constellation")
    ax.set_xlabel("right ascension (relative)")
    ax.set_ylabel("declination (relative)")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

    # Add vertices (stars)
    circles = []
    for s0 in range(n_stars):
        circles.append(pat.Circle(coords[s0], magnitude[s0]))
    circlecoll = mc.PatchCollection(circles, facecolor="k", edgecolor="w", zorder=3)
    ax.add_collection(circlecoll)

    # Create collections of edges and faces (lines and triangles)
    lines = []
    tris = []
    line_dist = pdist(coords) / 2
    tri_dist = []
    for s0 in range(n_stars):
        for s1 in range(s0 + 1, n_stars):
            lines.append([coords[s0], coords[s1]])
            for s2 in range(s1 + 1, n_stars):
                tris.append([coords[s0], coords[s1], coords[s2]])
                tri_dist.append(triangles[s0, s1, s2])
    
    line_dist, lines = zip(*sorted(zip(line_dist, lines), key = lambda t: t[0]))
    # print(tri_dist, tris)
    tri_dist, tris = zip(*sorted(zip(tri_dist, tris), key = lambda t: t[0]))
    
    linecoll = mc.LineCollection(list(lines), linewidths=2, capstyle="round")
    tricoll = mc.PolyCollection(list(tris))
    ax.add_collection(linecoll)
    ax.add_collection(tricoll)
    ax.axis('equal')
    
    # Create the slider
    initial_threshold = 10.
    plt.subplots_adjust(bottom=0.25)
    ax_slider = plt.axes([0.2, 0.02, 0.62, 0.05]) # Slider position
    slider = Slider(ax_slider, 'radius', 0., 30., valinit=initial_threshold, color="#ffbe00", initcolor="none")

    # Update function for slider
    linecolors = np.zeros((len(line_dist), 4), dtype=float)
    tricolors = np.zeros((len(tri_dist), 4), dtype=float)
    tricolors[:] = .7
    
    # New guy
    sublevelset = shapely.MultiPoint(coords)
    sls_buffer = sublevelset.buffer(initial_threshold)
    verts = []
    if hasattr(sls_buffer, "geoms"):
        for geom in sls_buffer.geoms:
            verts.append(np.array(geom.exterior.xy).T)
            verts += [np.array(int_geom.xy).T for int_geom in geom.interiors]
    else:
        verts.append(np.array(sls_buffer.exterior.xy).T)
        verts += [np.array(int_geom.xy).T for int_geom in sls_buffer.interiors]
    levelset_coll = mc.PolyCollection(verts, linestyles="dotted", facecolors="none", zorder=0)
    ax.add_collection(levelset_coll)
    
    def update(threshold):
        i = bisect.bisect(line_dist, threshold)
        linecolors[:i, 3] = 1.
        linecolors[i:, 3] = 0.
        linecoll.set_color(linecolors)
        linecoll.set_linewidth((30 - threshold) / 15)
        
        i = bisect.bisect(tri_dist, threshold)
        tricolors[:i, 3] = 1.
        tricolors[i:, 3] = 0.
        tricoll.set_color(tricolors)
        
        sls_buffer = sublevelset.buffer(threshold)
        verts = []
        if hasattr(sls_buffer, "geoms"):
            for geom in sls_buffer.geoms:
                verts.append(np.array(geom.exterior.xy).T)
                verts += [np.array(int_geom.xy).T for int_geom in geom.interiors]
        else:
            verts.append(np.array(sls_buffer.exterior.xy).T)
            verts += [np.array(int_geom.xy).T for int_geom in sls_buffer.interiors]
        levelset_coll.set_verts(verts)
    slider.on_changed(update)
    
    # Visualize!
    update(initial_threshold)
    fig.subplots_adjust(left=.3, right=.7, bottom = .13, top=.6)
    # plt.savefig("leo.pgf")
    plt.show()

def get_geoms(obj):
    if hasattr(obj, "geoms"):  # Multi-type geometry
        return obj.geoms
    else:  # simple geometry
        return [obj]

def render_frame(threshold, file_prefix=None, frame_id=None, render_tetras=False, debug=False):
    if frame_id is None:
        frame_id = threshold
    if file_prefix is None:
        file_prefix = "../figs/leo"
    
    # Create collections of edges and faces (lines and triangles)
    lines = []
    tris = []
    tri_dist = []
    for s0 in range(n_stars):
        for s1 in range(s0 + 1, n_stars):
            lines.append([coords[s0], coords[s1]])
            for s2 in range(s1 + 1, n_stars):
                if triangles[s0, s1, s2] <= threshold:
                    tris.append([coords[s0], coords[s1], coords[s2]])
                    tri_dist.append(triangles[s0, s1, s2])
    line_dist = pdist(coords) / 2
    
    # Sort and filter by threshold (triangles are already filtered)
    line_dist, lines = zip(*sorted(zip(line_dist, lines), key = lambda t: t[0]))
    i = bisect.bisect(line_dist, threshold)
    lines = lines[:i]
    
    # Get better polygon for triangles (giving up on drawing tetrahedra by opacity or whatever)
    multitri = shapely.MultiPolygon([(shell, []) for shell in tris])
    geoms = get_geoms(multitri.buffer(0))
    tri_patch_xys = []
    for geom in geoms:
        if shapely.get_num_coordinates(geom):
            tri_patch_xys.append((geom.exterior.xy, [int_geom.xy for int_geom in geom.interiors]))
    
    # Get tetrahedra
    tetras = []
    tetra_patch_xys = []
    if render_tetras:
        t2 = threshold * threshold
        for tetra in it.combinations(coords, 4):
            c, r2 = miniball.get_bounding_ball(np.array(tetra))
            if r2 <= t2:
                tetras.append(tetra)
                # print(tetra)
        multitetra = shapely.GeometryCollection([shapely.convex_hull(shapely.MultiPoint(tetra)) for tetra in tetras])
        geoms = get_geoms(multitetra.buffer(0))
        for geom in geoms:
            if shapely.get_num_coordinates(geom):
                tetra_patch_xys.append((geom.exterior.xy, [int_geom.xy for int_geom in geom.interiors]))
    
    # Ripple guy
    sublevelset = shapely.MultiPoint(coords)
    geoms = get_geoms(sublevelset.buffer(threshold))
    sls_xys = []
    for geom in geoms:
        if shapely.get_num_coordinates(geom):
            sls_xys.append(geom.exterior.xy)
            sls_xys.extend([int_geom.xy for int_geom in geom.interiors])
    
    filename = f"{file_prefix}-{frame_id}.pgf"
    with open(filename, 'w', encoding="utf-8") as f:
        render_to_pgf(
            f, sls_xys, tri_patch_xys, tetra_patch_xys, lines, coords, magnitude,
            edge_line_width=(30 - threshold) / 20,
            debug=debug
        )
    
    return

def render_to_pgf(
        f,                      # output file
        sls_xys,                # ripple coords
        tri_patch_xys,          # triangle coords (unioned)
        tetra_patch_xys,        # tetrahedra coords (unioned)
        lines,                  # edge coords
        coords,                 # point coords
        magnitude,              # point radii
        tri_gray=.8,            # triangle grayscale shade
        tetra_gray=.5,          # tetrahedra grayscale shade
        ripple_line_width=.4,   # ripple line width
        edge_line_width=1.5,    # edge line width
        debug=False
    ):
    endline = ""
    if debug:
        endline = "%\n"
    # start PGF
    f.write("\\begin{pgfpicture}" + endline)
    f.write(f"\\definecolor{{tri}}{{gray}}{{{tri_gray}}}" + endline)
    f.write(f"\\definecolor{{tetra}}{{gray}}{{{tetra_gray}}}" + endline)
    
    # Add ripple
    if debug:
        f.write("% ==== RIPPLE ====\n")
    f.write(f"\\pgfsetlinewidth{{{ripple_line_width}pt}}" + endline)
    f.write("\\pgfsetstrokecolor{black}" + endline)
    for xs, ys in sls_xys:
        f.write(f"\\pgfpathqmoveto{{{xs[0]:.5f}pt}}{{{ys[0]:.5f}pt}}" + endline)
        for i in range(len(xs) - 1):
            f.write(f"\\pgfpathqlineto{{{xs[i]:.5f}pt}}{{{ys[i]:.5f}pt}}" + endline)
        f.write("\\pgfpathclose" + endline)
    f.write("\\pgfusepathqstroke" + endline)
    
    # Add triangles
    if debug:
        f.write("% ==== TRIANGLES ====\n")
    f.write("\\pgfsetfillcolor{tri}" + endline)
    for ext_xys, int_xys_list in tri_patch_xys:
        xs, ys = ext_xys
        f.write(f"\\pgfpathqmoveto{{{xs[0]:.5f}pt}}{{{ys[0]:.5f}pt}}" + endline)
        for i in range(len(xs) - 1):
            f.write(f"\\pgfpathqlineto{{{xs[i]:.5f}pt}}{{{ys[i]:.5f}pt}}" + endline)
        f.write("\\pgfpathclose" + endline)
        for xs, ys in int_xys_list:
            f.write(f"\\pgfpathqmoveto{{{xs[0]:.5f}pt}}{{{ys[0]:.5f}pt}}" + endline)
            for i in range(len(xs) - 1):
                f.write(f"\\pgfpathqlineto{{{xs[i]:.5f}pt}}{{{ys[i]:.5f}pt}}" + endline)
            f.write("\\pgfpathclose" + endline)
    f.write("\\pgfusepathqfill" + endline)
    
    # Add tetrahedra
    if debug:
        f.write("% ==== TETRAHEDRA ====\n")
    f.write("\\pgfsetfillcolor{tetra}" + endline)
    for ext_xys, int_xys_list in tetra_patch_xys:
        xs, ys = ext_xys
        f.write(f"\\pgfpathqmoveto{{{xs[0]:.5f}pt}}{{{ys[0]:.5f}pt}}" + endline)
        for i in range(len(xs) - 1):
            f.write(f"\\pgfpathqlineto{{{xs[i]:.5f}pt}}{{{ys[i]:.5f}pt}}" + endline)
        f.write("\\pgfpathclose" + endline)
        for xs, ys in int_xys_list:
            f.write(f"\\pgfpathqmoveto{{{xs[0]:.5f}pt}}{{{ys[0]:.5f}pt}}" + endline)
            for i in range(len(xs) - 1):
                f.write(f"\\pgfpathqlineto{{{xs[i]:.5f}pt}}{{{ys[i]:.5f}pt}}" + endline)
            f.write("\\pgfpathclose" + endline)
    if tetra_patch_xys:  # nonempty
        f.write("\\pgfusepathqfill" + endline)
    
    # Add edges
    if debug:
        f.write("% ==== EDGES ====\n")
    f.write(f"\\pgfsetlinewidth{{{edge_line_width}pt}}" + endline)
    f.write("\\pgfsetstrokecolor{black}" + endline)
    for s, t in lines:
        f.write(f"\\pgfpathqmoveto{{{s[0]:.5f}pt}}{{{s[1]:.5f}pt}}" + endline)
        f.write(f"\\pgfpathqlineto{{{t[0]:.5f}pt}}{{{t[1]:.5f}pt}}" + endline)
    f.write("\\pgfusepathqstroke" + endline)
    
    # Add stars
    if debug:
        f.write("% ==== POINTS ====\n")
    f.write("\\pgfsetfillcolor{white}" + endline)
    for s0 in range(n_stars):
        x, y = coords[s0]
        r = magnitude[s0]
        f.write(f"\\pgfpathcircle{{\\pgfqpoint{{{x:.5f}pt}}{{{y:.5f}pt}}}}{{{r + 1:.5f}pt}}" + endline)
    f.write("\\pgfusepathqfill" + endline)
    f.write("\\pgfsetfillcolor{black}" + endline)
    for s0 in range(n_stars):
        x, y = coords[s0]
        r = magnitude[s0]
        f.write(f"\\pgfpathcircle{{\\pgfqpoint{{{x:.5f}pt}}{{{y:.5f}pt}}}}{{{r:.5f}pt}}" + endline)
    f.write("\\pgfusepathqfill" + endline)
    
    # end PGF
    f.write(
"""\
\\end{pgfpicture}%
"""
    )
    return

def plot_barcode(diag):
    """
    diag is the output of VR.fit_transform()
    """
    birth = diag[:, 0]
    death = diag[:, 1]
    finite_bars = death[death != np.inf]
    
    if len(finite_bars) > 0:
        inf_end = 1.1 * max(finite_bars)
    else:
        inf_end = 2
    death[death == np.inf] = inf_end
    
    fig, ax = plt.subplots(1, 2, figsize=(9 * .8, 5 * .8))
    
    # diagonal line
    ax[1].plot([0, inf_end], [0, inf_end], 'k--', linewidth=2)
    
    legend_artists = [None, None]
    for i, (b, d) in enumerate(zip(birth, death)):
        if d == inf_end:
            ax[0].plot([b, d], [i, i], color="#000061", lw=3)
            ax[1].plot(b, d, color="#000061", marker='o', markersize=5)
        else:
            dim = int(diag[i, 2])
            c = ("#000061", "#E86A58")[dim]
            ax[0].plot([b, d], [i, i], color=c, lw=3)
            legend_artists[dim], = ax[1].plot(b, d, color=c, marker='o', markersize=5)
    # random infinite bar?
    # ax[0].plot([0, inf_end], [-1, -1], color="#000061", lw=3)
    # ax[1].plot(0, inf_end, color="#000061", marker='o', markersize=5)
    # diagonal
    
    ax[0].set_title('Barcode')
    ax[0].set_xlabel('filtration value')
    ax[0].set_yticks([])
    
    ax[1].axis("equal")
    ax[1].set_title("Persistence diagram")
    ax[1].set_xlabel("birth")
    ax[1].set_ylabel("death")
    ax[1].legend(legend_artists, [r"$𝐻_0$", r"$𝐻_1$"], facecolor="none", edgecolor="none", handlelength=0.)
    
    fig.tight_layout()
    # plt.show()
    
    plt.savefig("../figs/barcode-diagram.png", dpi=300, transparent=True)
    return


def barcode_stuff():
    cpx = gd.AlphaComplex(points=coords).create_simplex_tree()  # output_squared_values=False is an option
    cpx.compute_persistence()
    diag = cpx.persistence(persistence_dim_max=2)
    diag_array = np.zeros((len(diag), 3), dtype=float)
    for i, element in enumerate(diag):
        diag_array[i] = (element[1][0], element[1][1], element[0])
    diag_array[:, :2] = np.sqrt(diag_array[:, :2])
    diag_array = diag_array[np.lexsort((diag_array[:, 1], diag_array[:, 0], diag_array[:, 2]))]
    # print(diag_array)
    plot_barcode(diag_array)

def flipbook_stuff():
    for i, t in enumerate(np.linspace(0, 17, endpoint=True, num=44)):
        print(f"[flipbook] rendering frame {i}...")
        render_frame(t, file_prefix="../figs/flip/leo", frame_id=i, render_tetras=True)
        print(f"[flipbook] done!")

if __name__ == "__main__":
    # visualize()
    # render_frame(10, render_tetras=True, debug=True)
    flipbook_stuff()
    # barcode_stuff()