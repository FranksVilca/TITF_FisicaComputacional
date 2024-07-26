import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.widgets import Slider, TextBox

class TornadoSimulator:
    def __init__(self, num_particulas, num_frames):
        self.num_particulas = num_particulas
        self.num_frames = num_frames
        self.radius_max = 1.0
        self.lon_center, self.lat_center = -100, 35
        self.fig, self.ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
        self.ax.set_extent([-130, -65, 24, 50], crs=ccrs.PlateCarree())  # Focalizando en Estados Unidos
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.add_feature(cfeature.BORDERS)
        self.ax.add_feature(cfeature.STATES)
        self.ax.add_feature(cfeature.LAND, edgecolor='black')
        self.ax.add_feature(cfeature.OCEAN)
        self.ax.add_feature(cfeature.LAKES, edgecolor='black')
        self.ax.add_feature(cfeature.RIVERS)
        self.ax.gridlines(draw_labels=True)

        self.init_particles()

        self.particulas = self.ax.scatter(self.lon_center + self.x, self.lat_center + self.y, c='blue', transform=ccrs.PlateCarree())

        self.slider_radius = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.slider_radius_bar = Slider(self.slider_radius, 'Radio del Tornado', 0.1, 10.0, valinit=self.radius_max, valstep=0.1)
        self.slider_radius_bar.on_changed(self.update_radius)

        self.slider_velocity = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.slider_velocity_bar = Slider(self.slider_velocity, 'Velocidad de Partículas', 0.001, 0.1, valinit=0.01, valstep=0.001)
        self.slider_velocity_bar.on_changed(self.update_velocity)

        self.textbox_particles = plt.axes([0.2, 0.10, 0.2, 0.03], facecolor='lightgoldenrodyellow')
        self.textbox_particles_bar = TextBox(self.textbox_particles, 'Partículas/s:', initial='1', color='black')
        self.textbox_particles_bar.on_submit(self.update_particles_per_second)

        self.textbox_lifetime = plt.axes([0.5, 0.10, 0.2, 0.03], facecolor='lightgoldenrodyellow')
        self.textbox_lifetime_bar = TextBox(self.textbox_lifetime, 'Tiempo de Vida:', initial='5.0', color='black')
        self.textbox_lifetime_bar.on_submit(self.update_lifetime)

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.anim = None
        self.frame_count = 0
        self.particles_per_second = 1  # Número inicial de partículas por segundo
        self.particle_lifetime = 5.0  # Tiempo de vida inicial de las partículas

    def init_particles(self):
        self.x = np.array([])
        self.y = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])
        self.life_time = np.array([])

    def add_particle(self):
        for _ in range(self.particles_per_second):
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, self.radius_max)
            new_x = radius * np.cos(angle)
            new_y = radius * np.sin(angle)
            new_vx = np.random.uniform(-0.01, 0.01)
            new_vy = np.random.uniform(-0.01, 0.01)
            new_life_time = np.array([self.particle_lifetime])

            self.x = np.append(self.x, new_x)
            self.y = np.append(self.y, new_y)
            self.vx = np.append(self.vx, new_vx)
            self.vy = np.append(self.vy, new_vy)
            self.life_time = np.append(self.life_time, new_life_time)

    def update(self, frame):
        self.frame_count += 1

        if self.frame_count % (50 // self.particles_per_second) == 0:
            self.add_particle()

        self.life_time -= 1 / 50  # Aproximadamente 50 frames por segundo

        mask = self.life_time > 0
        self.x = self.x[mask]
        self.y = self.y[mask]
        self.vx = self.vx[mask]
        self.vy = self.vy[mask]
        self.life_time = self.life_time[mask]

        centro_x, centro_y = 0, 0

        dx = centro_x - self.x
        dy = centro_y - self.y
        dist = np.sqrt(dx**2 + dy**2)
        dist = np.clip(dist, 0.01, self.radius_max)  # Evitar divisiones por cero

        # Fuerza central dependiente de la distancia al centro
        fuerza_central = 0.002 / dist
        self.vx += fuerza_central * dx / dist
        self.vy += fuerza_central * dy / dist

        # Velocidad angular inversamente proporcional a la distancia
        angulo = np.arctan2(dy, dx)
        velocidad_angular = 0.05 / dist
        self.vx += velocidad_angular * -np.sin(angulo)
        self.vy += velocidad_angular * np.cos(angulo)

        self.vy += 0.0002 * dist

        max_velocidad = self.slider_velocity_bar.val
        velocidad = np.sqrt(self.vx**2 + self.vy**2)
        self.vx = np.where(velocidad > max_velocidad, self.vx * max_velocidad / velocidad, self.vx)
        self.vy = np.where(velocidad > max_velocidad, self.vy * max_velocidad / velocidad, self.vy)

        self.x += self.vx
        self.y += self.vy

        self.particulas.set_offsets(np.c_[self.lon_center + self.x, self.lat_center + self.y])

        # Colores según la distancia al centro (más azul cuando está lejos, más rojo cuando está cerca)
        colors = plt.cm.coolwarm(1 - dist / self.radius_max)
        self.particulas.set_color(colors)

    def animate(self):
        self.anim = animation.FuncAnimation(self.fig, self.update, frames=self.num_frames, interval=50, repeat=True)
        plt.show()

    def update_radius(self, radius):
        self.radius_max = radius
        print(f'Radio del tornado actualizado: {radius:.2f}')

    def update_velocity(self, velocity):
        print(f'Velocidad de partículas actualizada: {velocity:.3f}')

    def update_particles_per_second(self, text):
        try:
            self.particles_per_second = int(text)
            print(f'Número de partículas por segundo actualizado: {self.particles_per_second}')
        except ValueError:
            print("Ingrese un valor numérico válido para las partículas por segundo.")

    def update_lifetime(self, text):
        try:
            self.particle_lifetime = float(text)
            print(f'Tiempo de vida de las partículas actualizado: {self.particle_lifetime:.2f}')
        except ValueError:
            print("Ingrese un valor numérico válido para el tiempo de vida.")

    def on_click(self, event):
        if event.inaxes == self.ax:
            self.lon_center, self.lat_center = event.xdata, event.ydata
            print(f'Nuevo centro del tornado: longitud {self.lon_center:.2f}, latitud {self.lat_center:.2f}')

def start_animation():
    sim = TornadoSimulator(num_particulas=100, num_frames=200)
    sim.animate()

if __name__ == "__main__":
    start_animation()
