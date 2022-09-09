import base64
from matplotlib import animation
from matplotlib import pyplot as plt
from numba import jit
import numpy as np
import os
from PIL import Image
import streamlit as st
import tempfile
import uuid

@jit(nopython=True)
def _cgol_tick(grid_a: np.array, grid_b: np.array, grid_shape):
    for y in range(1, grid_shape[0]-1):
        # For each horizontal index
        for x in range(1, grid_shape[1]-1):
            new_state = grid_a[x,y]
            neighbor_count = 0
            neighbor_count += grid_a[x-1][y-1]
            neighbor_count += grid_a[x-1][y]
            neighbor_count += grid_a[x-1][y+1]
            neighbor_count += grid_a[x+1][y-1]
            neighbor_count += grid_a[x+1][y]
            neighbor_count += grid_a[x+1][y+1]
            neighbor_count += grid_a[x][y-1]
            neighbor_count += grid_a[x][y+1]

            if grid_a[x,y] == 0:
                # Not alive
                if neighbor_count == 3:
                    new_state = 1
            else:
                # Alive
                if neighbor_count < 2 or neighbor_count > 3:
                    new_state = 0
            grid_b[x,y] = new_state

def cgol(initial: np.array, timesteps: int):
    fig = plt.figure()
    ims = []
    grid_shape = initial.shape
    grid_a = np.array(initial, copy=True)
    grid_b = np.zeros(shape=(grid_shape[0], grid_shape[1]), dtype=np.int8)
    progress_bar = st.progress(0)
    # For each timestep
    for t in range(timesteps):
        # For each vertical index
        im = plt.imshow(grid_a, animated=True, cmap="Greys")
        ims.append([im])
        _cgol_tick(grid_a, grid_b, grid_shape)
        tmp_grid = grid_a
        grid_a = grid_b
        grid_b = tmp_grid
        progress_bar.progress(t/(timesteps*1.5))
    plt.axis('off')
    plt.close()
    progress_bar.progress(timesteps/(timesteps*1.4))
    anim = animation.ArtistAnimation(fig, ims, interval=100, repeat=False)
    progress_bar.progress(timesteps/(timesteps*1.2))
    tmp_filename = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".gif")
    anim.save(tmp_filename, writer='pillow')

    del grid_b
    del grid_a
    progress_bar.progress(1.0)

    return tmp_filename

def st_ui():
    st.title("Conway's Game of Life")
    time_steps = st.sidebar.slider('How many time steps?', 10, 200, 100, 10)
    user_image = st.sidebar.file_uploader("Load your own image")
    if user_image is not None:
        src_img = Image.open(user_image)
    else:
        src_img = Image.open("cute_robot_daisy.png")
    w, h = src_img.size
    if h > 720:
        src_img = src_img.resize((int((float(src_img.size[0]) * float((720 / float(src_img.size[1]))))), 720), Image.NEAREST)
    st.header("The initial grid will be created from this image:")
    st.image(src_img)
    run_simulation_button = st.button('Run the Simulation')
    npimg = np.array(src_img)
    imgshape = npimg.shape
    mid_value = int(np.iinfo(npimg.dtype).max / 2) * imgshape[2]

    initial_grid = np.zeros(shape=(imgshape[0]+2, imgshape[1]+2), dtype=np.int8)
    for i in range(imgshape[0]):
        for j in range(imgshape[1]):
            initial_grid[i+1,j+1] = (int(npimg[i,j,0]) + npimg[i,j,1] + npimg[i,j,2]) < mid_value

    if run_simulation_button:
        ani_file = cgol(initial_grid, time_steps)
        st.header("The game animation as been generated:")
        with open(ani_file, "rb") as fp:
            contents = fp.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
                unsafe_allow_html=True,
                )


if __name__ == '__main__':
    st_ui()