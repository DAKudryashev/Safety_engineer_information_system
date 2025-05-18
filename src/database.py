import psycopg2

from config import DBNAME, USER, PASSWORD, HOST


class DataBase:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST)
        self.curs = self.connection.cursor()

    def __del__(self):
        self.connection.commit()
        self.curs.close()
        self.connection.close()

    def get_engineers(self):
        self.curs.execute('SELECT * FROM engineers')
        return self.curs.fetchall()

    def get_regulatory_documents(self):
        self.curs.execute('''
            SELECT 
                name,
                to_char(creation_date, 'DD.MM.YYYY') as formatted_date,
                url
            FROM regulatory_documents
        ''')
        return self.curs.fetchall()

    def get_internal_documents(self):
        self.curs.execute('''
            SELECT
                d.name AS document_name,
                to_char(d.creation_date, 'DD.MM.YYYY') AS creation_date,
                e.name AS engineer_name,
                d.file_path
            FROM
                internal_documents d
            JOIN
                engineers e ON d.responsible = e.engineer_id
        ''')
        return self.curs.fetchall()


if __name__ == '__main__':
    db = DataBase()
    print(db.get_internal_documents())
