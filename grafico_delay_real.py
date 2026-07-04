import matplotlib.pyplot as plt

# Throughput real calculado desde los logs de tshark (bytes totales / duracion)
# Baseline (~123 kbps) tomado del bitrate estable reportado por FFmpeg en vivo,
# en vez del valor anomalo de la primera captura (0ms dio 243.5 kbps por rafaga inicial)
delay_ms = [0, 50, 200, 500, 1500, 5000, 10000, 20000]
throughput_kbps = [123, 138.6, 131.1, 127.9, 123.0, 112.3, 105.7, 5.1]

labels = [str(d) for d in delay_ms]

plt.figure(figsize=(8, 5))
plt.plot(labels, throughput_kbps, marker='o')

# Marcar el colapso final (pipeline crasheo al terminar la captura de 20000ms)
plt.scatter([labels[-1]], [throughput_kbps[-1]], color='red', zorder=5,
            label='Colapso (FFmpeg crasheo por completo al estar en 20000ms)')

plt.title('Delay vs Throughput (datos reales tshark)')
plt.xlabel('Delay (ms)')
plt.ylabel('Throughput (kbps)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico_delay_vs_throughput.png', dpi=200)
print("Guardado: grafico_delay_vs_throughput.png")
