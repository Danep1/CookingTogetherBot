import pyodbc as odbc

conn = odbc.connect(r'Driver={Microsoft Access Driver (*.mdb, '
                    r'*.accdb)};DBQ=db\Кулинарная книга.mdb;')
cursor = conn.cursor()
cursor.execute('select * from Разделы')

for row in cursor.fetchall():
    print(row)