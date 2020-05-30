import sqlite3

class DBHelper:

    def __init__(self, dbname="bot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        tbl1stmt = "CREATE TABLE IF NOT EXISTS temas (id INTEGER NOT NULL, nombre TEXT, PRIMARY KEY (id), UNIQUE (nombre))"
        nombreidx = "CREATE INDEX IF NOT EXISTS nombreIndex ON temas (nombre ASC)" 
        tbl2stmt = "CREATE TABLE IF NOT EXISTS respuestas (id INTEGER NOT NULL, texto TEXT, texto_busqueda TEXT, en_respuesta_a TEXT, PRIMARY KEY (id))"
        textoidx = "CREATE INDEX IF NOT EXISTS textoIndex ON respuestas (texto ASC)"
        enrespidx= "CREATE INDEX IF NOT EXISTS enrespIndex ON respuestas (en_respuesta_a ASC)"
        tbl3stmt = "CREATE TABLE IF NOT EXISTS temaspreguntas (tema_id INTEGER, respuesta_id INTEGER, FOREIGN KEY (tema_id) REFERENCES temas (id),FOREIGN KEY (respuesta_id)REFERENCES respuestas (id) ) "
        self.conn.execute(tbl1stmt)
        self.conn.execute(nombreidx)
        self.conn.execute(tbl2stmt)
        self.conn.execute(textoidx)
        self.conn.execute(enrespidx)
        self.conn.execute(tbl3stmt)
        self.conn.commit()

    def add_tema(self, nombre):
        stmt = "INSERT INTO temas (nombre) VALUES (?)"
        args = (nombre, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_last_id(self):
        stmt = "SELECT last_insert_rowid()"
        cursor = self.conn.execute(stmt)
        for row in cursor:
            id = row[0]
        return id

    def get_temas(self):
        stmt = "SELECT nombre FROM temas"
        cursor = self.conn.execute(stmt)
        result = [item[0] for item in cursor.fetchall()]
        return result