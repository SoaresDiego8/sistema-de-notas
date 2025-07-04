import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

print("Conectando...")
try:
    load_dotenv()

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Usuário ou senha incorretos.')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Banco de dados não encontrado.')
    else:
        print(err)
    exit()
else:
    print("Conexão estabelecida com sucesso!")

cursor = conn.cursor()

# Listando usuários
cursor.execute('SELECT * FROM login')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(f'Nome: {user[1]}')

# Listando Login
cursor.execute('SELECT * FROM lista_de_notas')
print(' -------------  Notas:  -------------')
for nota in cursor.fetchall():
    print(f'Nota: {nota[2]}')

cursor.close()
conn.close()
