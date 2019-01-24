import threading
import time
import pyodbc
from mainAppFolder.crmapi.functions import handle_datetimeoffset
returnMsgSqlModule = {
    "CmdNotFound": {
        "code": 1,
        "msg": "Command not found or currently not supported."
    },
    "SqlReturn": {
        "code": 2,
        "msg": ""  # Dynamic return
    },
    "ChangePasswordSuccessfully": {
        "code": 3,
        "msg": "Password has change successfully."
    }
}


class sqlQuery(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.kwargs = kwargs
        self.server = '11.11.11.16,9433'
        self.database = 'CRM'
        self.username = 'rk7'
        self.password = 'rk7'
        self.sqlReturn = {}

    def run(self):
        if self.kwargs['cmd'] == 'get_card_info':
            self.get_card_info()
        elif self.kwargs['cmd'] == 'get_cardcode_password':
            self.get_cardcode_password()
        elif self.kwargs['cmd'] == 'change_password':
            self.change_password()
        elif self.kwargs['cmd'] == 'get_transactions':
            self.get_transactions()
        else:
            self.sqlReturn = returnMsgSqlModule['CmdNotFound']

    def get_card_info(self):
        msg = returnMsgSqlModule['SqlReturn']
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password +';MARS_Connection=yes')
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
                                """.format(self.kwargs['cardcode']))
        records = myfile.fetchall()
        msg['msg'] = records
        msg['msg'] = self.kwargs['cardcode']
        self.sqlReturn = msg
        cnxn.close()


    def get_cardcode_password(self):
        msg = returnMsgSqlModule['SqlReturn']
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        myfile = cnxn.cursor()
        myfile.execute("""select 
                                        CARD_CARDS.CARD_CODE,
                                        CARD_CARDS.TEXT_PASSWORD,
                                        CARD_CARDS.PEOPLE_ID
                                        from CARD_CARDS 
                                        WHERE LEN(CARD_CODE) = 6 AND CARD_CODE = '{}'
                                  """.format(self.kwargs['cardcode']))
        records = myfile.fetchall()
        msg['msg'] = records
        self.sqlReturn = msg

    def get_transactions(self):
        msg = returnMsgSqlModule['SqlReturn']
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        myfile = cnxn.cursor()
        cnxn.add_output_converter(-155, handle_datetimeoffset)
        myfile.execute("""SELECT CARD_TRANSACTIONS.TRANSACTION_ID, CARD_TRANSACTIONS.SUMM,CARD_TRANSACTIONS.TRANSACTION_TIME,CARD_CLIENTS.NAME,CARD_TRANSACTION_NOTES.XML_CHECK
                                FROM CARD_CARDS
                                LEFT JOIN CARD_PEOPLE_ACCOUNTS ON CARD_CARDS.PEOPLE_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ID
                                JOIN CARD_TRANSACTIONS ON CARD_TRANSACTIONS.ACCOUNT_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ACCOUNT_ID
                                LEFT JOIN CARD_CLIENTS ON CARD_TRANSACTIONS.CLIENT_ID = CARD_CLIENTS.CLIENT_ID
                                LEFT JOIN CARD_TRANSACTION_NOTES ON CARD_TRANSACTIONS.TRANSACTION_ID = CARD_TRANSACTION_NOTES.TRANSACTION_ID
                                WHERE CARD_CARDS.CARD_CODE = {}
                              """.format(self.kwargs['cardcode']))
        records = myfile.fetchall()
        msg['msg'] = records
        self.sqlReturn = msg

    def change_password(self):
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        myfile = cnxn.cursor()
        myfile.execute("""UPDATE
                                    CARD_CARDS
                                    SET
                                    TEXT_PASSWORD = '{1}'
                                    WHERE
                                    CARD_CODE = {0}
                              """.format(self.kwargs['cardcode'], self.kwargs['password']))
        cnxn.commit()
        msg = returnMsgSqlModule['ChangePasswordSuccessfully']
        self.sqlReturn = msg


a = sqlQuery(cmd='get_card_info', cardcode=602567)
b = sqlQuery(cmd='get_card_info', cardcode=602237)
a.start()
b.start()
a.join()
b.join()
print(a.sqlReturn)
print(b.sqlReturn)
