import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class TornadoSimulator:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 800)
        self.ax.set_ylim(0, 600)
        self.ax.set_facecolor('lightblue')
        self.ax.set_aspect('equal', 'box')
        self.num_particulas = 200
        self.radio = 50
        self.x_centro = 400
        self.y_centro = 300
        self.particulas, = self.ax.plot([], [], 'o', color='gray', alpha=0.7, markersize=5)
        self.x_particulas = np.random.uniform(0, 800, self.num_particulas)
        self.y_particulas = np.random.uniform(0, 600, self.num_particulas)
        self.angles = np.zeros(self.num_particulas)
        self.radii = np.zeros(self.num_particulas)
        self.phase = 0  # 0: moving to center, 1: rotating

        # Añadir un círculo en el centro del tornado para referencia visual
        circle = plt.Circle((self.x_centro, self.y_centro), self.radio, color='red', fill=False, linestyle='--')
        self.ax.add_artist(circle)

    def init(self):
        self.particulas.set_data([], [])
        return self.particulas,

    def update(self, frame):
        if self.phase == 0:
            # Movimiento de las partículas hacia el centro
            direction_x = self.x_centro - self.x_particulas
            direction_y = self.y_centro - self.y_particulas
            distance = np.sqrt(direction_x**2 + direction_y**2)
            move_step = 5
            self.x_particulas += move_step * direction_x / distance
            self.y_particulas += move_step * direction_y / distance

            # Comprobar si todas las partículas están cerca del centro
            if np.all(distance < move_step):
                self.phase = 1  # Cambiar a fase de rotación
                self.radii = np.random.uniform(0, self.radio, self.num_particulas)
                self.angles = np.random.uniform(0, 2 * np.pi, self.num_particulas)
        else:
            # Rotar partículas alrededor del centro del tornado
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
