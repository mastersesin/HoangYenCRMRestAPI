import threading
import time
import pyodbc
class sqlQuery(threading.Thread):
    def __init__(self,**kwargs):
        threading.Thread.__init__(self)
        self.server = '11.11.11.16,9433'
        self.database = 'CRM'
        self.username = 'rk7'
        self.password = 'rk7'
        self.sqlReturn = ''
        self.kwargs = kwargs
    def run(self):
        if self.sqlFunction == 'get_card_info()':
            self.get_card_info()
        else:
            pass
    def get_return_data(self):
        return self.sqlReturn
    def get_card_info(self):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        myfile = cnxn.cursor()
        myfile.execute("""SELECT
                                    CARD_CARDS.CARD_CODE,
                                    CARD_CARDS.PEOPLE_ID,
                                    CARD_PEOPLES.F_NAME,
                                    CARD_PEOPLES.L_NAME,
                                    CARD_PEOPLES.FULL_NAME,
                                    CARD_CARDS.TEXT_PASSWORD,
                                    CARD_PEOPLES.BIRTHDAY,
                                    CARD_PEOPLES.SOURCE,
                                    CARD_PEOPLE_ACCOUNTS.BALANCE
                                    FROM
                                    CARD_CARDS
                                    LEFT JOIN
                                    CARD_PEOPLES
                                    ON
                                    CARD_CARDS.PEOPLE_ID = CARD_PEOPLES.PEOPLE_ID
                                    LEFT JOIN
                                    CARD_PEOPLE_ACCOUNTS
                                    ON
                                    CARD_PEOPLES.PEOPLE_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ID
                                    LEFT JOIN
                                    CARD_ACCOUNT_TYPES
                                    ON
                                    CARD_ACCOUNT_TYPES.ACCOUNT_TYPE_ID = CARD_PEOPLE_ACCOUNTS.ACCOUNT_TYPE_ID
                                    WHERE
                                    CARD_CODE LIKE '6%' AND LEN(CARD_CODE) = 6 AND (CARD_ACCOUNT_TYPES.NAME LIKE 'Tich luy') AND CARD_CODE = {}
                                """.format(self.CardCode))
        records = myfile.fetchall()
        self.sqlReturn = records

    def getCardCodePassWord(self):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        myfile = cnxn.cursor()
        myfile.execute("""select 
                                    CARD_CARDS.CARD_CODE,
                                    CARD_CARDS.TEXT_PASSWORD,
                                    CARD_CARDS.PEOPLE_ID
                                    from CARD_CARDS 
                                    WHERE LEN(CARD_CODE) = 6 AND CARD_CODE = '{}'
                              """.format(self.CardCode))
        records = myfile.fetchall()
        self.sqlReturn = records

    def change_password(self, password):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        myfile = cnxn.cursor()
        myfile.execute("""UPDATE
                                    CARD_CARDS
                                    SET
                                    TEXT_PASSWORD = {1}
                                    WHERE
                                    CARD_CODE = {0}
                              """.format(self.CardCode, password))
        cnxn.commit()

start = time. time()
a = sqlQuery('get_card_info()','601916')
b = sqlQuery('get_card_info()','601959')
a.start()
b.start()
threada = []
threada.append(a)
threada.append(b)
for thread in threada:
    thread.join()
print(a.get_return_data())
print(b.get_return_data())
end = time. time()
print(end - start)