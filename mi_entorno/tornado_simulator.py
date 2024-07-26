import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.widgets import Slider, Button

class TornadoSimulator:
    def __init__(self, num_particulas, num_frames):
        self.num_particulas = num_particulas
        self.num_frames = num_frames
        self.radius_max = 1.0
        self.lon_center, self.lat_center = -100, 35
        self.R0 = 0.1  # Radio del núcleo sólido del vórtice de Rankine
        self.circulation = 1.0  # Circulación del vórtice
        self.fig, self.ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
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

        self.particles_value = 1
        self.lifetime_value = 5.0

        # Layout de los controles
        self.text_particles_label = plt.text(0.24, 0.11, f'Partículas/s: {self.particles_value}', transform=self.fig.transFigure,
                                             fontsize=12, color='black', ha='center', va='center')

        self.increase_particles_button = plt.axes([0.3, 0.10, 0.05, 0.03], facecolor='lightgoldenrodyellow')
        self.decrease_particles_button = plt.axes([0.36, 0.10, 0.05, 0.03], facecolor='lightgoldenrodyellow')

        self.increase_particles = Button(self.increase_particles_button, '+', color='lightgoldenrodyellow', hovercolor='lightblue')
        self.decrease_particles = Button(self.decrease_particles_button, '-', color='lightgoldenrodyellow', hovercolor='lightblue')
        self.increase_particles.on_clicked(self.increase_particles_per_second)
        self.decrease_particles.on_clicked(self.decrease_particles_per_second)

        self.text_lifetime_label = plt.text(0.52, 0.11, f'Tiempo de Vida: {self.lifetime_value:.2f}', transform=self.fig.transFigure,
                                            fontsize=12, color='black', ha='center', va='center')

        self.increase_lifetime_button = plt.axes([0.6, 0.10, 0.05, 0.03], facecolor='lightgoldenrodyellow')
        self.decrease_lifetime_button = plt.axes([0.66, 0.10, 0.05, 0.03], facecolor='lightgoldenrodyellow')

        self.increase_lifetime = Button(self.increase_lifetime_button, '+', color='lightgoldenrodyellow', hovercolor='lightblue')
        self.decrease_lifetime = Button(self.decrease_lifetime_button, '-', color='lightgoldenrodyellow', hovercolor='lightblue')
        self.increase_lifetime.on_clicked(self.increase_lifetime_per_second)
        self.decrease_lifetime.on_clicked(self.decrease_lifetime_per_second)

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.anim = None
        self.frame_count = 0
        self.particles_per_second = self.particles_value
        self.particle_lifetime = self.lifetime_value

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
            new_vx, new_vy = self.calculate_vortex_velocity(new_x, new_y)
            new_life_time = np.array([self.particle_lifetime])

            self.x = np.append(self.x, new_x)
            self.y = np.append(self.y, new_y)
            self.vx = np.append(self.vx, new_vx)
            self.vy = np.append(self.vy, new_vy)
            self.life_time = np.append(self.life_time, new_life_time)

    def calculate_vortex_velocity(self, x, y):
        r = np.sqrt(x**2 + y**2)
        if r < self.R0:
            v_theta = self.circulation / (2 * np.pi * self.R0)
        else:
            v_theta = self.circulation / (2 * np.pi * r)
        
        theta = np.arctan2(y, x)
        vx = v_theta * np.cos(theta + np.pi / 2)
        vy = v_theta * np.sin(theta + np.pi / 2)
        
        return vx, vy

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

        # Velocidad angular inversamente proporcional a la distancia
        v_theta = self.circulation / (2 * np.pi * dist)
        self.vx = v_theta * -dy / dist
        self.vy = v_theta * dx / dist

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

    def increase_particles_per_second(self, event):
        self.particles_per_second += 1
        self.text_particles_label.set_text(f'Partículas/s: {self.particles_per_second}')
        print(f'Número de partículas por segundo actualizado: {self.particles_per_second}')

    def decrease_particles_per_second(self, event):
        self.particles_per_second = max(1, self.particles_per_second - 1)
        self.text_particles_label.set_text(f'Partículas/s: {self.particles_per_second}')
        print(f'Número de partículas por segundo actualizado: {self.particles_per_second}')

    def increase_lifetime_per_second(self, event):
        self.particle_lifetime += 0.5
        self.text_lifetime_label.set_text(f'Tiempo de Vida: {self.particle_lifetime:.2f}')
        print(f'Tiempo de vida de las partículas actualizado: {self.particle_lifetime:.2f}')

    def decrease_lifetime_per_second(self, event):
        self.particle_lifetime = max(0.1, self.particle_lifetime - 0.5)
        self.text_lifetime_label.set_text(f'Tiempo de Vida: {self.particle_lifetime:.2f}')
        print(f'Tiempo de vida de las partículas actualizado: {self.particle_lifetime:.2f}')

    def on_click(self, event):
        if event.inaxes == self.ax:
            self.lon_center, self.lat_center = event.xdata, event.ydata
            print(f'Nuevo centro del tornado: longitud {self.lon_center:.2f}, latitud {self.lat_center:.2f}')

def start_animation():
    sim = TornadoSimulator(num_particulas=100, num_frames=200)
    sim.animate()

if __name__ == "__main__":
    start_animation()
