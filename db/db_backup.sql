--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: complaints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complaints (
    complaint_id integer NOT NULL,
    by integer NOT NULL,
    content text NOT NULL,
    date date NOT NULL,
    status character varying(32) NOT NULL,
    responsible integer NOT NULL
);


ALTER TABLE public.complaints OWNER TO postgres;

--
-- Name: completed_briefings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.completed_briefings (
    completed_briefing_id integer NOT NULL,
    name text NOT NULL,
    topic text NOT NULL,
    completion_date date NOT NULL,
    responsible integer NOT NULL,
    documentation integer
);


ALTER TABLE public.completed_briefings OWNER TO postgres;

--
-- Name: completed_briefings_completed_briefing_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.completed_briefings ALTER COLUMN completed_briefing_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.completed_briefings_completed_briefing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: regulatory_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.regulatory_documents (
    document_id integer NOT NULL,
    name text NOT NULL,
    url text NOT NULL,
    creation_date date NOT NULL
);


ALTER TABLE public.regulatory_documents OWNER TO postgres;

--
-- Name: documents_document_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.regulatory_documents ALTER COLUMN document_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.documents_document_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employee_complaints_employee_complaint_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.complaints ALTER COLUMN complaint_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.employee_complaints_employee_complaint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    employee_id integer NOT NULL,
    name character varying(128) NOT NULL,
    pasport_series character(5) NOT NULL,
    pasport_number character(6) NOT NULL,
    "position" character varying(128) NOT NULL,
    instructed character varying(32),
    by_briefing integer,
    examination integer,
    med_examination integer
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.employees ALTER COLUMN employee_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.employees_employee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: engineers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.engineers (
    engineer_id integer NOT NULL,
    name character varying(128) NOT NULL,
    password character varying(128) NOT NULL
);


ALTER TABLE public.engineers OWNER TO postgres;

--
-- Name: engineers_engineer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.engineers ALTER COLUMN engineer_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.engineers_engineer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: equipment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.equipment (
    equipment_id integer NOT NULL,
    name text NOT NULL,
    location integer NOT NULL,
    supplier text NOT NULL,
    manufacture_date date NOT NULL,
    sell_by_date date NOT NULL,
    responsible integer NOT NULL
);


ALTER TABLE public.equipment OWNER TO postgres;

