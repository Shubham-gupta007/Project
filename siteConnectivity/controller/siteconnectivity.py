import server
from flask import jsonify
from flask import flash, request
from app import app
import collections
import time
import logging
from logging.handlers import TimedRotatingFileHandler
loglocation = "/home/shubham/Shubham/Self Projects/Project/siteConnectivity/controller/"
handler = TimedRotatingFileHandler(loglocation+'siteconnectivity.log', when="s", interval=5)
handler.suffix = "%Y-%m-%d_%H-%M-%S"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
# ALTER TABLE sites_collection ADD packet_transmit int(10),ADD packet_receive int(10),ADD packet_loss_count int(10),ADD packet_loss_rate int(10),ADD rtt_min int(10),ADD rtt_avg int(10),ADD "rtt_max" int(10),ADD rtt_mdev int(10);
# Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(20), state varchar(20), created_date DATE, updated_date DATE, code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id));
# Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(150), state varchar(150), created_date varchar(150), updated_date varchar(150), code varchar(150), error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id));
# def createTable():
#     conn = server.mysqlConnection()
#     print("conn",conn)
#     myscursor = conn.cursor()
#     myscursor.execute("Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(150), state varchar(150), created_date INT(11) NOT NULL DEFAULT '0', updated_date INT(11) NOT NULL DEFAULT '0', code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id))")


@app.route('/add', methods=['POST'])
def addSiteName():
    try:
        _json = request.json
        _dnsname = _json['dns_name']
        _status = _json['status']
        _state = _json['state']
        _createddate = _json['created_date']
        _updateddate = _json['updated_date']
        _errorcode = _json['code']
        _errormsg = _json['error_message']
        _ipaddress = _json['ipaddress']
        _packettransmit = _json['packet_transmit']
        _packerreceive = _json['packet_receive']
        _packetlosscount = _json['packet_loss_count']
        _packetlossrate = _json['packet_loss_rate']
        _rttmin = _json['rtt_min']
        _rttmax = _json['rtt_max']
        _rttavg = _json['rtt_avg']
        _rttmdev = _json['rtt_mdev']
        _createddate = time.time()
        _updateddate = time.time()
        _state = "active"
        # if _dnsname and _status and _state and _createddate and _updateddate and _errorcode and _errormsg and _ipaddress and request.method == 'POST':
        if _dnsname and request.method == 'POST':
            # sqlQuery = "INSERT INTO sites_collection(dns_name, status, state, created_date, updated_date, code, error_message, ipaddress, packet_transmit, packet_receive, packet_loss_count, packet_loss_rate, rtt_min, rtt_max, rtt_avg, rtt_mdev) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
            sqlQuery = "INSERT INTO sites_collection(dns_name, status, state, created_date, updated_date, code, error_message, ipaddress, packet_transmit, packet_receive, packet_loss_count, packet_loss_rate, rtt_min, rtt_max, rtt_avg, rtt_mdev) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            # sqlQuery = "INSERT INTO sites_collection(dns_name, status, state, created_date, updated_date, code, error_message, ipaddress, packet_transmit, packet_receive, packet_loss_count, packet_loss_rate, rtt_min, rtt_max, rtt_avg, rtt_mdev) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            bindData = (_dnsname, _status, _state, _createddate, _updateddate, _errorcode, _errormsg, _ipaddress,_packettransmit, _packerreceive, _packetlosscount, _packetlossrate , _rttmin , _rttmax,_rttavg, _rttmdev)
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify(message="Site added Successfully")
            response.status_code = 200
            logger.info("New entry in sites_collection function:addSiteName, filename:siteconnectivity")
            return response
        else:
            logger.error("Error in adding entry function:addSiteName, filename:siteconnectivity")
            return not_found()
    except Exception as e:
        logger.error("Error in Exception function:addSiteName, filename:siteconnectivity")
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/showall')
def showAllsites():
    try:
        if request.method == 'GET':

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
                d['error_message'] = row[6]
                d['ipaddress'] = row[7]
                d['rtt_min'] = row[8]
                d['rtt_avg'] = row[9]
                d['rtt_max'] = row[10]
                d['rtt_mdev'] = row[11]
                d['packet_transmit'] = row[12]
                d['packet_receive'] = row[13]
                d['packet_loss_count'] = row[14]
                d['packet_loss_rate'] = row[15]
                d['code'] = row[16]
                # d['code'] = row[4]
                rowarray_list.append(d)
            response = jsonify(rowarray_list)
            response.status_code = 200
            logger.info("Show all data in sites_collection function:showAllsites, filename:siteconnectivity")
            return response
        else:
            logger.error("Error in show data function:showAllsites, filename:siteconnectivity")
            return not_found()
    except Exception as e:
        logger.error("Exception in show data function:showAllsites, filename:siteconnectivity")
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
            sqlQuery = "SELECT * FROM sites_collection WHERE dns_name = '" + _dnsname + "' and state='active';"
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
            d['error_message'] = siterows[6]
            d['ipaddress'] = siterows[7]
            d['rtt_min'] = siterows[8]
            d['rtt_avg'] = siterows[9]
            d['rtt_max'] = siterows[10]
            d['rtt_mdev'] = siterows[11]
            d['packet_transmit'] = siterows[12]
            d['packet_receive'] = siterows[13]
            d['packet_loss_count'] = siterows[14]
            d['packet_loss_rate'] = siterows[15]
            d['code'] = siterows[16]
            rowarray_list.append(d)
            response = jsonify(rowarray_list)
            response.status_code = 200
            logger.info("Show single data in sites_collection function:showsinglesite, filename:siteconnectivity")
            return response
        else:
            logger.error("Error in show single data function:showsinglesite, filename:siteconnectivity")
            return not_found()
    except Exception as e:
        logger.error("Exception in show single data function:showsinglesite, filename:siteconnectivity")
        return not_found()
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatesite', methods=['POST'])
def updatesite():
    try:
        _json = request.json
        _dnsname = _json['dns_name']
        _id = _json['id']
        print("1")
        if _dnsname and _id and request.method == 'POST':
            print("2", _dnsname, _id)
            # UPDATE
            # sites_collection
            # SET
            # dns_name = 'xyz.com'
            # WHERE
            # state = 'active' and id = '4';
            # sqlQuery = "UPDATE sites_collection SET dns_name = '" + _dnsname + "'  WHERE state='active' and id= '" + _id + "'; "
            sqlQuery = "UPDATE sites_collection SET dns_name = '"+_dnsname+"'  WHERE state='active' and id= '"+_id+"'; "
            print("3")
            print(sqlQuery)
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            print("4")
            cursor.execute(sqlQuery)
            # siterows = cursor.fetchone()
            # rowarray_list = []
            # for row in siterows:
            # d = collections.OrderedDict()
            # d['id'] = siterows[0]
            # d['dns_name'] = siterows[1]
            # d['status'] = siterows[2]
            # d['state'] = siterows[3]
            # d['created_date'] = siterows[4]
            # d['updated_date'] = siterows[5]
            # d['code'] = siterows[6]
            # d['error_message'] = siterows[7]
            # d['ipaddress'] = siterows[8]
            # rowarray_list.append(d)
            conn.commit()
            response = jsonify(message="Site updated Successfully")
            response.status_code = 200
            return response
        else:
            print("5")
            return not_found()
    except Exception as e:
        print("6")
        return not_found()
        print(e)
    finally:
        print("7")
        cursor.close()
        conn.close()

