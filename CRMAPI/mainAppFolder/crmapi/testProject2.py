import threading
import pyodbc
import random
server = '11.11.11.16,9433'
database = 'CRM'
username = 'rk7'
password = 'rk7'
returnStr = {}
def get_card_info():
    global returnStr
    a = [600230,600321,600482,600233,600384,600995,600326,600337,600339,600339]
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    myfile = cnxn.cursor()
    # while not app.config['SqlState']:
    #    continue
    # app.config['SqlState'] = False
    ran = random.randint(0,len(a)-1)
    myfile.execute("""SELECT CARD_CARDS.CARD_CODE,CARD_TRANSACTIONS.TRANSACTION_ID, CARD_TRANSACTIONS.SUMM,CARD_CLIENTS.NAME,CARD_TRANSACTION_NOTES.XML_CHECK
                                FROM CARD_CARDS
                                LEFT JOIN CARD_PEOPLE_ACCOUNTS ON CARD_CARDS.PEOPLE_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ID
                                JOIN CARD_TRANSACTIONS ON CARD_TRANSACTIONS.ACCOUNT_ID = CARD_PEOPLE_ACCOUNTS.PEOPLE_ACCOUNT_ID
                                LEFT JOIN CARD_CLIENTS ON CARD_TRANSACTIONS.CLIENT_ID = CARD_CLIENTS.CLIENT_ID
                                LEFT JOIN CARD_TRANSACTION_NOTES ON CARD_TRANSACTIONS.TRANSACTION_ID = CARD_TRANSACTION_NOTES.TRANSACTION_ID
                                WHERE CARD_CARDS.CARD_CODE = {}
                              """.format(a[ran]))
    import time
    records = myfile.fetchall()
    returnStr[ran] = records
    # app.config['SqlState'] = True
import threading
import time


def worker():
    print(threading.current_thread().getName(), 'Starting')
    time.sleep(5)
    print(threading.current_thread().getName(), 'Exiting')


def my_service():
    print(threading.current_thread().getName(), 'Starting')
    time.sleep(5)
    print(threading.current_thread().getName(), 'Exiting')


threads = []
for i in range(100):
    t = threading.Thread(target=get_card_info)
    threads.append(t)
    t.start()
    t.join()
for k,v in returnStr.items():
    print(k,v)
print('hihi')