--
-- Name: examinations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.examinations (
    examination_id integer NOT NULL,
    date date NOT NULL,
    responsible integer NOT NULL,
    results character varying(32) NOT NULL,
    documentation integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.examinations OWNER TO postgres;

--
-- Name: examinations_examination_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.examinations ALTER COLUMN examination_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.examinations_examination_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: incidents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.incidents (
    incident_id integer NOT NULL,
    content text NOT NULL,
    date date NOT NULL,
    responsible integer NOT NULL,
    participant integer,
    proof_path text
);


ALTER TABLE public.incidents OWNER TO postgres;

--
-- Name: incidents_incident_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.incidents ALTER COLUMN incident_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.incidents_incident_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: internal_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.internal_documents (
    internal_document_id integer NOT NULL,
    name text NOT NULL,
    file_path text NOT NULL,
    creation_date date NOT NULL,
    responsible integer NOT NULL
);


ALTER TABLE public.internal_documents OWNER TO postgres;

--
-- Name: internal documents_internal_document_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.internal_documents ALTER COLUMN internal_document_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."internal documents_internal_document_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: medical_examinations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medical_examinations (
    medical_examination_id integer NOT NULL,
    date date NOT NULL,
    documentation integer NOT NULL,
    results character varying(16) NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.medical_examinations OWNER TO postgres;

--
-- Name: medical_examinations_medical_examination_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.medical_examinations ALTER COLUMN medical_examination_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.medical_examinations_medical_examination_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: planned_briefings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planned_briefings (
    planned_briefing_id integer NOT NULL,
    name text NOT NULL,
    topic text NOT NULL,
    planned_date date NOT NULL,
    responsible integer NOT NULL,
    documentation integer
);


ALTER TABLE public.planned_briefings OWNER TO postgres;

--
-- Name: planned_briefings_planned_briefing_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.planned_briefings ALTER COLUMN planned_briefing_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.planned_briefings_planned_briefing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ppe_equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.equipment ALTER COLUMN equipment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ppe_equipment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    room_id integer NOT NULL,
    name character varying(32) NOT NULL,
    state character varying(16) NOT NULL,
    responsible integer NOT NULL,
    check_date date NOT NULL
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- Name: rooms_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.rooms ALTER COLUMN room_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.rooms_room_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: complaints; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complaints (complaint_id, by, content, date, status, responsible) FROM stdin;
1	1	Не работает третья электроустановка в ауд. 3-317	2025-05-25	на рассмотрении	2
2	2	Осыпается потолок в ауд. 3-107	2025-03-17	устранено	4
\.


--
-- Data for Name: completed_briefings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.completed_briefings (completed_briefing_id, name, topic, completion_date, responsible, documentation) FROM stdin;
1	Инструктаж на рабочем месте ауд. 3-307	ТБ на рабочем месте	2024-12-21	2	\N
2	Инструктаж на рабочем месте ауд. 3-307	ТБ на рабочем месте	2024-12-21	2	1
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (employee_id, name, pasport_series, pasport_number, "position", instructed, by_briefing, examination, med_examination) FROM stdin;
1	Антонов Илья Александрович	12 34	123456	преподаватель	проинструктирован	1	\N	\N
2	Кодиров Азиз Абдуманонович	13 31	345090	преподаватель	проинструктирован	1	\N	\N
3	Петров Александр Андреевич	34 78	630716	аспирант	\N	\N	\N	\N
4	Петров Петр Петрович	63 21	734012	преподаватель	проинструктирован	2	5	5
5	Сергеев Сергей Сергеевич	28 16	730617	аспирант	\N	\N	6	\N
6	Иванов Иван Иванович	52 87	007172	преподаватель	проинструктирован	1	\N	6
\.


--
-- Data for Name: engineers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.engineers (engineer_id, name, password) FROM stdin;
1	admin	1234
2	Кудряшев Дмитрий Алексеевич	qwerty
4	Иванов Иван Иванович	wasd
\.


--
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.equipment (equipment_id, name, location, supplier, manufacture_date, sell_by_date, responsible) FROM stdin;
1	огнетушитель	1	ОАО «Огнетушители»	2024-08-12	2028-08-12	4
2	электроустановка	1	ОАО «Электроустановки»	2018-08-12	2038-08-12	2
\.


--
-- Data for Name: examinations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.examinations (examination_id, date, responsible, results, documentation, name) FROM stdin;
5	2025-07-16	4	допущен	1	Экзамен на допуск Петрова П.П. от 16.07.2025
6	2022-08-25	2	не допущен	2	Экзамен на допуск Сергеева С.С. от 25.08.2022
\.


--
-- Data for Name: incidents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.incidents (incident_id, content, date, responsible, participant, proof_path) FROM stdin;
1	Задымилась розетка в аудитории 3-110	2025-05-25	4	1	C:\\Projects\\Safety_engineer_information_system\\incidents_proof\\1.jpg
2	Протекает потолок в аудитории 3-420	2024-11-12	2	\N	\N
\.


--
-- Data for Name: internal_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.internal_documents (internal_document_id, name, file_path, creation_date, responsible) FROM stdin;
1	Приказ от 26.02.2022 № 28 «О назначении отв.лиц за пожарную безопасность в МАИ»	C:\\Projects\\Safety_engineer_information_system\\internal_documents\\28-ot-26.02.2022_o-naznachenii-otv.lits-za-pozharnuyu-bezopasnost-v-MAI_kontrol-A.P.Vysikantsev.pdf	2022-02-26	2
2	Приказ от 23.09.2020 № 338 «Об утв.инструкции по пожарной безопасности»	C:\\Projects\\Safety_engineer_information_system\\internal_documents\\338-ot-23.09.2020_ob-utv.instruktsii-po-pozharnoy-bezopasnosti_kontrol-A.P.Vysikantsev.pdf	2020-09-23	2
\.


--
-- Data for Name: medical_examinations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medical_examinations (medical_examination_id, date, documentation, results, name) FROM stdin;
4	2022-03-11	2	просрочен	Медосмотр Иванова И.И. от 11.03.2022
5	2025-08-25	1	пройден	Медосмотр Петрова П.П. от 25.08.2022
6	2025-08-25	1	не пройден	Медосмотр Иванова И.И. от 25.08.2025
7	2025-08-25	1	не пройден	Медосмотр Иванова И.И. от 25.08.2025
\.


--
-- Data for Name: planned_briefings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planned_briefings (planned_briefing_id, name, topic, planned_date, responsible, documentation) FROM stdin;
1	Инструктаж о пожарной безопасности №1	Пожарная безопасность	2025-05-19	2	2
2	Инструктаж по ТБ при использовании спец. оборудования №1	ТБ на рабочем месте	2026-10-01	2	\N
\.


--
-- Data for Name: regulatory_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.regulatory_documents (document_id, name, url, creation_date) FROM stdin;
1	Положение о службе радиационной безопасности Управления кадрового, правового и документационного обеспечения (СРБ УКПДО)	https://mai.ru/upload/iblock/e8c/advk68se0a1ci51qbpn7wdb4iwrm91ye/524-ot-03.12.2021_ob-utv.polozheniya-o-Sluzhbe-radiatsionnoy-bezopasnosti_kontrol-A.E.Sorokin.pdf	2021-03-12
2	Приказ от 22.10.2021 № 459 «Об утверждении Сборника инструкций по охране труда выпуск № 6»	https://mai.ru/upload/iblock/d75/b86fzkrrr5n5gqwfz2iatvf6a37smuj5/459-ot-22.10.2021_ob-utverzhdenii-Sbornika-instruktsiy-po-okhrane-truda-vypusk-_-6-Kontrol-M.V.Kalinin_compressed.pdf	2021-10-22
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (room_id, name, state, responsible, check_date) FROM stdin;
1	3-307	удовл.	2	2024-10-30
34	4-109	неудовл.	4	2025-01-28
16	3-309	требует проверки	2	2023-07-17
43	3-311	удовл.	4	2022-04-23
45	3-119	удовл.	2	2023-03-21
46	3-420	требует проверки	4	2025-05-30
\.


--
-- Name: completed_briefings_completed_briefing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.completed_briefings_completed_briefing_id_seq', 8, true);


--
-- Name: documents_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_document_id_seq', 8, true);


--
-- Name: employee_complaints_employee_complaint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employee_complaints_employee_complaint_id_seq', 4, true);


--
-- Name: employees_employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_employee_id_seq', 10, true);


--
-- Name: engineers_engineer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.engineers_engineer_id_seq', 4, true);


--
-- Name: examinations_examination_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.examinations_examination_id_seq', 12, true);


--
-- Name: incidents_incident_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.incidents_incident_id_seq', 6, true);


--
-- Name: internal documents_internal_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."internal documents_internal_document_id_seq"', 5, true);


--
-- Name: medical_examinations_medical_examination_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medical_examinations_medical_examination_id_seq', 9, true);


--
-- Name: planned_briefings_planned_briefing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planned_briefings_planned_briefing_id_seq', 14, true);


--
-- Name: ppe_equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ppe_equipment_id_seq', 4, true);


--
-- Name: rooms_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_room_id_seq', 51, true);


--
-- Name: examinations pk_ examination_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examinations
    ADD CONSTRAINT "pk_ examination_id" PRIMARY KEY (examination_id);


--
-- Name: incidents pk_ incident_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT "pk_ incident_id" PRIMARY KEY (incident_id);


--
-- Name: completed_briefings pk_completed_briefing_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed_briefings
    ADD CONSTRAINT pk_completed_briefing_id PRIMARY KEY (completed_briefing_id);


--
-- Name: regulatory_documents pk_document_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.regulatory_documents
    ADD CONSTRAINT pk_document_id PRIMARY KEY (document_id);


--
-- Name: complaints pk_employee_complaint_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT pk_employee_complaint_id PRIMARY KEY (complaint_id);


--
-- Name: employees pk_employee_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT pk_employee_id PRIMARY KEY (employee_id);


--
-- Name: engineers pk_engineer_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.engineers
    ADD CONSTRAINT pk_engineer_id PRIMARY KEY (engineer_id);


--
-- Name: equipment pk_equipment_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT pk_equipment_id PRIMARY KEY (equipment_id);


--
-- Name: internal_documents pk_internal_document_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.internal_documents
    ADD CONSTRAINT pk_internal_document_id PRIMARY KEY (internal_document_id);


--
-- Name: medical_examinations pk_medical_examination_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_examinations
    ADD CONSTRAINT pk_medical_examination_id PRIMARY KEY (medical_examination_id);


--
-- Name: planned_briefings pk_planned_briefing_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planned_briefings
    ADD CONSTRAINT pk_planned_briefing_id PRIMARY KEY (planned_briefing_id);


--
-- Name: rooms pk_room_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT pk_room_id PRIMARY KEY (room_id);


--
-- Name: fki_k; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_k ON public.rooms USING btree (responsible);


--
-- Name: complaints fk_by_employee; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT fk_by_employee FOREIGN KEY (by) REFERENCES public.employees(employee_id);


--
-- Name: completed_briefings fk_com_br_documentation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed_briefings
    ADD CONSTRAINT fk_com_br_documentation FOREIGN KEY (documentation) REFERENCES public.internal_documents(internal_document_id);


--
-- Name: completed_briefings fk_com_br_responsible; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.completed_briefings
    ADD CONSTRAINT fk_com_br_responsible FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- Name: complaints fk_complaint_responsible; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT fk_complaint_responsible FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- Name: planned_briefings fk_documentation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planned_briefings
    ADD CONSTRAINT fk_documentation FOREIGN KEY (documentation) REFERENCES public.internal_documents(internal_document_id) NOT VALID;


--
-- Name: employees fk_employee_briefing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_employee_briefing FOREIGN KEY (by_briefing) REFERENCES public.completed_briefings(completed_briefing_id);


--
-- Name: rooms fk_engineer_name; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_engineer_name FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id) NOT VALID;


