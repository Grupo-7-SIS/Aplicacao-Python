import psutil as p
from mysql.connector import connect, Error
from tabulate import tabulate
import platform
import time
import datetime
import sys

def selecionar_porcentagem_cpu(calcular, quantos=None):
    config = {
        'user': "aluno",
        'password': "sptech",
        'host': 'localhost',
        'database': "aula_sis"
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.get_server_info()
            print('Connected to MySQL server version -', db_info)
    
            with db.cursor() as cursor: 
                if calcular == "1":
                    query = "SELECT porcentagem, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM aula_sis.cpu ORDER BY id DESC LIMIT 5;"
                elif calcular == "2":
                    query = "SELECT ram, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM aula_sis.cpu ORDER BY id DESC LIMIT 5;"
                elif calcular == "3":
                    query = "SELECT disco, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM aula_sis.cpu ORDER BY id DESC LIMIT 5;"
                elif calcular == "update":
                    query = "UPDATE aula_sis.cpu SET dthora = NOW() WHERE id IN (SELECT id FROM (SELECT id FROM aula_sis.cpu ORDER BY id DESC LIMIT 3) AS temp);"
                    print("Atualizando...")
                    cursor.execute(query)
                    db.commit()
                    return None
                elif calcular == "4":
                    query = "SELECT porcentagem, ram, disco, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM aula_sis.cpu ORDER BY id DESC LIMIT 5;"
                
                if calcular != "deletar":
                    cursor.execute(query)
                    resultado = cursor.fetchall()
                    return resultado
                        
    except Error as e:
        print('Error to connect with MySQL -', e)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()




def insercao(porcentagem, ram, disco, dthoraformat):

    config = {
      'user': "aluno",
      'password': "sptech",
      'host': 'localhost',
      'database': "aula_sis"
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            
            with db.cursor() as cursor:
                query = "INSERT INTO aula_sis.cpu (id, porcentagem, ram, disco, dthora) VALUES (null, %s, %s, %s, %s)"
                value = (porcentagem, ram, disco, dthoraformat)
                cursor.execute(query, value)
                
                db.commit()
                print(cursor.rowcount, "registro inserido")
            
            cursor.close()
            db.close()
    
    except Error as e:
        print('Error to connect with MySQL -', e) 





def sair():
    print("Obrigado por usar nosso sistema! Saindo...")
    sys.exit(0)


def sistema():
    while True:
        print("|=================================|")
        print("|           CYBERBEEF             |")
        print("|=================================|")
        print("| 1 - INSERIR REGISTROS           |")
        print("| 2 - MONITORAMENTO DO SISTEMA    |")
        print("| 3 - ENVIAR FEEDBACK             |")
        print("| 0 - Sair                        |")
        print("|=================================|")

        escolha = input("\n Escolha o que deseja ver: ")

        if escolha not in ["0", "1", "2", "3"]:
                    print("⚠️  Opção inválida! Tente novamente.")
                    continue

        if escolha == "1":
            insercaoDados()

        if escolha == "2":
            monitoramentoSistema()

        if escolha == "3":
            feedback()

        if escolha == "0":
            sair()


def insercaoDados():

    while True:
        print("|=================================|")
        print("|            INSERÇÃO             |")
        print("|=================================|")
        print("| 1 - INSERIR APENAS 1 REGISTRO   |")
        print("| 2 - 10 REGISTROS POR MINUTO     |")
        print("| 3 - 20 REGISTROS POR MINUTO     |")
        print("| 4 - INSIRA NÚMERO DE REGISTROS  |")
        print("| 0 - Voltar                      |")
        print("|=================================|")

        intervalo = input("\n Insira a opção desejada: ")

        if intervalo not in ["0", "1", "2", "3", "4"]:
                    print("⚠️  Opção inválida! Tente novamente.")
                    continue

        if intervalo == "1":         
                
                porcentagem = p.cpu_percent(interval=1, percpu=False)

                ram = p.virtual_memory().percent

                disco = p.disk_usage("/").percent

                dthora = datetime.datetime.now()
                dthoraformat = dthora.strftime("%Y-%m-%d %H:%M:%S")

                insercao(porcentagem, ram, disco, dthoraformat)


        if intervalo == "2":         
                
                while 10:

                    porcentagem = p.cpu_percent(interval=1, percpu=False)

                    ram = p.virtual_memory().percent

                    disco = p.disk_usage("/").percent

                    dthora = datetime.datetime.now()
                    dthoraformat = dthora.strftime("%Y-%m-%d %H:%M:%S")

                    insercao(porcentagem, ram, disco, dthoraformat)

                    time.sleep(6)
        
        if intervalo == "3":    

                while 20:     
                
                    porcentagem = p.cpu_percent(interval=1, percpu=False)

                    ram = p.virtual_memory().percent

                    disco = p.disk_usage("/").percent

                    dthora = datetime.datetime.now()
                    dthoraformat = dthora.strftime("%Y-%m-%d %H:%M:%S")

                    insercao(porcentagem, ram, disco, dthoraformat)

                    time.sleep(3)


        if intervalo == "4":
            tempo = int(input("\n Escolha quantas inserções por minuto: "))

            while tempo:

                porcentagem = p.cpu_percent(interval=1, percpu=False)

                ram = p.virtual_memory().percent

                disco = p.disk_usage("/").percent

                dthora = datetime.datetime.now()
                dthoraformat = dthora.strftime("%Y-%m-%d %H:%M:%S")

                insercao(porcentagem, ram, disco, dthoraformat)

                time.sleep(60 / tempo)


        if intervalo == "0":
            print("\n Voltando...")
            break




def feedback():
    mensagem = str(input("Nos ajude a melhorar nosso sistema: "))
    print("|=================================|")
    print("|            FEEDBACK             |")
    print("|=================================|")
    
    if len(mensagem) > 31:
        mensagem = mensagem[:28] + "..."

    print(f"| {mensagem:<31} |")

    for _ in range(2):
        print("|                                 |")


         
def monitoramentoSistema():
    while True:
        print("|=================================|")
        print("|      MONITORAMENTO DO SISTEMA   |")
        print("|=================================|")
        print("| 1 - Ver Componentes             |")
        print("| 2 - Ver Processos em execução   |")
        print("| 3 - Ver informações de rede     |")
        print("| 4 - Ver usuários logados        |")
        print("| 5 - Ver uptime do sistema       |")
        print("| 0 - Voltar                      |")
        print("|=================================|")

        escolha = int(input("\n Insira o que deseja ver: "))
        if escolha == 1:
        
            while True:
                print("|=================================|")
                print("|   MONITORAMENTO DE COMPONENTES  |")
                print("|=================================|")
                print("| 1 - Ver uso de CPU              |")
                print("| 2 - Ver uso de RAM              |")
                print("| 3 - Ver uso de Disco            |")
                print("| 4 - Ver Todos                   |")
                print("| 0 - Voltar                      |")
                print("|=================================|")

        
                calcular = input("\n Insira o que deseja ver: ")

                if calcular not in ["0", "1", "2", "3", "4"]:
                    print("⚠️  Opção inválida! Tente novamente.")
                    continue

                if calcular == "0":
                    print("\n Voltando...")
                    break
                    
                resultado = selecionar_porcentagem_cpu(calcular)

                if calcular == "1":
                    print("\n", tabulate(resultado, headers=["CPU EM USO", "DATA DA CAPTURA"], tablefmt="fancy_grid"), "\n")
                    

                if calcular == "2":
                    print("\n", tabulate(resultado, headers=["RAM EM USO", "DATA DA CAPTURA"], tablefmt="fancy_grid"), "\n")
                    

                if calcular == "3":
                    print("\n", tabulate(resultado, headers=["DISCO EM USO", "DATA DA CAPTURA"], tablefmt="fancy_grid"), "\n")
                    

                if calcular == "4":
                    print("\n", tabulate(resultado, headers=["CPU EM USO","RAM EM USO", "DISCO EM USO", "DATA DA CAPTURA"], tablefmt="fancy_grid"), "\n")

                


        if escolha == 2:
            processos = []
            nucleosFisicos = p.cpu_count(logical=False)  # Apenas núcleos físicos

            for i in p.process_iter():
                    cpu_porcentagem = i.cpu_percent(interval=None)
                    cpu_percentagem_fisico = cpu_porcentagem / nucleosFisicos
                    processos.append([i.name(),(cpu_percentagem_fisico)])


            time.sleep(0.5)

            '''EU REPETI O MESMO CODIGO 2 VEZES PRA PODER USAR O INTERVALO NULO, PARA A COLETA SER MAIS RAPIDA E RETORNAR ALGO, SE NÃO TIVESSE REUTILIZADO O CODIGO A COLETA DEMORARIA MAIS.'''

            '''PEGA OS 10 PROCESSOS MAIS RELEVANTES'''
                        
            for i in p.process_iter():
                    cpu_porcentagem = i.cpu_percent(interval=None)
                    cpu_percentagem_fisico = cpu_porcentagem / nucleosFisicos
                    if i.name().lower() == "system idle process":
                        continue
                    processos.append([i.name(),(cpu_percentagem_fisico)])
                
            
            processos.sort(key=lambda x: x[1], reverse=True)
            
            print(tabulate(processos[:10], headers=["NOME", "CPU(%)"], tablefmt="fancy_grid"))

        if escolha == 3:
            status = p.net_io_counters()
            rede = [
                ["Pacotes Enviados", status.packets_sent],
                ["Pacotes Recebidos", status.packets_recv],
                ["Erros de Envio", status.errout],
                ["Erros de Recepção", status.errin],
            ]
    
            print(tabulate(rede, headers=["Métricas (unidades)", "Valor"], tablefmt="fancy_grid"))

        if escolha == 4:
            usuarios = p.users()

            if not usuarios:
                print("Nenhum usuário logado no momento.")
                return
            
            for usuario in usuarios:
                tempoAtivo = datetime.datetime.fromtimestamp(usuario.started).strftime('%H:%M:%S')
                print(f"{usuario.name} - desde {tempoAtivo}")
            
            print(f"\nTotal: {len(usuarios)} usuário(s) logado(s)")


        if escolha == 5:
            data_ligou = datetime.datetime.fromtimestamp(p.boot_time())

            '''VALE LEMBRAR QUE ELE CONTA DESDE QUE O SISTEMA INICIALIZOU, CONTANDO COM SUSPENSÃO E HIBERNAÇÃO'''
    
            segundos_ligado = time.time() - p.boot_time()
            horas = int(segundos_ligado // 3600)
            minutos = int((segundos_ligado % 3600) // 60)
            
            print(f"\n Ligado desde: {data_ligou.strftime('%d/%m %H:%M')}")
            print(f"Tempo ligado: {horas}h {minutos}min")

        if escolha == 0:
            sistema()
             

sistema()
