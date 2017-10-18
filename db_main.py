import sqlite3  # A Python Package for sqlite3 , pip3 install sqlite3


# Before doing that make sure you have sqlite browser downloaded as well
# This is a lite database for 1- 10's of GBs( I HAVE WORKED WITH 5.7 GB with it :))


class DB:
    connection = None  # Global Variables which will be used when the object has been Created !
    cursor = None  # Global Cursor will be used when the object has been created !

    def __init__(self):
        self.connection = sqlite3.connect("Masterdatabase.sqlite3")  # Connecting  to the database
        # If the database doesn't exits it will create one of its own named Master database
        self.cursor = self.connection.cursor()  # This is a cursor which will be used to execute each and every query
        self.create_tables()
        # self.delete_ALL() # Deleting all the tables

    # The below Function will Create the tables , if the tables if not exists.
    # The queries in python are writted in the Cursor with triple single or double quotes
    # After Executing each query keep in mind at the end to commit all the things (so that they may go from temporary -> database storage)

    def create_tables(self):
        # Below is the Filter Qualification Table  , which will have the filters of QUALIFICATION NAMES ONLY
        # E.G BACHELORS IN COMPUTER SCIENCE or MASTERS or others
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILTER_QUALIFICATION
(FQ_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FQ_NAME TEXT NOT NULL)''')
        # Below is the table for the Skills , same filter purpose as Above although
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILTER_SKILL
(FS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FS_NAME TEXT NOT NULL)''')
        # Filter Certification will hold the Filters on the Certification names
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILTER_CERTIFICATION
(FC_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FC_NAME TEXT NOT NULL)''')
        # Filter Education will hold the Filters on the Education names as well
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILTER_EDUCATION
(FE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FE_NAME TEXT NOT NULL)''')
        # Filter Certification will hold the Filters on the Certifications
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILTER_WORK_EXPERIENCE
(FW_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FW_Name TEXT UNIQUE NOT NULL)''')
        # This will hold the doc file name with the auto incremented integer
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DOC
(DOC_ID INTEGER PRIMARY KEY AUTOINCREMENT,
DOC_LOCATION TEXT UNIQUE NOT NULL)''')
        # This will hold the PDF file name , same with the autoincrement integer
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS PDF
(PDF_ID INTEGER PRIMARY KEY AUTOINCREMENT,
PDF_Location TEXT UNIQUE NOT NULL)''')
        # This will be the File General (.txt) Files with their location as well as the other things as wel
        # Such as File name , File location ,  Extracted from Document or From PDF ?
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILE_
(F_ID INTEGER PRIMARY KEY AUTOINCREMENT,
 F_NAME  TEXT UNIQUE NOT NULL,
F_LOC TEXT UNIQUE NOT NULL,
DOC_ID_FK INTEGER,
PDF_ID_FK INTEGER,
FOREIGN KEY(DOC_ID_FK) REFERENCES DOC(DOC_ID),
FOREIGN KEY(PDF_ID_FK) REFERENCES PDF(PDF_ID))''')
        # THE FILE TABLE TAKES THE FOREIGN KEYS FOM THE PDF AND THE DOC TABLE (TO SPECIFY WHICH TYPE AND STUFF )
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS FILE_DATA
(FD_ID INTEGER PRIMARY KEY AUTOINCREMENT,
F_ID_FK INTEGER,
QUALIFICATION TEXT,
EDUCATION TEXT,
SKILL TEXT,
CERTIFICATION TEXT,
WORK_EXPERIENCE TEXT,

FOREIGN KEY (F_ID_FK) REFERENCES  FILE_(F_ID))
''')
        # Creating the table Brief Qualificaion
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BRIEF_QUALIFICATION
(BQ_ID INTEGER PRIMARY KEY AUTOINCREMENT,
BQ_DATA TEXT,
FQ_ID_FK INTEGER,
FOREIGN KEY (FQ_ID_FK) REFERENCES FILTER_QUALIFICATION(FQ_ID)
)''')
        # Creating the table of BRIEF SKILL as per ERD
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BRIEF_SKILL
(BS_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
BS_DATA TEXT,
FS_ID_FK INTEGER,
FOREIGN KEY (FS_ID_FK) REFERENCES FILTER_SKILL(FS_ID)
)''')
        # Brief Certification !
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BRIEF_CERTIFICATION
(BC_ID INTEGER PRIMARY KEY  AUTOINCREMENT,
BC_DATA TEXT,
FC_ID_FK INTEGER,
FOREIGN KEY (FC_ID_FK) REFERENCES FILTER_CERTIFICATION(FC_ID)
)''')
        # Brief Education
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BRIEF_EDUCATION
(BE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
BE_DATA TEXT,
FE_ID_FK INTEGER,
FOREIGN KEY (FE_ID_FK) REFERENCES FILTER_EDUCATION(FE_ID)
)''')
        # WORK EXPERIENCE BRIEF , KEEP IN MIND THAT THESE DATA WILL BE INSERTED THROUGH THE ITEM
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS BRIEF_WORK_EXPERIENCE
(BW_ID INTEGER PRIMARY KEY AUTOINCREMENT,
BW_DATA TEXT,
FW_ID_FK INTEGER,
FOREIGN KEY (FW_ID_FK) REFERENCES FILTER_WORK_EXPERIENCE(FW_ID)

)''')
        # RESOLVED ENTITY FOR THE RESOLVED QUALIFICATION
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS RES_QUA
(RQ_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
FD_ID_FK INTEGER,
BQ_ID_FK INTEGER,
FOREIGN KEY (FD_ID_FK) REFERENCES FILE_DATA(FD_ID),
FOREIGN KEY(BQ_ID_FK) REFERENCES BRIEF_QUALIFICATION(BQ_ID)
)''')
        # RESOLE
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS RES_SKILL
(RS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FD_ID_FK INTEGER,
BS_ID_FK INTEGER,
FOREIGN KEY (FD_ID_FK) REFERENCES FILE_DATA(FD_ID),
FOREIGN KEY (BS_ID_FK) REFERENCES BRIEF_SKILL(BS_ID)
)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS  RES_CERTIFICATION
(RC_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FD_ID_FK INTEGER,
BC_ID_FK INTEGER,
FOREIGN KEY (FD_ID_FK) REFERENCES FILE_DATA(FD_ID),
FOREIGN KEY (BC_ID_FK) REFERENCES BRIEF_CERTIFICATION(BC_ID)
)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS RES_EDUCATION
(RE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FD_ID_FK INTEGER,
BE_ID_FK INTEGER,
FOREIGN KEY (FD_ID_FK) REFERENCES FILE_DATA(FD_ID),
FOREIGN KEY (BE_ID_FK) REFERENCES BRIEF_EDUCATION(BE_ID)
)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS RES_WORK_EXPERIENCE
(RW_ID INTEGER PRIMARY KEY AUTOINCREMENT,
FD_ID_FK INTEGER,
BW_ID_FK INTEGER,
FOREIGN KEY (FD_ID_FK) REFERENCES FILE_DATA(FD_ID),
FOREIGN KEY (BW_ID_FK) REFERENCES BRIEF_WORK_EXPERIENCE(BW_ID)
)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS JOB
( JOB_ID INTEGER PRIMARY KEY AUTOINCREMENT,
JOB_NAME TEXT,
JOB_QUALIFICATION TEXT,
JOB_SKILL TEXT,
JOB_CERTIFICATION TEXT,
JOB_EDUCATION TEXT,
JOB_WORK_EXPERIENCE TEXT
)''')

    # Deleting all the tabels from the database
    def delete_ALL(self):
        self.cursor.executescript('''

DROP TABLE IF EXISTS BRIEF_QUALIFICATION;
DROP TABLE IF EXISTS BRIEF_SKILLS;
DROP TABLE IF EXISTS BRIEF_CERTIFICATION;
DROP TABLE IF EXISTS BRIEF_EDUCATION;
DROP TABLE IF EXISTS BRIEF_WORK_EXPERIENCE;
DROP TABLE IF EXISTS RES_QUALIFICATION;
DROP TABLE IF EXISTS RES_SKILL;
DROP TABLE IF EXISTS RES_EDUCATION;
DROP TABLE IF EXISTS RES_CERTIFICATION;
DROP TABLE IF EXISTS RES_WORK_EXPERIENCE;
DROP TABLE IF EXISTS FILTER_QUALIFICATION;
DROP TABLE IF EXISTS FILTER_SKILL;
DROP TABLE IF EXISTS FILTER_CERTIFICATION;
DROP TABLE IF EXISTS FILTER_EDUCATION;
DROP TABLE IF EXISTS FILTER_WORK_EXPERIENCE;
DROP TABLE IF EXISTS FILE_DATA;
DROP TABLE IF EXISTS FILE_;
DROP TABLE IF EXISTS DOC;
DROP TABLE IF EXISTS PDF;
''')
        print("ALL TABLES HAVE BEEN DROPPED!")

    def insert_into_filter_qualification(self, FQ_NAME):
        self.cursor.execute('''INSERT INTO FILTER_QUALIFICATION(FQ_NAME) VALUES (?)''', (FQ_NAME,))
        self.connection.commit()  # Commits the changes

    def insert_into_filter_skill(self, FS_NAME):
        # Keep in mind that the store parameter if single has a comma at the end
        # Because its inserted in the form of a set
        self.cursor.execute('''INSERT INTO FILTER_SKILL(FS_NAME) VALUES (?)''', (FS_NAME,))
        self.connection.commit()

    # TO insert into filter certification
    def insert_into_filter_certification(self, FC_NAME):
        self.cursor.execute('''INSERT INTO FILTER_CERTIFICATION(FC_NAME) VALUES (?)''', (FC_NAME,))
        self.connection.commit()  # Commuits or saves the changes in the database

    # To insert into the education filter as per DATABASE SCHEME

    def insert_into_filter_education(self, FE_NAME):
        self.cursor.execute('''INSERT INTO FILTER_EDUCATION(FE_NAME) VALUES (?)''', (FE_NAME,))
        self.connection.commit()

    # To insert into the filter work experience table

    def insert_into_filter_work_experience(self, FW_NAME):
        self.cursor.execute('''INSERT INTO FILTER_WORK_EXPERIENCE(FW_NAME) VALUES (?)''', (FW_NAME,))
        self.connection.commit()

    # Inserting in to the documents table for the specified value
    def insert_into_doc(self, DOC_LOCATION):
        self.cursor.execute('''INSERT INTO DOC(DOC_LOCATION) VALUES (?)''', (DOC_LOCATION,))
        self.connection.commit()  # Commits  the changes !

    def insert_into_pdf(self, PDF_LOCATION):
        self.cursor.execute('''INSERT INTO PDF(PDF_LOCATION) VALUES (?)''', (PDF_LOCATION,))
        self.connection.commit()  # Commits the changes

    def insert_into_file_(self, FILENAME, FILE_LOCATION, DOC_ID="", PDF_ID=""):
        self.cursor.execute('''INSERT INTO FILE_(F_NAME,F_LOC,DOC_ID_FK,PDF_ID_FK)
VALUES (?,?,?,?)''', (FILENAME, FILE_LOCATION, DOC_ID, PDF_ID))
        self.connection.commit()  # Commits the changes in the database

    # The below function will be used to add in the manual data in the database and the other things
    # The File ID would be the integer representing the FILE LOCATION.
    def insert_into_file_data(self, FILE_ID, QUALIFICATION, EDUCATION, SKILL, CERTIFICATION, WORKEXPERIENCE):
        self.cursor.execute('''INSERT INTO FILE_DATA(F_ID_FK,QUALIFICATION,EDUCATION, SKILL, CERTIFICATION, WORK_EXPERIENCE)
VALUES (?,?,?,?,?,?)''', (FILE_ID, QUALIFICATION, EDUCATION, SKILL, CERTIFICATION, WORKEXPERIENCE))
        self.connection.commit()

    # Inserting  into Brief qualification , dependent on the filter qualifcication as well.

    def insert_into_brief_qualification(self, BQ_DATA, FQ_ID):
        self.cursor.execute('''INSERT INTO BRIEF_QUALIFICATION(BQ_DATA, FQ_ID_FK) VALUES (?,?)''', (BQ_DATA, FQ_ID))
        self.connection.commit()  # commits the changes

    # Accepts he Brief Skills data and the ID in form of integer from the Filter skill
    def insert_into_brief_skill(self, BS_DATA, FS_ID):
        # INserting in to the table of skills
        self.cursor.execute('''INSERT INTO BRIEF_SKILL(BS_DATA,FS_NAME) VALUES (?,?)''', (BS_DATA, FS_ID))
        self.connection.commit()  # Commits the changes

    # Accepts the Brief certification data and the Foreign ID --> Representing the Filter Certification ID


    def insert_into_brief_certification(self, BC_DATA, FC_ID):
        self.cursor.execute('''INSERT INTO BRIEF_CERTIFICATION(BC_DATA,FC_ID_FK) VALUES (?,?)''', (BC_DATA, FC_ID))
        self.connection.commit()

    # inserting into brief education

    def insert_into_brief_education(self, BE_DATA, FE_ID):
        self.cursor.execute('''INSERT INTO BRIEF_EDUCATION(BE_DATA,FE_ID_FK) VALUES (?,?)''', (BE_DATA, FE_ID))
        self.connection.commit()

    # Accepts the brief work experience

    def insert_into_brief_work_experience(self, BW_DATA, FW_ID):
        # Executing the Cursor and adding in the brief work experience.
        self.cursor.execute('''INSERT INTO BRIEF_WORK_EXPERIENCE(BW_DATA,FW_ID_FK) VALUES (?,?)''', (BW_DATA, FW_ID))
        self.connection.commit()

    # Resolved qualification insertion

    def insert_into_res_qua(self, FD_ID, BQ_ID):
        self.cursor.execute('''INSERT INTO RES_QUA(FD_ID_FK, BQ_ID_FK) VALUES (?,?)''', (FD_ID, BQ_ID))
        self.connection.commit()  # this commits the connection !

    # inserts into resolved skills

    def insert_into_res_skill(self, FD_ID, BS_ID):
        self.cursor.execute('''INSERT INTO RES_SKILL(FD_ID_FK,BS_ID_FK) VALUES (?,?)''', (FD_ID, BS_ID))
        self.connection.commit()  # Commits the changes

    # inserts into the resolved certification
    def insert_into_res_certification(self, FD_ID, BC_ID):
        self.cursor.execute('''INSERT INTO RES_CERTIFICATION(FD_ID_FK,BC_ID_FK) VALUES (?,?)''', (FD_ID, BC_ID))
        self.connection.commit()

    # Inserts into resolved education

    def insert_into_res_education(self, FD_ID, RE_ID):
        self.cursor.execute('''INSERT INTO RES_EDUCATION(FD_ID_FK,BE_ID_FK) VALUES (?,?)''', (FD_ID, RE_ID))
        self.connection.commit()  # Commits the changes

    # Inserts into resolved work experience and the  filedata
    def insert_into_res_work_experience(self, FD_ID, BW_ID):
        self.cursor.execute('''INSERT INTO RES_WORK_EXPERIENCE(FD_ID_FK,BW_ID_FK) VALUES (?,?)''', (FD_ID, BW_ID))
        self.connection.commit()  # Creates the work experience
    # The below adds in the values in the database
    # Inserting into the table for the recriter for the job specificcation
    def insert_into_job(self,job_name, job_qualification, job_skill, job_certification, job_education, job_work_experience):
        self.cursor.execute('''INSERT INTO JOB
(JOB_NAME, JOB_QUALIFICATION,JOB_SKILL,JOB_CERTIFICATION,JOB_EDUCATION,JOB_WORK_EXPERIENCE)
VALUES (?,?,?,?,?,?)''',(job_name , job_qualification,job_skill,job_certification,job_education,job_work_experience))
        self.connection.commit()  # this commits the changes in the database as well
    # gets the id from the brief qualification
    def select_id_from_brief_qualification(self, BQ_NAME):
        self.cursor.execute('''SELECT BQ_ID FROM BRIEF_QUALIFICATION WHERE BQ_DATA = ?''', (BQ_NAME,))
        BQ_ID = self.cursor.fetchone()[0]
        return BQ_ID

    # Gets the id from the Brief skill
    def select_id_from_brief_skill(self, BS_NAME):
        self.cursor.execute('''SELECT BS_ID FROM BRIEF_SKILL WHERE BS_NAME = ?''', (BS_NAME,))
        BS_ID = self.cursor.fetchone()[0]
        return BS_ID

    def select_id_from_brief_certification(self, BC_NAME):
        self.cursor.execute('''SELECT BC_ID FROM BRIEF_CERTIFICATION WHERE BC_DATA = ?''', (BC_NAME,))
        BC_NAME = self.cursor.fetchone()[0]
        return BC_NAME

    def select_id_from_brief_education(self, BE_NAME):
        self.cursor.execute('''SELECT BE_ID FROM BRIEF_EDUCATION WHERE BE_DATA = ?''', (BE_NAME,))
        BE_NAME = self.cursor.fetchone()[0]
        return BE_NAME

    # Returns the id got from the bw_name
    def select_id_from_brief_work_experience(self, bw_name):
        self.cursor.execute('''SELECT BW_ID FROM BRIEF_WORK_EXPERIENCE WHERE BW_DATA = ?''', (bw_name,))
        BW_ID = self.cursor.fetchone()[0]  # The First element from the Fetched DATABASE (1st Value is returned)
        return BW_ID  # returnss the BW ID From the way .

    # Selecting the if from the table pdf , this will also be used as a foreign key in the
    def select_id_from_pdf(self, pdflocation):
        self.cursor.execute('''SELECT PDF_ID FROM PDF WHERE PDF_LOCATION = ?''', (pdflocation,))
        pdf_id = self.cursor.fetchone()[0]  # gets the first most element from the index of the pdf
        return pdf_id

    # Selects the id from the doc data base table , so that later onward it can be used as a foreign key in the places
    def select_id_from_doc(self, doclocation):
        self.cursor.execute('''SELECT DOC_ID FROM DOC WHERE DOC_LOCATION = ?''', (doclocation,))
        doc_id = self.cursor.fetchone()[0]  # Gets the first element for the doc id
        return doc_id  # This returns the doc id to the called function

    # Selects the file id from the FILE_ table , since the queries are getting more complex . !
    def select_id_from_file_(self, filename):
        self.cursor.execute('''SELECT F_ID FROM FILE_ WHERE F_NAME = ?''', (filename,))
        file_id = self.cursor.fetchone()[0]  # Gets the file id from the file table
        return file_id

    def select_id_from_filter_qualification(self, FQ_NAME):
        self.cursor.execute('''SELECT FQ_ID FROM FILTER_QUALIFICATION WHERE FQ_NAME = ? ''', (FQ_NAME,))
        FQ_ID = self.cursor.fetchone()[0]
        return FQ_ID  # Returns to the main filter qualification !

    def select_id_from_filter_skill(self, FS_NAME):
        self.cursor.execute('''SELECT FS_ID FROM FILTER_SKILL WHERE FS_NAME = ?''', (FS_NAME,))
        FS_ID = self.cursor.fetchone()[0]
        return FS_ID  # This returns the FS ID to the main function

    def select_id_from_filter_certification(self, FC_NAME):
        self.cursor.execute('''SELECT FC_ID FROM FILTER_CERTIFICATION WHERE FC_NAME = ?''', (FC_NAME,))
        FC_ID = self.cursor.fetchone()[0]  # Retrieving the indexed  !
        return FC_ID  # Returns the FC_ID to the main function

    def select_id_from_filter_education(self, FE_NAME):
        self.cursor.execute('''SELECT FE_ID FROM FILTER_EDUCATION WHERE FE_NAME = ?''', (FE_NAME,))
        FE_ID = self.cursor.fetchone()[0]  # Gets the first connection
        return FE_ID  # Retus nteh FE_ID
    # Selecting the id from the filter work experience
    def select_id_from_filter_work_experience(self, FW_NAME):
        self.cursor.execute('''SELECT FW_ID FROM FILTER_WORK_EXPERIENCE WHERE FW_NAME = ?''', (FW_NAME,))
        FW_ID = self.cursor.fetchone()[0]
        return FW_ID  # Return to the main function

    def select_id_from_file_data(self,file_id):
        self.cursor.execute('''SELECT FD_ID FROM FILE_DATA WHERE F_ID_FK = ?''', (file_id,))
        FD_ID = self.cursor.fetchone()[0]  # This retrieves the
        return FD_ID  # This rteturns the File data id that is retrieved from the web
    def clear_all_db(self):
        self.cursor.executescript('''
DELETE  FROM BRIEF_QUALIFICATION;
DELETE FROM  BRIEF_SKILLS;
DELETE FROM BRIEF_CERTIFICATION;
DELETE FROM BRIEF_EDUCATION;
DELETE FROM BRIEF_WORK_EXPERIENCE;
DELETE FROM RES_QUALIFICATION;
DELETE FROM RES_SKILL;
DELETE FROM RES_EDUCATION;
DELETE FROM RES_CERTIFICATION;
DELETE FROM RES_WORK_EXPERIENCE;
DELETE FROM FILTER_QUALIFICATION;
DELETE FROM FILTER_SKILL;
DELETE FROM FILTER_CERTIFICATION;
DELETE FROM FILTER_EDUCATION;
DELETE FROM FILTER_WORK_EXPERIENCE;
DELETE FROM FILE_DATA;
DELETE FROM FILE_;
DELETE FROM DOC;
DELETE FROM PDF;
''')
# Deleting all data form the tables , as per specified !


def test():
    db_test = DB()
    db_test.delete_ALL()
    db_test.create_tables()
    # db_test. <-- type in any method here to insert the data

# if __name__ == '__main__':
#    test()  # Calls in the Test function to create the data base
