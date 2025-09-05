import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os 
load_dotenv()


def selecionar_porcentagem_cpu():

    config = {
      'user': os.getenv("USER"),
      'password': os.getenv("PASSWORD"),
      'host': os.getenv("HOST"),
      'database': os.getenv("DATABASE")
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            
            with db.cursor() as cursor:
                query = "SELECT * FROM aula_sis.cpu;"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
        
        
resultado = selecionar_porcentagem_cpu()
print(resultado)
