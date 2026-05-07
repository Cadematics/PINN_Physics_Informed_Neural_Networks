import numpy as np

class DiffusionSolver:
    def __init__(self, alpha=110, length=100, nx=100, nt=None, time_steps=400, total_time=4):
        """
        1D Numerical Diffusion Solver using explicit finite difference.
        
        :param alpha: Thermal diffusivity
        :param length: Length of the domain
        :param nx: Number of spatial nodes
        :param nt: Number of time steps (overrides time_steps if provided)
        :param time_steps: Number of time steps
        :param total_time: Total simulation time
        """
        self.alpha = float(alpha)
        self.length = float(length)
        self.nx = int(nx)
        self.time_steps = int(nt) if nt is not None else int(time_steps)
        self.total_time = float(total_time)

    def solve(self):
        dx = self.length / self.nx
        dt = self.total_time / self.time_steps
        
        # Initial condition
        u = np.zeros(self.nx) + 20.0  # Initial temperature in °C
        
        # Boundary conditions
        u[0] = 100.0  # Boundary condition at the left end (°C)
        u[-1] = 100.0  # Boundary condition at the right end (°C)
        
        results = [u.copy().tolist()]
        
        for _ in range(self.time_steps):
            w = u.copy()
            for i in range(1, self.nx - 1):
                u[i] = w[i] + self.alpha * dt * (w[i-1] - 2*w[i] + w[i+1]) / (dx**2)
            results.append(u.tolist())
            
        return {
            "parameters": {
                "alpha": self.alpha,
                "length": self.length,
                "nx": self.nx,
                "time_steps": self.time_steps,
                "total_time": self.total_time,
                "dx": dx,
                "dt": dt
            },
            "results": results
        }
