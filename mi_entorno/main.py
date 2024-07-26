from tornado_simulator import TornadoSimulator

def start_animation():
    # Crear una instancia de TornadoSimulator con los parámetros actualizados
    sim = TornadoSimulator(num_particulas=100, num_frames=200)  # Puedes ajustar num_particulas si es necesario
    sim.animate()

if __name__ == "__main__":
    start_animation()
