import sqlite3
from model.archivo import Archivo
from model.concepto import Concepto


class DBHelper:

    def __init__(self, dbname="bot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        drop1 = "DROP TABLE IF EXISTS archivos"
        drop2 = "DROP TABLE IF EXISTS conceptos"
        drop3 = "DROP TABLE IF EXISTS conceptosxarchivos"
        tbl1stmt = "CREATE TABLE IF NOT EXISTS archivos (id INTEGER NOT NULL, nombre TEXT, topPalabras TEXT, source TEXT, PRIMARY KEY (id), UNIQUE (nombre))"
        nombreidx = "CREATE INDEX IF NOT EXISTS nombreIndex ON archivos (nombre ASC)" 
        tbl2stmt = "CREATE TABLE IF NOT EXISTS conceptos (id INTEGER NOT NULL, texto TEXT, archivo INTEGER, PRIMARY KEY (id), FOREIGN KEY (archivo) REFERENCES archivos (id))"
        textoidx = "CREATE INDEX IF NOT EXISTS textoIndex ON conceptos (texto ASC)"
        tbl3stmt = "CREATE TABLE IF NOT EXISTS conceptosxarchivos (archivo_id INTEGER, concepto_id INTEGER, texto_busqueda TEXT, FOREIGN KEY (archivo_id) REFERENCES archivos (id),FOREIGN KEY (concepto_id)REFERENCES conceptos (id) ) "

        self.conn.execute(drop1)
        self.conn.execute(drop2)
        self.conn.execute(drop3)
        self.conn.execute(tbl1stmt)
        self.conn.execute(nombreidx)
        self.conn.execute(tbl2stmt)
        self.conn.execute(textoidx)
        self.conn.execute(tbl3stmt)
        self.conn.commit()

    def add_archivo(self, archivo):
        stmt = "INSERT INTO archivos (nombre, topPalabras, source) VALUES (?,?,?)"
        args = (archivo.nombre, archivo.topPalabras, archivo.source)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_concepto(self, concepto, archivo):
        stmt = "INSERT INTO conceptos (texto, archivo) VALUES (?,?)"
        args = (concepto,archivo)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_conceptosxarchivo(self, archivo, concepto, texto_busqueda):
        stmt = "INSERT INTO conceptosxarchivos (archivo_id, concepto_id, texto_busqueda) VALUES (?,?,?)"
        args = (archivo,concepto,texto_busqueda)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_last_id(self):
        stmt = "SELECT last_insert_rowid()"
        cursor = self.conn.execute(stmt)
        for row in cursor:
            id = row[0]
        return id

    def get_archivos(self):
        stmt = "SELECT nombre, topPalabras, source FROM archivos"
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchall()
        datos = []
        for row in rows:
            archivo = Archivo(row[0],row[1],row[2])
            datos.append(archivo)
        return datos

    def get_conceptos(self):
        stmt = "SELECT id, texto FROM conceptos"
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchall()
        datos = []
        for row in rows:
            concepto = Concepto(row[0],row[1])
            datos.append(concepto)
        return datos

    def get_rows_by_word(self, search):
        stmt = "SELECT distinct texto_busqueda FROM conceptosxarchivos WHERE texto_busqueda LIKE '%"+search+"%' LIMIT 5"
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchall()
        return rows

    def get_rows_by_concept(self, search):
        stmt = "SELECT id FROM conceptos WHERE texto LIKE '%"+search+"%'"
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchone()
        id= rows[0]
        stmt = "SELECT distinct texto_busqueda FROM conceptosxarchivos WHERE concepto_id ="+str(id)+" LIMIT 5"
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchall()
        return rows

db = DBHelper()
db.setup()