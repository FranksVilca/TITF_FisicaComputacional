import matplotlib.pyplot as plt
from tornado_simulator import TornadoSimulator

def start_animation():
    sim = TornadoSimulator(num_particulas=100, num_frames=200)  # Asegúrate de que los parámetros coincidan
    plt.show()

if __name__ == "__main__":
    start_animation()
