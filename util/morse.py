# -*-coding:utf8-*-

"""
Render torus for illustrating Morse functions.
"""

import pyvista as pv

pv.global_theme.transparent_background = True

torus = pv.ParametricTorus()
plotter = pv.Plotter(window_size=(420, 520), off_screen=False, lighting='three lights')

def callback(x):
    '''
    This function is called everytime the user right-clicks in the scene. 
    x is the mouse coordinates of the 3D point clicked on.
    '''

    print(x) # not really relevant here
    print(f'camera position: {plotter.camera.position}')
    print(f'camera az,rol,elev: {plotter.camera.azimuth},{plotter.camera.roll},\
        {plotter.camera.elevation}')
    print(f'camera view angle, focal point: {plotter.camera.view_angle,plotter.camera.focal_point}')

# now set the camera parameters in the code
plotter.track_click_position(callback)
plotter.camera.position = (1.973742561652129, 4.003212044362904, 3.628009192211756)#(2.8567601919386445, 5.735962610119241, 5.460484312754356)
plotter.camera.azimuth = 0
plotter.camera.roll = 108.55745572817646
plotter.camera.elevation = 0
plotter.camera.view_angle = 33.2409972299169
plotter.camera.focal_point = (0.02253691180673456, 0.0854724021805123, -0.10157506620935983)


critical_points = [
    (-1.5, 0, 0),
    (-.5, 0, 0),
    (.5, 0, 0),
    (1.5, 0, 0)
]

def render_figs(heights=[-1.2, -.49, .51, 2]):
    for i, h in enumerate(heights):
        mesh = torus.clip(normal='x', value=h)
        actor0 = plotter.add_mesh(mesh, color='#B2E0E0', smooth_shading=True)
        
        sphere = pv.Sphere(radius=.07, center=critical_points[i])
        actor1 = plotter.add_mesh(sphere, color='E86A58', lighting=False)

        plotter.screenshot(f"../figs/morse/morse-{i}.png", window_size=(420, 520), scale=2)
        plotter.remove_actor(actor0)
        plotter.remove_actor(actor1)

def make_nested(heights=[-.7, 0, .7, 2], csradius=[.8, .7, .6, .5]):
    for i, h in enumerate(heights):
        mesh = pv.ParametricTorus(crosssectionradius=csradius[i]).clip(normal='x', value=h)
        plotter.add_mesh(mesh, color='#FFBE00', smooth_shading=True)
    plotter.show()

if __name__ == "__main__":
    render_figs()
    # make_nested()
