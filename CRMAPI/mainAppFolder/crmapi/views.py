from flask import request, jsonify, Blueprint, abort
from mainAppFolder.crmapi import functions, returnMsg, sqlQuery
#from mainAppFolder.crmapi import testProject3
crmapiApp = Blueprint('crmapiApp', __name__)


@crmapiApp.route('/', methods=['GET'])
def index():
    return "<h1>HYG CRM API</h1>"


@crmapiApp.route('/login', methods=['POST'])
def login():
    if request.is_json:
        cardcode = request.json.get('cardcode')
        password = request.json.get('password')
        try:
            assert (len(cardcode) == 6)
            cardcode = int(cardcode)
        except:
            return jsonify(returnMsg.returnMsg["400"])
        dataReturnFromSQL = [record for record in sqlQuery.get_cardcode_password(cardcode)]
        if len(dataReturnFromSQL) == 1:
            cardcodeCheck, cardcodeCheckPassword, people_id = dataReturnFromSQL[0]
            print(cardcodeCheck, cardcodeCheckPassword, people_id)
            if cardcodeCheckPassword == None:
                cardcodeCheckPassword = '19801980'
            else:
                pass
            if cardcodeCheckPassword == password:
                msg = returnMsg.returnMsg["Return Token"]
                msg['msg'] = functions.generate_auth_token(cardcode, people_id)
                return jsonify(msg)
            else:
                return jsonify(returnMsg.returnMsg["Username or Password Incorrect"])
        elif len(dataReturnFromSQL) == 0:
            return jsonify(returnMsg.returnMsg["Username or Password Incorrect"])
        else:
            abort(500)
    else:
        abort(405)


@crmapiApp.route('/firstlogin', methods=['PUT'])
@functions.login_required
def firstlogin(guardMsg):
    while True:
        if (crmapiApp.config['SqlState']):
            break
    if request.is_json:
        print(guardMsg)
        if guardMsg == 'Warn':
            return jsonify(returnMsg.returnMsg["400"])
        else:
            password = request.json.get('password')
            sqlQuery.change_password(guardMsg, password)
            return jsonify(returnMsg.returnMsg["Password change successfully"])
    else:
        abort(405)


@crmapiApp.route('/transactions', methods=['GET'])
@functions.login_required
def transactions(guardMsg):
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsg["400"])
    else:
        msg = returnMsg.returnMsg["Return Transaction List"]
        for record in sqlQuery.get_transactions(guardMsg):
            id, value, time, location, details = [value for value in record]
            if details != None:
                details = functions.convert_xml_json(details)
                details = details['CHECK']['CHECKDATA']['CHECKLINES']['LINE']
            try:
                msg['msg'][id] = {'value': float(value), 'location': location, 'time': time[:-15], 'details': details}
            except:  # value variable can be none but float() not happy with that
                msg['msg'][id] = {'value': value, 'location': location, 'time': time[:-15], 'details': details}
        for k,v in msg['msg'].items():
            print(k,v)
        return jsonify(msg)


@crmapiApp.route('/cardinfo', methods=['GET'])
@functions.login_required
def cardinfo(guardMsg):
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsg["400"])
    else:
        msg = returnMsg.returnMsg["Return Card Info"]
        record = [value for value in sqlQuery.get_card_info(guardMsg)]
        if len(record) == 1:
            CARD_CODE, PEOPLE_ID, F_NAME, L_NAME, FULL_NAME, TEXT_PASSWORD, BIRTHDAY, SOURCE, BALANCE = record[0]
            try:
                msg['msg'] = {'CARD_CODE': CARD_CODE, 'PEOPLE_ID': PEOPLE_ID, 'F_NAME': F_NAME, 'L_NAME': L_NAME,
                              'BIRTHDAY': BIRTHDAY, 'SOURCE': SOURCE, 'BALANCE': float(BALANCE)}
            except:  # BALANCE variable can be none but float() not happy with that
                msg['msg'] = {'CARD_CODE': CARD_CODE, 'PEOPLE_ID': PEOPLE_ID, 'F_NAME': F_NAME, 'L_NAME': L_NAME,
                              'BIRTHDAY': BIRTHDAY, 'SOURCE': SOURCE, 'BALANCE': float(BALANCE)}
            return jsonify(msg)
        else:
            abort(500)

@crmapiApp.route('/coupons', methods=['GET'])
@functions.login_required
def coupons(guardMsg):
    if guardMsg == 'Warn':
        return jsonify(returnMsg.returnMsg["400"])
    else:
        msg = returnMsg.returnMsg["Return Coupons Of Card"]
        records = [value for value in sqlQuery.get_coupons(guardMsg)]
        for record in records:
            cardcode, peopleID, couponID, couponCode, couponName, Datefrom, Dateto, Flag = record
            if Flag == 49: # Flag 49 mean not yet used
                msg['msg'].update({couponID:{'name':couponName,'issued':Datefrom,'expire':Dateto}})
            else:
                pass
        return jsonify(msg)
