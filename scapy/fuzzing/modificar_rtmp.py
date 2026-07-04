from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import random

contador_paquetes = {"n": 0}
MODIFICACION_ACTIVA = 2

def modificar_timestamp(payload):
    if len(payload) > 4:
        payload = bytearray(payload)
        payload[1] = random.randint(0, 255)
        payload[2] = random.randint(0, 255)
        payload[3] = random.randint(0, 255)
        return bytes(payload)
    return payload

def modificar_csid(payload):
    if len(payload) > 0:
        payload = bytearray(payload)
        fmt_bits = payload[0] & 0b11000000
        nuevo_csid = random.randint(2, 63)
        payload[0] = fmt_bits | nuevo_csid
        return bytes(payload)
    return payload

def modificar_message_length(payload):
    if len(payload) > 7:
        payload = bytearray(payload)
        payload[4] = random.randint(0, 255)
        payload[5] = random.randint(0, 255)
        payload[6] = random.randint(0, 255)
        return bytes(payload)
    return payload

def procesar_paquete(pkt):
    scapy_pkt = IP(pkt.get_payload())

    if scapy_pkt.haslayer(Raw):
        contador_paquetes["n"] += 1

        if contador_paquetes["n"] % 50 == 0:
            payload_original = bytes(scapy_pkt[Raw].load)

            if MODIFICACION_ACTIVA == 1:
                payload_modificado = modificar_timestamp(payload_original)
                print("[MOD 1 - Timestamp] Paquete #" + str(contador_paquetes["n"]) + " modificado")
            elif MODIFICACION_ACTIVA == 2:
                payload_modificado = modificar_csid(payload_original)
                print("[MOD 2 - CSID] Paquete #" + str(contador_paquetes["n"]) + " modificado")
            elif MODIFICACION_ACTIVA == 3:
                payload_modificado = modificar_message_length(payload_original)
                print("[MOD 3 - Message Length] Paquete #" + str(contador_paquetes["n"]) + " modificado")
            else:
                payload_modificado = payload_original

            scapy_pkt[Raw].load = payload_modificado
            del scapy_pkt[IP].len
            del scapy_pkt[IP].chksum
            del scapy_pkt[TCP].chksum

            pkt.set_payload(bytes(scapy_pkt))

    pkt.accept()

print("[+] Escuchando cola NFQUEUE #1. Modificacion activa: " + str(MODIFICACION_ACTIVA))
print("[+] Presiona Ctrl+C para detener.")

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesar_paquete)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print("[+] Deteniendo...")
    nfqueue.unbind()
