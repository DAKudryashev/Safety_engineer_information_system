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

    def get_engineers_without_passwords(self):
        self.curs.execute('SELECT engineer_id, name FROM engineers')
        return self.curs.fetchall()

    def get_regulatory_documents(self):
        self.curs.execute('''
            SELECT
                document_id, 
                name,
                to_char(creation_date, 'DD.MM.YYYY') as formatted_date,
                url
            FROM
                regulatory_documents
        ''')
        return self.curs.fetchall()

    def get_internal_documents(self):
        self.curs.execute('''
            SELECT
                d.internal_document_id,
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

    def get_rooms(self):
        self.curs.execute('''
            SELECT
                r.room_id, 
                r.name AS room_name,
                r.state,
                to_char(r.check_date, 'DD.MM.YYYY') AS check_date,
                e.name AS responsible    
            FROM 
                rooms r
            JOIN 
                engineers e ON r.responsible = e.engineer_id;
        ''')
        return self.curs.fetchall()

    def get_planned_briefings(self):
        self.curs.execute('''
            SELECT
                b.planned_briefing_id,
                b.name,
                b.topic,
                to_char(b.planned_date, 'DD.MM.YYYY') AS planned_date,
                e.name AS responsible,
                d.file_path AS file_path
            FROM
                planned_briefings b
            JOIN
                engineers e ON b.responsible = e.engineer_id
            LEFT JOIN
                internal_documents d ON b.documentation = d.internal_document_id
        ''')
        return self.curs.fetchall()

    def get_completed_briefings(self):
        self.curs.execute('''
            SELECT
                b.completed_briefing_id,
                b.name,
                b.topic,
                to_char(b.completion_date, 'DD.MM.YYYY') AS completion_date,
                e.name AS responsible,
                d.file_path AS file_path
            FROM
                completed_briefings b
            JOIN
                engineers e ON b.responsible = e.engineer_id
            LEFT JOIN
                internal_documents d ON b.documentation = d.internal_document_id        
        ''')
        return self.curs.fetchall()

    def get_examinations(self):
        self.curs.execute('''
            SELECT
                e.examination_id,
                e.name,
                to_char(e.date, 'DD.MM.YYYY') AS date,
                eng.name AS responsible,
                e.results,
                d.file_path
            FROM
                examinations e
            JOIN
                engineers eng ON e.responsible = eng.engineer_id
            JOIN
                internal_documents d ON e.documentation = d.internal_document_id
        ''')
        return self.curs.fetchall()

    def get_med_examinations(self):
        self.curs.execute('''
            SELECT
                e.medical_examination_id,
                e.name,
                to_char(e.date, 'DD.MM.YYYY') AS date,
                e.results,
                d.file_path
            FROM
                medical_examinations e
            JOIN
                internal_documents d ON e.documentation = d.internal_document_id
        ''')
        return self.curs.fetchall()

    def get_employees(self):
        self.curs.execute('''
            SELECT
                e.employee_id,
                e.name,
                e.pasport_series,
                e.pasport_number,
                e.position,
                e.instructed,
                b.name,
                exam.name,
                exam.results,
                med_exam.name,
                med_exam.results
            FROM
                employees e
            LEFT JOIN
                completed_briefings b ON e.by_briefing = b.completed_briefing_id
            LEFT JOIN
                examinations exam ON e.examination = exam.examination_id
            LEFT JOIN
                medical_examinations med_exam ON e.med_examination = med_exam.medical_examination_id
        ''')
        return self.curs.fetchall()

    def get_equipment(self):
        self.curs.execute('''
            SELECT
                e.equipment_id,
                e.name,
                r.name,
                e.supplier,
                to_char(e.manufacture_date, 'DD.MM.YYYY') AS manufacture_date,
                to_char(e.sell_by_date, 'DD.MM.YYYY') AS sell_by_date,
                eng.name
            FROM
                equipment e
            JOIN
                rooms r ON e.location = r.room_id
            JOIN
                engineers eng ON e.responsible = eng.engineer_id        
        ''')
        return self.curs.fetchall()

    def get_incidents(self):
        self.curs.execute('''
            SELECT
                i.incident_id,
                i.content,
                to_char(i.date, 'DD.MM.YYYY') AS date,
                e.name,
                emp.name,
                i.proof_path
            FROM
                incidents i
            LEFT JOIN
                engineers e ON i.responsible = e.engineer_id
            LEFT JOIN
                employees emp ON i.participant = emp.employee_id        
        ''')
        return self.curs.fetchall()

    def get_complaints(self):
        self.curs.execute('''
            SELECT
                c.complaint_id,
                emp.name,
                c.content,
                to_char(c.date, 'DD.MM.YYYY') AS date,
                c.status,
                e.name
            FROM
                complaints c
            JOIN
                employees emp ON c.by=emp.employee_id
            JOIN
                engineers e ON c.responsible = e.engineer_id        
        ''')
        return self.curs.fetchall()


if __name__ == '__main__':
    db = DataBase()
    print(db.get_engineers_without_passwords())
