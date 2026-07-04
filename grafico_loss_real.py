import matplotlib.pyplot as plt

loss_pct = [0, 2, 5, 10, 20, 40]
throughput_kbps = [123, 223.5, 196.5, 174.4, 158.2, 114.1]

plt.figure(figsize=(8, 5))
plt.plot(loss_pct, throughput_kbps, marker='o', color='green')

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
