import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class TopographicMap:
    def __init__(self, image_path):
        self.image_path = 'mapa-topografico-mundo.jpg'

    def plot_topographic_map(self):
        img = plt.imread(self.image_path)
        plt.imshow(img, extent=[-180, 180, -90, 90], transform=ccrs.PlateCarree())
        plt.gca().set_aspect('auto')

class TornadoSimulator:
    def __init__(self, num_particulas, num_frames, topographic_image):
        self.num_particulas = num_particulas
        self.num_frames = num_frames
        self.radius_max = 1.0  # Ajustado para que el radio inicial sea más grande
        self.lon_center, self.lat_center = -100, 35  # Coordenadas iniciales del centro del tornado
        self.fig, self.ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})

        # Crear el mapa base con cartopy
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.add_feature(cfeature.BORDERS, linestyle=':')
        self.ax.set_global()

        # Mostrar el mapa topográfico como fondo
        self.topo_map = TopographicMap(topographic_image)
        self.topo_map.plot_topographic_map()

        # Inicializar posiciones y velocidades de partículas
        self.x = np.random.uniform(-self.radius_max, self.radius_max, num_particulas)
        self.y = np.random.uniform(-self.radius_max, self.radius_max, num_particulas)
        self.vx = np.random.uniform(-0.01, 0.01, num_particulas)
        self.vy = np.random.uniform(-0.01, 0.01, num_particulas)

        # Convertir las posiciones iniciales al sistema de coordenadas del mapa
        self.particulas = self.ax.scatter(self.lon_center + self.x, self.lat_center + self.y, transform=ccrs.PlateCarree(), c='blue')

        # Añadir control de slider para el radio del tornado
        self.slider_radius = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.slider_radius_bar = plt.Slider(self.slider_radius, 'Radio del Tornado', 0.1, 10.0, valinit=self.radius_max, valstep=0.1)

        # Conectar el slider con la función de actualización del radio
        self.slider_radius_bar.on_changed(self.update_radius)

        # Añadir control de slider para la velocidad de las partículas
        self.slider_velocity = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.slider_velocity_bar = plt.Slider(self.slider_velocity, 'Velocidad de Partículas', 0.001, 0.1, valinit=0.01, valstep=0.001)

        # Conectar el slider con la función de actualización de velocidad
        self.slider_velocity_bar.on_changed(self.update_velocity)

        # Conectar el evento de clic en el mapa
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        # Almacenar la animación para poder controlarla
        self.anim = None

    def update(self, frame):
        centro_x, centro_y = 0, 0

        dx = centro_x - self.x
        dy = centro_y - self.y
        dist = np.sqrt(dx**2 + dy**2)

        # Velocidad radial hacia el centro
        fuerza_central = 0.002
        self.vx += fuerza_central * dx / dist
        self.vy += fuerza_central * dy / dist

        # Velocidad angular (rotación)
        angulo = np.arctan2(dy, dx)
        velocidad_angular = 0.005
        self.vx += velocidad_angular * -np.sin(angulo)
        self.vy += velocidad_angular * np.cos(angulo)

        # Movimiento vertical ascendente para simular el tornado
        self.vy += 0.0002 * dist

        # Limitar la velocidad para evitar que las partículas se expandan demasiado rápido
        max_velocidad = self.slider_velocity_bar.val
        velocidad = np.sqrt(self.vx**2 + self.vy**2)
        self.vx = np.where(velocidad > max_velocidad, self.vx * max_velocidad / velocidad, self.vx)
        self.vy = np.where(velocidad > max_velocidad, self.vy * max_velocidad / velocidad, self.vy)

        # Actualizar posiciones
        self.x += self.vx
        self.y += self.vy

        # Rebote en los límites de la figura
        self.x = np.clip(self.x, -self.radius_max, self.radius_max)
        self.y = np.clip(self.y, -self.radius_max, self.radius_max)

        # Generar nuevas partículas si el número es menor al máximo
        if len(self.x) < self.num_particulas:
            new_x = np.random.uniform(-self.radius_max, self.radius_max, self.num_particulas - len(self.x))
            new_y = np.random.uniform(-self.radius_max, self.radius_max, self.num_particulas - len(self.y))
            self.x = np.concatenate((self.x, new_x))
            self.y = np.concatenate((self.y, new_y))
            self.vx = np.concatenate((self.vx, np.random.uniform(-0.01, 0.01, self.num_particulas - len(self.vx))))
            self.vy = np.concatenate((self.vy, np.random.uniform(-0.01, 0.01, self.num_particulas - len(self.vy))))

        # Actualizar posiciones de las partículas en el mapa
        self.particulas.set_offsets(np.column_stack([self.lon_center + self.x, self.lat_center + self.y]))

    def animate(self):
        self.anim = animation.FuncAnimation(self.fig, self.update, frames=self.num_frames, interval=20, repeat=True)
        plt.show()

    def update_radius(self, radius):
        self.radius_max = radius
        self.x = np.random.uniform(-self.radius_max, self.radius_max, self.num_particulas)
        self.y = np.random.uniform(-self.radius_max, self.radius_max, self.num_particulas)
        self.vx = np.random.uniform(-0.01, 0.01, self.num_particulas)
        self.vy = np.random.uniform(-0.01, 0.01, self.num_particulas)
        if self.anim is not None:
            pass  # La animación se actualiza automáticamente al modificar los parámetros
        print(f'Radio del tornado actualizado: {radius:.2f}')

    def update_velocity(self, velocity):
        if self.anim is not None:
            # Detener la animación para aplicar los cambios de velocidad
            self.anim.event_source.stop()
        # Actualizar la velocidad de las partículas
        self.slider_velocity_bar.val = velocity
        print(f'Velocidad de partículas actualizada: {velocity:.3f}')
        if self.anim is not None:
            # Reiniciar la animación con la nueva velocidad
            self.animate()

    def on_click(self, event):
        if event.inaxes == self.ax:
            self.lon_center, self.lat_center = event.xdata, event.ydata
            self.x = np.random.uniform(-self.radius_max, self.radius_max, self.num_particulas)
            self.y = np.random.uniform(-self.radius_max, self.radius_max, self.num_particulas)
            self.vx = np.random.uniform(-0.01, 0.01, self.num_particulas)
            self.vy = np.random.uniform(-0.01, 0.01, self.num_particulas)
            print(f'Nuevo centro del tornado: longitud {self.lon_center:.2f}, latitud {self.lat_center:.2f}')

def start_animation():
    topo_image = 'mapa-topografico-mundo.jpg'
    sim = TornadoSimulator(num_particulas=100, num_frames=200, topographic_image=topo_image)
    sim.animate()

if __name__ == "__main__":
    start_animation()
