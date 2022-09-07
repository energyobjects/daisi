from IPython.display import HTML
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.animation import writers
from numba import jit
import numpy as np
import os
from PIL import Image, ImageOps
import streamlit as st
import tempfile
import time

#initial_grid = np.zeros(shape=(imgshape[0], imgshape[1]), dtype=np.int8)
#for i in range(imgshape[0]):
#    for j in range(imgshape[1]):
#        initial_grid[i,j] = (int(npimg[i,j,0]) + npimg[i,j,1] + npimg[i,j,2]) > mid_value

# Random initial grid
#initial_grid = np.random.randint(2, size=(imgshape[0], imgshape[1]))

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

@jit(nopython=True)
def _cgol_tick2(grid_a: np.array, grid_b: np.array, grid_shape):
    for y in range(grid_shape[0]):
        # For each horizontal index
        for x in range(grid_shape[1]):
            new_state = grid_a[x,y]
            neighbor_count = 0
            neighbor_count += grid_a[x-1][y-1] if x > 0 and y > 0 else 0
            neighbor_count += grid_a[x-1][y] if x > 0 else 0
            neighbor_count += grid_a[x-1][y+1] if x > 0 and y < grid_shape[0] - 1 else 0
            neighbor_count += grid_a[x+1][y-1] if x < grid_shape[1] - 1 and y > 0 else 0
            neighbor_count += grid_a[x+1][y] if x < grid_shape[1] - 1 else 0
            neighbor_count += grid_a[x+1][y+1] if x < grid_shape[1] - 1 and y < grid_shape[0] - 1 else 0
            neighbor_count += grid_a[x][y-1] if y > 0 else 0
            neighbor_count += grid_a[x][y+1] if x > 0 and y < grid_shape[0] - 1 else 0

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
    # For each timestep
    for t in range(timesteps):
        # For each vertical index
        im = plt.imshow(grid_a, animated=True, cmap="Greys")
        ims.append([im])
        _cgol_tick(grid_a, grid_b, grid_shape)
        tmp_grid = grid_a
        grid_a = grid_b
        grid_b = tmp_grid
    plt.axis('off')
    plt.close()
    anim = animation.ArtistAnimation(fig, ims, interval=100, repeat=False)
    tmp_dir = tempfile.gettempdir()
    anim.save(f"{tmp_dir}/cgol.gif", writer='pillow')

    del grid_b
    del grid_a

    return f"{tmp_dir}/cgol.gif"

def st_ui():
    st.title("Conway's Game of Life")
    time_steps = st.slider('How many time steps?', 10, 200, 100, 10)
    user_image = st.sidebar.file_uploader("Load your own image")
    if user_image is not None:
        src_img = Image.open(user_image)
    else:
        src_img = Image.open("cute_robot_daisy.png")
    w, h = src_img.size
    if h > 720:
        src_img = src_img.resize((int((float(src_img.size[0]) * float((720 / float(src_img.size[1]))))), 720), Image.NEAREST)
    st.header("Original image")
    st.image(src_img)
    draw_landmark_button = st.button('Run the Simulation')
    npimg = np.array(src_img)
    imgshape = npimg.shape
    mid_value = int(np.iinfo(npimg.dtype).max / 2) * imgshape[2]

    initial_grid = np.zeros(shape=(imgshape[0]+2, imgshape[1]+2), dtype=np.int8)
    for i in range(imgshape[0]):
        for j in range(imgshape[1]):
            initial_grid[i+1,j+1] = (int(npimg[i,j,0]) + npimg[i,j,1] + npimg[i,j,2]) < mid_value

    ani_file = cgol(initial_grid, time_steps)
    if draw_landmark_button:
        st.header("Game Animation")
        with open(ani_file, "rb") as fp:
            btn = st.download_button(
                label="Download Animation",
                data=fp,
                file_name="cgol.gif",
                mime="image/gif"
            )


if __name__ == '__main__':
    st_ui()
