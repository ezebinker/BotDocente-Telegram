import sqlite3
from model.archivo import Archivo

class DBHelper:

    def __init__(self, dbname="bot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tbl1stmt = "CREATE TABLE IF NOT EXISTS archivos (id INTEGER NOT NULL, nombre TEXT, topPalabras TEXT, PRIMARY KEY (id), UNIQUE (nombre))"
        nombreidx = "CREATE INDEX IF NOT EXISTS nombreIndex ON archivos (nombre ASC)" 
        tbl2stmt = "CREATE TABLE IF NOT EXISTS conceptos (id INTEGER NOT NULL, texto TEXT, PRIMARY KEY (id))"
        textoidx = "CREATE INDEX IF NOT EXISTS textoIndex ON conceptos (texto ASC)"
        tbl3stmt = "CREATE TABLE IF NOT EXISTS conceptosxarchivos (archivo_id INTEGER, concepto_id INTEGER, FOREIGN KEY (archivo_id) REFERENCES archivos (id),FOREIGN KEY (concepto_id)REFERENCES conceptos (id) ) "

        self.conn.execute(tbl1stmt)
        self.conn.execute(nombreidx)
        self.conn.execute(tbl2stmt)
        self.conn.execute(textoidx)
        self.conn.execute(tbl3stmt)
        self.conn.commit()

    def add_archivo(self, archivo):
        stmt = "INSERT INTO temas (nombre, topPalabras) VALUES (?,?)"
        args = (archivo.nombre, archivo.topPalabras)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_last_id(self):
        stmt = "SELECT last_insert_rowid()"
        cursor = self.conn.execute(stmt)
        for row in cursor:
            id = row[0]
        return id

    def get_archivos(self):
        stmt = "SELECT nombre, topPalabras FROM archivos"
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchall()
        datos = []
        for row in rows:
            archivo = Archivo(row[0],row[1])
            datos.append(archivo)
            print (archivo.nombre + " " + archivo.topPalabras)
        return datos

db = DBHelper()
print(str(db.get_archivos()))