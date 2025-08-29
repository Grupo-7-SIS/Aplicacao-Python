import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv

load_dotenv()

def componentes_servidor(cpu,disco,ram,rede):

    config = {
        'user': USER_DB,
        'password': PASSWORD_DB,
        'host': HOST_DB,
        'database': DATABASE_DB
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            
            with db.cursor() as cursor:
                query = ""
                value = (cpu, disco, ram,rede, )
                cursor.execute(query, value)
                
                db.commit()
                print(cursor.rowcount, "registro inserido")
            
            cursor.close()
            db.close()
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
        
for i in range(20):

    cpu = p.cpu_percent(interval=1, percpu=False)
    disco = p.disk_usage('/').percent
    ram = p.virtual_memory().percent
    rede = p.net_io_counters()
    print(f"")
    componentes_servidor(cpu, disco, ram, rede ) 