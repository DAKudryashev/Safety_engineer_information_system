import psycopg2

from config import DBNAME, USER, PASSWORD, HOST


class DataBase:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Паттерн Singleton
    def __init__(self):
        if not DataBase._initialized:
            self.connection = psycopg2.connect(
                dbname=DBNAME,
                user=USER,
                password=PASSWORD,
                host=HOST
            )
            # self.connection.autocommit = True
            self.curs = self.connection.cursor()
            DataBase._initialized = True

    def __del__(self):
        if hasattr(self, 'connection'):
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

    def get_regulatory_document_by_id(self, document_id):
        self.curs.execute(f'''
            SELECT
                name,
                to_char(creation_date, 'DD.MM.YYYY') as formatted_date,
                url
            FROM
                regulatory_documents
            WHERE document_id = {document_id}
                ''')
        return self.curs.fetchall()

    def search_regulatory_documents(self, data):
        self.curs.execute(f'''
            SELECT
                document_id, 
                name,
                to_char(creation_date, 'DD.MM.YYYY') as formatted_date,
                url
            FROM
                regulatory_documents
            WHERE
                name LIKE '%{data['name']}%'
                AND creation_date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
        ''')
        return self.curs.fetchall()

    def insert_regulatory_document(self, data):
        self.curs.execute(f"INSERT INTO regulatory_documents(name, creation_date, url) "
                          f"VALUES ('{data['name']}', DATE'{data['date']}', '{data['url']}')")

    def update_regulatory_document(self, data, document_id):
        self.curs.execute(f'''
                    UPDATE regulatory_documents
                    SET name = '{(data['name'])}', creation_date = DATE'{(data['date'])}', url = '{(data['url'])}'
                    WHERE document_id = {document_id}
                    ''')

    def delete_from_regulatory_documents(self, document_id):
        self.curs.execute(f"DELETE FROM regulatory_documents WHERE document_id = {document_id}")

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

    def get_internal_document_by_id(self, document_id):
        self.curs.execute(f'''
            SELECT
                d.name AS document_name,
                to_char(d.creation_date, 'DD.MM.YYYY') AS creation_date,
                e.name AS engineer_name,
                d.file_path
            FROM
                internal_documents d
            JOIN
                engineers e ON d.responsible = e.engineer_id
            WHERE
                d.internal_document_id = {document_id}
        ''')
        return self.curs.fetchall()

    def get_internal_documents_references(self):
        self.curs.execute('SELECT documentation FROM completed_briefings')
        data = self.curs.fetchall()
        self.curs.execute('SELECT documentation FROM planned_briefings')
        data = list(data + self.curs.fetchall())
        self.curs.execute('SELECT documentation FROM medical_examinations')
        data = list(data + self.curs.fetchall())
        self.curs.execute('SELECT documentation FROM examinations')
        data = list(data + self.curs.fetchall())
        return list(set(row[0] for row in data))

    def search_internal_documents(self, data):
        self.curs.execute(f'''
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
            WHERE
                d.name LIKE '%{data['name']}%'
                AND d.creation_date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
                AND e.name LIKE '%{data['responsible']}%'
        ''')
        return self.curs.fetchall()

    def insert_internal_document(self, data):
        self.curs.execute(f'''
            INSERT INTO internal_documents(name, creation_date, responsible, file_path)
            VALUES ('{data['name']}', DATE'{data['date']}', {data['responsible']}, '{data['file_path']}')
        ''')

    def update_internal_document(self, data, document_id):
        self.curs.execute(f'''
            UPDATE internal_documents
            SET name = '{(data['name'])}', creation_date = DATE'{(data['date'])}',
            responsible = {(data['responsible'])}, file_path = '{data['file_path']}'
            WHERE internal_document_id = {document_id}
        ''')

    def delete_from_internal_documents(self, document_id):
        self.curs.execute(f'DELETE FROM internal_documents WHERE internal_document_id = {document_id}')

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

    def get_rooms_references(self):
        self.curs.execute('SELECT location FROM equipment')
        return list(set(row[0] for row in self.curs.fetchall()))

    def search_rooms(self, data):
        self.curs.execute(f'''
            SELECT
                r.room_id, 
                r.name AS room_name,
                r.state,
                to_char(r.check_date, 'DD.MM.YYYY') AS check_date,
                e.name AS responsible    
            FROM 
                rooms r
            JOIN 
                engineers e ON r.responsible = e.engineer_id
            WHERE
                r.name LIKE '%{(data['name'])}%'
                AND r.state LIKE '%{(data['state'])}%'
                AND r.check_date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
                AND e.name LIKE '%{(data['responsible'])}%'
        ''')
        return self.curs.fetchall()

    def insert_room(self, data):
        request = (f"INSERT INTO rooms(name, state, check_date, responsible) VALUES ('{(data[0])}',"
                   f" '{(data[1])}', DATE'{(data[2])}', {(data[3])})")
        print(request)
        self.curs.execute(request)

    def update_room(self, room_id, data):
        self.curs.execute(f'''
            UPDATE rooms
            SET name = '{(data[0])}', state = '{(data[1])}', check_date = DATE'{(data[2])}', responsible = {(data[3])}
            WHERE room_id = {room_id}
            ''')

    def delete_from_rooms(self, room_id):
        self.curs.execute('DELETE FROM rooms WHERE room_id = ' + room_id)

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

    def get_planned_briefing_by_id(self, briefing_id):
        self.curs.execute(f'''
            SELECT
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
            WHERE
                b.planned_briefing_id = {briefing_id}
        ''')
        return self.curs.fetchall()

    def search_planned_briefings(self, data):
        self.curs.execute(f'''
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
            WHERE
                b.name LIKE '%{(data['name'])}%'
                AND b.topic LIKE '%{(data['topic'])}%'
                AND b.planned_date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
                AND e.name LIKE '%{(data['responsible'])}%'
        ''')
        return self.curs.fetchall()

    def insert_planned_briefing(self, data):
        if len(data) == 5:
            request = (f"INSERT INTO planned_briefings(name, topic, planned_date, responsible, documentation) "
                       f"VALUES ('{data[0]}', '{data[1]}', DATE'{data[2]}', {(data[3])}, {(data[4])})")
        else:
            request = (f"INSERT INTO planned_briefings(name, topic, planned_date, responsible) "
                       f"VALUES ('{data[0]}', '{data[1]}', DATE'{data[2]}', {(data[3])})")
        print(request)
        self.curs.execute(request)

    def update_planned_briefing(self, data, briefing_id):
        if len(data) == 5:
            self.curs.execute(f'''
                        UPDATE planned_briefings
                        SET name = '{(data[0])}', topic = '{(data[1])}', planned_date = DATE'{(data[2])}',
                        responsible = {(data[3])}, documentation = {(data[4])}
                        WHERE planned_briefing_id = {briefing_id}
            ''')
        else:
            self.curs.execute(f'''
                        UPDATE planned_briefings
                        SET name = '{(data[0])}', topic = '{(data[1])}', planned_date = DATE'{(data[2])}',
                        responsible = {(data[3])}, documentation = NULL
                        WHERE planned_briefing_id = {briefing_id}
                        ''')

    def delete_from_planned_briefings(self, briefing_id):
        self.curs.execute(f'DELETE FROM planned_briefings WHERE planned_briefing_id = {briefing_id}')

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

    def get_completed_briefing_by_id(self, briefing_id):
        self.curs.execute(f'''
            SELECT
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
            WHERE
                b.completed_briefing_id = {briefing_id}
        ''')
        return self.curs.fetchall()

    def get_completed_briefings_references(self):
        self.curs.execute('SELECT by_briefing FROM employees')
        return list(set(row[0] for row in self.curs.fetchall()))

    def search_completed_briefings(self, data):
        self.curs.execute(f'''
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
            WHERE
                b.name LIKE '%{(data['name'])}%'
                AND b.topic LIKE '%{(data['topic'])}%'
                AND b.completion_date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
                AND e.name LIKE '%{(data['responsible'])}%'  
        ''')
        return self.curs.fetchall()

    def insert_completed_briefing(self, data):
        if len(data) == 5:
            request = (f"INSERT INTO completed_briefings(name, topic, completion_date, responsible, documentation) "
                       f"VALUES ('{data[0]}', '{data[1]}', DATE'{data[2]}', {(data[3])}, {(data[4])})")
        else:
            request = (f"INSERT INTO completed_briefings(name, topic, completion_date, responsible) "
                       f"VALUES ('{data[0]}', '{data[1]}', DATE'{data[2]}', {(data[3])})")
        print(request)
        self.curs.execute(request)

    def update_completed_briefing(self, data, briefing_id):
        if len(data) == 5:
            self.curs.execute(f'''
                        UPDATE completed_briefings
                        SET name = '{(data[0])}', topic = '{(data[1])}', completion_date = DATE'{(data[2])}',
                        responsible = {(data[3])}, documentation = {(data[4])}
                        WHERE completed_briefing_id = {briefing_id}
            ''')
        else:
            self.curs.execute(f'''
                        UPDATE completed_briefings
                        SET name = '{(data[0])}', topic = '{(data[1])}', completion_date = DATE'{(data[2])}',
                        responsible = {(data[3])}, documentation = NULL
                        WHERE completed_briefing_id = {briefing_id}
            ''')

    def delete_from_completed_briefings(self, briefing_id):
        self.curs.execute(f'DELETE FROM completed_briefings WHERE completed_briefing_id = {briefing_id}')

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

    def get_examination_by_id(self, examination_id):
        self.curs.execute(f'''
            SELECT
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
            WHERE
                e.examination_id = {examination_id} 
        ''')
        return self.curs.fetchall()

    def get_examinations_references(self):
        self.curs.execute('SELECT examination FROM employees')
        return list(set(row[0] for row in self.curs.fetchall()))

    def search_examinations(self, data):
        self.curs.execute(f'''
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
            WHERE
                e.name LIKE '%{data['name']}%'
                AND e.date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
                AND eng.name LIKE '%{data['responsible']}%'
                AND e.results LIKE '%{data['results']}%'
        ''')
        return self.curs.fetchall()

    def insert_examination(self, data):
        self.curs.execute(f'''
            INSERT INTO examinations(name, date, responsible, results, documentation)
            VALUES ('{data['name']}', DATE'{data['date']}', {data['responsible']},
            '{data['results']}', {data['document']})
        ''')

    def update_examination(self, data, examination_id):
        self.curs.execute(f'''
            UPDATE examinations
            SET name = '{data['name']}', date = DATE'{data['date']}', responsible = {data['responsible']},
            results = '{data['results']}', documentation = {data['document']}
            WHERE examination_id = {examination_id}
        ''')

    def delete_from_examinations(self, examination_id):
        self.curs.execute(f'DELETE FROM examinations WHERE examination_id = {examination_id}')

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

    def get_med_examination_by_id(self, examination_id):
        self.curs.execute(f'''
            SELECT
                e.name,
                to_char(e.date, 'DD.MM.YYYY') AS date,
                e.results,
                d.file_path
            FROM
                medical_examinations e
            JOIN
                internal_documents d ON e.documentation = d.internal_document_id
            WHERE
                e.medical_examination_id = {examination_id}
        ''')
        return self.curs.fetchall()

    def get_med_examinations_references(self):
        self.curs.execute('SELECT med_examination FROM employees')
        return list(set(row[0] for row in self.curs.fetchall()))

    def search_med_examinations(self, data):
        self.curs.execute(f'''
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
            WHERE
                e.name LIKE '%{data['name']}%'
                AND e.date BETWEEN '{(data['date_from'])}' AND '{(data['date_to'])}'
                AND e.results LIKE '%{data['results']}%'
        ''')
        return self.curs.fetchall()

    def insert_med_examination(self, data):
        self.curs.execute(f'''
                    INSERT INTO medical_examinations(name, date, results, documentation)
                    VALUES ('{data['name']}', DATE'{data['date']}',
                    '{data['results']}', {data['document']})
                ''')

    def update_med_examination(self, data, examination_id):
        self.curs.execute(f'''
                    UPDATE medical_examinations
                    SET name = '{data['name']}', date = DATE'{data['date']}',
                    results = '{data['results']}', documentation = {data['document']}
                    WHERE medical_examination_id = {examination_id}
                ''')

    def delete_from_med_examinations(self, examination_id):
        self.curs.execute(f'DELETE FROM medical_examinations WHERE medical_examination_id = {examination_id}')

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

    def get_employees_references(self):
        self.curs.execute('SELECT by FROM complaints')
        data = self.curs.fetchall()
        self.curs.execute('SELECT participant FROM incidents')
        data = list(data + self.curs.fetchall())
        return list(set(row[0] for row in data))

    def search_employees(self, data):
        request = f'''
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
            WHERE 
                e.name LIKE '%{data['name']}%'
                AND e.pasport_series LIKE '%{data['passport_series']}%'
                AND e.pasport_number LIKE '%{data['passport_number']}%'
                AND e.position LIKE '%{data['position']}%' '''
        if data['instruction_result']:
            request += f'''
                AND e.instructed LIKE '%{data['instruction_result']}%' '''
        if data['briefing']:
            request += f'''
                AND b.name LIKE '%{data['briefing']}%' '''
        if data['exam']:
            request += f'''
                AND exam.name LIKE '%{data['exam']}%' '''
        if data['exam_result']:
            request += f'''
                AND exam.results LIKE '%{data['exam_result']}%' '''
        if data['medical_exam']:
            request += f'''        
                AND med_exam.name LIKE '%{data['medical_exam']}%' '''
        if data['medical_result']:
            request += f'''
                AND med_exam.results LIKE '%{data['medical_result']}%' '''
        self.curs.execute(request)
        return self.curs.fetchall()

    def insert_employee(self, data):
        request = (f"INSERT INTO employees (name, pasport_series, pasport_number, position,"
                   f"instructed, by_briefing, examination, med_examination) VALUES "
                   f"('{(data['name'])}', '{(data['passport_series'])}', '{(data['passport_number'])}', "
                   f"'{(data['position'])}', '{(data['instruction_result'])}', "
                   f"{(data['briefing'] if data['briefing'] else 'NULL')}, "
                   f"{(data['exam'] if data['exam'] else 'NULL')}, "
                   f"{(data['medical_exam'] if data['medical_exam'] else 'NULL')})")
        print(request)
        self.curs.execute(request)

    def update_employee(self, data, employee_id):
        self.curs.execute(f'''
            UPDATE employees
            SET name = '{data['name']}', pasport_series = '{data['passport_series']}',
            pasport_number = '{data['passport_number']}', position = '{data['position']}',
            instructed = '{data['instruction_result']}',
            by_briefing = {(data['briefing'] if data['briefing'] else 'NULL')},
            examination = {(data['exam'] if data['exam'] else 'NULL')},
            med_examination = {(data['medical_exam'] if data['medical_exam'] else 'NULL')}
            WHERE employee_id = {employee_id}
        ''')

    def delete_from_employees(self, employee_id):
        self.curs.execute(f'DELETE FROM employees WHERE employee_id = {employee_id}')

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
    # Тестирование Singleton
    db1 = DataBase()
    db2 = DataBase()
    print(db1 is db2)  # Должно вывести True - это один и тот же объект

    print(db1.get_med_examinations_references())
