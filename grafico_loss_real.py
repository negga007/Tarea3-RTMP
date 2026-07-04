import matplotlib.pyplot as plt

# Throughput real calculado desde los logs de tshark (bytes totales / duracion)
# Baseline (~123 kbps) tomado del bitrate estable reportado por FFmpeg en vivo
loss_pct = [0, 2, 5, 10, 20, 40]
throughput_kbps = [123, 223.5, 196.5, 174.4, 158.2, 114.1]

plt.figure(figsize=(8, 5))
plt.plot(loss_pct, throughput_kbps, marker='o', color='green')

# Marcar el colapso final (pipeline crasheo al terminar la captura de 40%)
plt.scatter([loss_pct[-1]], [throughput_kbps[-1]], color='red', zorder=5,
            label='Colapso (FFmpeg crasheo por completo al estar en 40% de packet loss)')

plt.title('Packet Loss vs Throughput (datos reales tshark)')
plt.xlabel('Packet loss (%)')
plt.ylabel('Throughput (kbps)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico_loss_vs_throughput.png', dpi=200)
print("Guardado: grafico_loss_vs_throughput.png")