@app.route('/deletesite', methods=['POST'])
def deletesite():
    try:
        _json = request.json
        _dnsname = _json['dns_name']
        if _dnsname and request.method == 'POST':
            sqlQuery = "UPDATE sites_collection SET state = 'deleted' WHERE dns_name ='"+_dnsname+"'; "
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
            response = jsonify(message="Deleted Successfully")
            response.status_code = 200
            logger.info("Delete single data in sites_collection function:deletesite, filename:siteconnectivity")
            return response
        else:
            logger.error("Error in delete single data in sites_collection function:deletesite, filename:siteconnectivity")
            return not_found()
    except Exception as e:
        logger.error("Exception in delete single data in sites_collection function:deletesite, filename:siteconnectivity")
        return not_found()
        print(e)
    finally:
        cursor.close()
        conn.close()

def getallsites():
    conn = server.mysqlConnection('shubham')
    mycursor = conn.cursor()
    mycursor.execute("Select * from sites_collection")
    myresult = mycursor.fetchall()
    for row in myresult:
        print(row)
    # try:
    #     conn = server.mysqlConnection('shubham')
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM sites_collection WHERE state='active';")
    #
    #     siterows = cursor.fetchall()
    #     rowarray_list = []
    #     for row in siterows:
    #         d = collections.OrderedDict()
    #         d['id'] = row[0]
    #         d['dns_name'] = row[1]
    #         d['status'] = row[2]
    #         d['state'] = row[3]
    #         d['created_date'] = row[4]
    #         d['updated_date'] = row[5]
    #         d['code'] = row[6]
    #         d['error_message'] = row[6]
    #         d['ipaddress'] = row[8]
    #         # d['code'] = row[4]
    #         rowarray_list.append(d)
    #     response = jsonify(rowarray_list)
    #     print(response)
    #     response.status_code = 200
    #     return response
    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close()
    #     conn.close()


def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    getallsites()
    app.run()
