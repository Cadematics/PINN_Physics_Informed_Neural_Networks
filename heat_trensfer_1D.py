import numpy as np
import matplotlib.pyplot as plt


# Parameters
a = 110
length = 100 # mm 
time = 4 #seconds


nodes = 100 

dx = length / nodes 
dt = 0.5 * dx**2 /a 
t_nodes = int(time / dt)    


# Initial condition
u = np.zeros(nodes) + 20  # Initial temperature in °C

# Boundary conditions
u[0] = 100  # Boundary condition at the left end (°C)
u[-1] = 100  # Boundary condition at the right end (°C)

# Plotting the results
fig, ax = plt.subplots()
pcm = ax.pcolormesh([u], cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=ax, label='Temperature (°C)')
ax.set_ylim([-2,3])




counter = 0 

while counter < time:

    w = u.copy()

    for i in range(1 , nodes -1):
        u[i] = w[i] + a * dt * (w[i-1] - 2*w[i] + w[i+1])/ dx**2 

    counter += dt
    print (f"Time: {counter:.2f} seconds, Temperature distribution: {u}")
    pcm.set_array([u])  # Update the color mesh with the new temperature distribution
    plt.pause(0.01)  # Pause to update the plot



plt.show()