--
-- Name: examinations fk_exam_documentation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examinations
    ADD CONSTRAINT fk_exam_documentation FOREIGN KEY (documentation) REFERENCES public.internal_documents(internal_document_id);


--
-- Name: examinations fk_exam_responsible; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examinations
    ADD CONSTRAINT fk_exam_responsible FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- Name: employees fk_examination; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_examination FOREIGN KEY (examination) REFERENCES public.examinations(examination_id) NOT VALID;


--
-- Name: incidents fk_incident_responsible; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT fk_incident_responsible FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- Name: internal_documents fk_it_doc_responsible; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.internal_documents
    ADD CONSTRAINT fk_it_doc_responsible FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- Name: equipment fk_location; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT fk_location FOREIGN KEY (location) REFERENCES public.rooms(room_id);


--
-- Name: medical_examinations fk_med_documentation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_examinations
    ADD CONSTRAINT fk_med_documentation FOREIGN KEY (documentation) REFERENCES public.internal_documents(internal_document_id);


--
-- Name: employees fk_med_examination; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT fk_med_examination FOREIGN KEY (med_examination) REFERENCES public.medical_examinations(medical_examination_id) NOT VALID;


--
-- Name: incidents fk_participant; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT fk_participant FOREIGN KEY (participant) REFERENCES public.employees(employee_id);


--
-- Name: planned_briefings fk_pl_br_responsible; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planned_briefings
    ADD CONSTRAINT fk_pl_br_responsible FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- Name: equipment fk_responsible_ppe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT fk_responsible_ppe FOREIGN KEY (responsible) REFERENCES public.engineers(engineer_id);


--
-- PostgreSQL database dump complete
--

