from classifier import classifier

# Ustawianie parametrów połączenia z bazą danych
user = 'user'
password = 'password'
host = 'host'
port = 3306
database = 'database'

if __name__ == '__main__':
    classifier(user, password, host, port, database)
