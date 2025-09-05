import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv

load_dotenv()

def selecionar_porcentagem_cpu(calcular):
    
    config = {
        'user': 'USERNAME_DB',
        'password': 'PASSWORD_DB',
        'host': 'HOST_DB',
        'database': 'DATABASE_DB'

    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.get_server_info()
            print('Connected to MySQL server version -', db_info)
    
            with db.cursor() as cursor: 
                if calcular == "cpu":
                    query = "SELECT usoCPU, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM cyberbeef.componentes ORDER BY id DESC LIMIT 1;"
                elif calcular == "ram":
                    query = "SELECT ram, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM cyberbeef.componentes ORDER BY id DESC LIMIT 1;"
                elif calcular == "disco":
                    query = "SELECT disco, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM cyberbeef.componentes ORDER BY id DESC LIMIT 1;"
                elif calcular == "deletar":
                    query = " DELETE FROM cyberbeef.componentes WHERE id IN (SELECT id FROM (SELECT id FROM cyberbeef.componentes ORDER BY id DESC LIMIT 5) AS temp);"
                    print("Deletando...")
                    cursor.execute(query)
                    db.commit()
                    return None
                elif calcular == "update":
                    query = "UPDATE cyberbeef.componentes  SET dthora = NOW() WHERE id IN (SELECT id FROM (SELECT id FROM cyberbeef.componentes  ORDER BY id DESC LIMIT 3) AS temp);"
                    print("Atualizando...")
                    cursor.execute(query)
                    db.commit()
                    return None
                else:
                    query = "SELECT usoCPU, ram, disco, DATE_FORMAT(dthora, '%d/%m/%Y %H:%i:%s') FROM cyberbeef.componentes ORDER BY id DESC LIMIT 1;"
                
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
         
while True:
    calcular = input("O que deseja ver (CPU/RAM/DISCO)? Para ver todos pressione enter, para parar digite 'sair' e caso queira deletar os ultimos 5 registros, digite 'deletar'. Para apenas atualizar 'update': ").lower()

    if calcular == "sair":
        print("Encerrando...")
        break

    resultado = selecionar_porcentagem_cpu(calcular)

    if resultado:
        print("Resultado:", resultado)