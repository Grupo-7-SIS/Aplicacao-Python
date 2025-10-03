#!/usr/bin/env python
import mysql.connector
from mysql.connector import Error
import datetime
import psutil
import time

DB_CONFIG = {
    'host': '52.91.191.206',
    'user': 'root',
    'password': 'stevejobs',
    'database': 'cyberbeef',
    'port': 3306
}

ID_MAQUINA = 1
INTERVALO = 5

def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Erro na conexão com o banco: {e}")
        return None

def obter_ou_criar_componente(nome, unidade, id_maquina):
    db = conectar()
    if db is None:
        return None
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT idComponente FROM componente
            WHERE nomeComponente = %s AND unidadeMedida = %s AND idMaquina = %s
        """, (nome, unidade, id_maquina))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]

        cursor.execute("""
            INSERT INTO componente (nomeComponente, unidadeMedida, idMaquina)
            VALUES (%s, %s, %s)
        """, (nome, unidade, id_maquina))
        db.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Erro ao obter ou criar componente '{nome}': {e}")
        return None
    finally:
        cursor.close()
        db.close()

def inserir_leitura(id_componente, id_maquina, valor, nome, unidade):
    db = conectar()
    if db is None:
        return
    try:
        cursor = db.cursor()
        agora = datetime.datetime.now()
        cursor.execute("""
            INSERT INTO leitura (idComponente, idMaquina, dado, dthCaptura, idNucleo)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_componente, id_maquina, valor, agora, None))
        db.commit()
        
        print(f"[{agora.strftime('%Y-%m-%d %H:%M:%S')}] Componente: {nome:<6} | Unidade: {unidade:<3} | Valor: {valor:.2f}")
        
    except Error as e:
        print(f"Erro ao inserir leitura: {e}")
    finally:
        cursor.close()
        db.close()

def capturar_metricas():
    # CPU %
    cpu_percent = psutil.cpu_percent(interval=1)

    # RAM em GB (uso atual)
    ram_uso_gb = psutil.virtual_memory().used / (1024 ** 3)

    # Disco em GB (uso atual)
    disco_uso_gb = psutil.disk_usage('/').used / (1024 ** 3)

    return {
        ("CPU", "%"): cpu_percent,
        ("RAM", "GB"): ram_uso_gb,
        ("DISCO", "GB"): disco_uso_gb
    }

def iniciar_monitoramento():
    print("Iniciando monitoramento... (Ctrl + C para parar)\n")
    while True:
        metricas = capturar_metricas()
        for (nome, unidade), valor in metricas.items():
            id_comp = obter_ou_criar_componente(nome, unidade, ID_MAQUINA)
            if id_comp:
                inserir_leitura(id_comp, ID_MAQUINA, valor, nome, unidade)
        time.sleep(INTERVALO)

if __name__ == "__main__":
    iniciar_monitoramento()
