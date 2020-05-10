import pyodbc as odbc

conn = odbc.connect(r'Driver={Microsoft Access Driver (*.mdb, '
                    r'*.accdb)};DBQ=db\Кулинарная книга2.mdb;')
cursor = conn.cursor()
cursor.execute('select cooking from Книга where id_1=1')

for row in cursor.fetchall():
    print(row)
