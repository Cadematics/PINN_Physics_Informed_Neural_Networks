import numpy as np
import matplotlib.pyplot as plt


# Parameters
a = 110
length = 100 # mm 
time = 4 #seconds


nodes = 100 

dx = length / nodes 
dy = length / nodes


dt = min(dx**2 /(4*a), dy**2 /(4*a))

t_nodes = int(time / dt)    


# Initial condition
u = np.zeros((nodes, nodes)) + 20  # Initial temperature in °C

# Boundary conditions
u[0, :] = 100  # Boundary condition at the left end (°C)
# u[-1, :] = 100  # Boundary condition at the right end (°C)
# u[:, 0] = 100  # Boundary condition at the bottom end (°C)
# u[:, -1] = 100  # Boundary condition at the top end (°C)



# Plotting the results
fig, ax = plt.subplots()
pcm = ax.pcolormesh(u, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=ax, label='Temperature (°C)')






counter = 0 

while counter < time:

    w = u.copy()

    for i in range(1 , nodes -1):
        for j in range(1 , nodes -1):
            
            dd_ux = (w[i-1, j] - 2*w[i, j] + w[i+1, j]) / dx**2
            dd_uy = (w[i, j+1] - 2*w[i, j] + w[i, j-1]) / dy**2

            u[i,j] = dt * a * (dd_ux + dd_uy) + w[i,j]




    counter += dt
    print (f"Time: {counter:.2f} seconds, Temperature distribution: {u}")
    pcm.set_array(u)  # Update the color mesh with the new temperature distribution
    plt.pause(0.01)  # Pause to update the plot



plt.show()


