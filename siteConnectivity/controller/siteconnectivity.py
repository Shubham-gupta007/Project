import server
from flask import jsonify
from flask import flash, request
from app import app
import collections
import time

# Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(20), state varchar(20), created_date DATE, updated_date DATE, error_code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id));
# Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(150), state varchar(150), created_date varchar(150), updated_date varchar(150), error_code varchar(150), error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id));
# def createTable():
#     conn = server.mysqlConnection()
#     print("conn",conn)
#     myscursor = conn.cursor()
#     myscursor.execute("Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(150), state varchar(150), created_date INT(11) NOT NULL DEFAULT '0', updated_date INT(11) NOT NULL DEFAULT '0', error_code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id))")


@app.route('/add', methods=['POST'])
def addSiteName():
    try:
        _json = request.json
        _dnsname = _json['dns_name']
        _status = _json['status']
        _state = _json['state']
        _createddate = _json['created_date']
        _updateddate = _json['updated_date']
        _errorcode = _json['error_code']
        _errormsg = _json['error_message']
        _ipaddress= _json['ipaddress']

        _createddate = time.time()
        _updateddate = time.time()
        _state = "active"
        # if _dnsname and _status and _state and _createddate and _updateddate and _errorcode and _errormsg and _ipaddress and request.method == 'POST':
        if _dnsname and request.method == 'POST':
            sqlQuery = "INSERT INTO sites_collection(dns_name, status, state, created_date, updated_date, error_code, error_message, ipaddress) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
            bindData = (_dnsname, _status, _state, _createddate, _updateddate, _errorcode, _errormsg, _ipaddress)
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify(message ="Site added Successfully")
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/showall')
def showAllsites():
    try:
        conn = server.mysqlConnection('shubham')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sites_collection WHERE state='active';")

        siterows = cursor.fetchall()
        rowarray_list = []
        for row in siterows:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['dns_name'] = row[1]
            d['status'] = row[2]
            d['state'] = row[3]
            d['created_date'] = row[4]
            d['updated_date'] = row[5]
            d['error_code'] = row[6]
            d['error_message'] = row[6]
            d['ipaddress'] = row[8]
            # d['error_code'] = row[4]
            rowarray_list.append(d)
        response = jsonify(rowarray_list)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/showsinglesite', methods=['POST'])
def showSinglesite():
    try:
        _json = request.json
        _dnsname = _json['dns_name']
        if _dnsname and request.method == 'POST':
            sqlQuery = "SELECT * FROM sites_collection WHERE dns_name = '"+ _dnsname +"' and state='active';"
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            siterows = cursor.fetchone()
            rowarray_list = []
        # for row in siterows:
            d = collections.OrderedDict()
            d['id'] = siterows[0]
            d['dns_name'] = siterows[1]
            d['status'] = siterows[2]
            d['state'] = siterows[3]
            d['created_date'] = siterows[4]
            d['updated_date'] = siterows[5]
            d['error_code'] = siterows[6]
            d['error_message'] = siterows[7]
            d['ipaddress'] = siterows[8]
            rowarray_list.append(d)
        response = jsonify(rowarray_list)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run()