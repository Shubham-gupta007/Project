import server
from flask import jsonify
from flask import flash, request
from app import app
import collections
import time

# Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(20), state varchar(20), created_date DATE, updated_date DATE, error_code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id));

# def createTable():
#     conn = server.mysqlConnection()
#     print("conn",conn)
#     myscursor = conn.cursor()
#     myscursor.execute("Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(20), state varchar(20), created_date DATE, updated_date DATE, error_code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id))")





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
        print("_createddate",_createddate)
        _updateddate = time.time()
        print("_updateddate",_updateddate)
        _state = "active"
        if _dnsname and request.method == "POST":
            sqlQuery = "INSERT INTO sites_collection(dns_name,created_date,updated_date,state) VALUES(%s, %s, %s, %s);"
            bindData = (_dnsname,_createddate,_updateddate,_state)
            conn = server.mysqlConnection('shubham')
            print("conn",conn)
            cursor = conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response =jsonify(message ="Site added Successfully")
            response.status_code = 200
            return  response
        else:
            return  not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/show')
def show_emp():
    try:
        conn = server.mysqlConnection('shubham')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rest_emp")

        emprows = cursor.fetchall()
        rowarray_list = []
        for row in emprows:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['name'] = row[1]
            d['email'] = row[2]
            d['phone'] = row[3]
            d['address'] = row[4]
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