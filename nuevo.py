import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class TornadoSimulator:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 800)
        self.ax.set_ylim(0, 600)
        self.num_particulas = 200
        self.radio = 50
        self.x_centro = 400
        self.y_centro = 300
        self.particulas, = self.ax.plot([], [], 'o', color='gray')
        self.angles = np.random.uniform(0, 2 * np.pi, self.num_particulas)
        self.radii = np.random.uniform(0, self.radio, self.num_particulas)
        self.x_particulas = self.x_centro + self.radii * np.cos(self.angles)
        self.y_particulas = self.y_centro + self.radii * np.sin(self.angles)

    def init(self):
        self.particulas.set_data([], [])
        return self.particulas,

    def update(self, frame):
        self.angles += 0.1  # Ajustar para cambiar la velocidad de rotación
        self.x_particulas = self.x_centro + self.radii * np.cos(self.angles)
        self.y_particulas = self.y_centro + self.radii * np.sin(self.angles)
        self.particulas.set_data(self.x_particulas, self.y_particulas)
        return self.particulas,

    def start(self):
        ani = animation.FuncAnimation(self.fig, self.update, init_func=self.init, frames=200, interval=50, blit=True)
        plt.show()

simulator = TornadoSimulator()
simulator.start()
