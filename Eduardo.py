import tkinter as tk
import random
import math

class TornadoSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Tornados")

        # Configuración del lienzo
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack(padx=10, pady=10)

        # Botón de iniciar simulación
        self.btn_iniciar = tk.Button(self.root, text="Iniciar Tornado", command=self.iniciar_tornado)
        self.btn_iniciar.pack(pady=10)

        # Variables del tornado
        self.x_centro = 400
        self.y_centro = 300
        self.radio = 50
        self.num_particulas = 200
        self.color_tornado = 'gray'
        self.particulas = []

    def iniciar_tornado(self):
        # Limpiar el lienzo
        self.canvas.delete(tk.ALL)

        # Dibujar el tornado (círculo y partículas)
        self.canvas.create_oval(self.x_centro - self.radio, self.y_centro - self.radio,
                                self.x_centro + self.radio, self.y_centro + self.radio,
                                outline=self.color_tornado, width=2)

        # Generar partículas aleatorias dentro del radio del tornado
        for _ in range(self.num_particulas):
            r = random.uniform(0, self.radio)
            theta = random.uniform(0, 2 * math.pi)
            x_particula = self.x_centro + r * math.cos(theta)
            y_particula = self.y_centro + r * math.sin(theta)
            self.particulas.append(self.canvas.create_oval(x_particula - 1, y_particula - 1,
                                                           x_particula + 1, y_particula + 1,
                                                           fill=self.color_tornado))

        # Simular movimiento del tornado
        self.simular_movimiento_tornado()

    def simular_movimiento_tornado(self):
        for _ in range(50):  # Simular 50 iteraciones
            for idx, particula in enumerate(self.particulas):
                # Movimiento aleatorio de las partículas
                dx = random.uniform(-2, 2)
                dy = random.uniform(-2, 2)
                self.canvas.move(particula, dx, dy)
                # Girar partículas alrededor del centro del tornado
                self.rotar_particula(particula)

            self.root.update()  # Actualizar la ventana
            self.root.after(100)  # Esperar 0.1 segundos entre cada iteración

    def rotar_particula(self, particula):
        # Calcular posición relativa a partir del centro del tornado
        x, y, _, _ = self.canvas.coords(particula)
        dx = x - self.x_centro
        dy = y - self.y_centro
        # Ángulo de rotación
        angulo = random.uniform(0, 2 * math.pi)
        # Nueva posición rotada
        nueva_x = self.x_centro + dx * math.cos(angulo) - dy * math.sin(angulo)
        nueva_y = self.y_centro + dx * math.sin(angulo) + dy * math.cos(angulo)
        self.canvas.coords(particula, nueva_x - 1, nueva_y - 1, nueva_x + 1, nueva_y + 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = TornadoSimulator(root)
    root.mainloop()
