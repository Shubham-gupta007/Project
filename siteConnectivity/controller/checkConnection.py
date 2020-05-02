import server
import collections
import json
import pingparsing
import time
import logging
from logging.handlers import TimedRotatingFileHandler
loglocation = "/home/shubham/Shubham/Self Projects/Project/siteConnectivity/controller/"
handler = TimedRotatingFileHandler(loglocation+'checkConnection.log', when="s", interval=5)
handler.suffix = "%Y-%m-%d_%H-%M-%S"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def siteConnection():
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
        d['code'] = row[6]
        d['error_message'] = row[6]
        d['ipaddress'] = row[8]
        rowarray_list.append(d)
    result = json.dumps(rowarray_list)
    parsed_json = (json.loads(result))
    all_dns = ""
    for i in range(len(parsed_json)):
        all_dns += parsed_json[i]['dns_name'] + ","
    return(all_dns)

def checkConnection():
    all_connection = siteConnection()
    trim_all_connection = all_connection[:-1]
    list_of_connection = trim_all_connection.split(",")
    print(len(list_of_connection))
    for i in range(len(list_of_connection)):
        print("'" + list_of_connection[i] + "'")
        ping_parser = pingparsing.PingParsing()
        transmitter = pingparsing.PingTransmitter()
        transmitter.destination = list_of_connection[i]
        transmitter.count = 3
        result = transmitter.ping()

        jsonresult = json.dumps(ping_parser.parse(result).as_dict(), indent=4)
        parsed_json = (json.loads(jsonresult))
        getresponse = updateConnectioninDB(list_of_connection[i],parsed_json)
        print("getresponse==",getresponse)

def updateConnectioninDB(list_of_connection,parsed_json):
    if (parsed_json['destination'] == None) :
        error_message = "Please Enter Valid Destination"
        code = "400"
        updation_time = str(time.time())
        sqlQuery = "UPDATE sites_collection SET error_message = '" + error_message + "', code = '" + code + "', updated_date = '" + updation_time + "'  WHERE dns_name ='" + list_of_connection + "'and state = 'active'; "
        # sqlQuery = "UPDATE sites_collection SET status = '" + status + "', rtt_max = '" + maximum_time + "',rtt_min = '" + minimum_time + "', code = '" + code + "', error_message = '" + error_message + "', packet_loss_count = '" + packet_loss_count + "', packet_receive = '" + packet_received + "', packet_transmit = '" + packet_transmit_count + "', rtt_avg = '" + average_rate_time + "', updated_date = '" + updation_time + "'  WHERE dns_name ='" + parsed_json['destination'] + "'and state = 'active'; "
        conn = server.mysqlConnection('shubham')
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        conn.commit()
        logger.error("Entry update in sites_collection function:updateConnectioninDB, filename:checkConnection " +updation_time + " value: " + list_of_connection)
        return("success")
    else:
        packet_transmit_count = str(parsed_json['packet_transmit'])
        packet_received = str(parsed_json['packet_receive'])
        packet_loss_count = str(parsed_json['packet_loss_count'])
        packet_loss_rate = parsed_json['packet_loss_rate']
        error_message = ""
        code = "200"
        average_rate_time = str(parsed_json['rtt_avg'])
        minimum_time = str(parsed_json['rtt_min'])
        maximum_time = str(parsed_json['rtt_max'])
        updation_time = str(time.time())
        if packet_loss_rate > 50.0:
            print("INSIDE IF")
            status = "down"
            # sqlQuery = "UPDATE sites_collection SET status = '"+status+"', rtt_avg = "+average_rate_time+", updated_date = '"+updation_time+"'  WHERE dns_name ='" + parsed_json['destination'] + "'and state = 'active'; "

            sqlQuery = "UPDATE sites_collection SET status = '"+status+"', rtt_max = '"+maximum_time+"',rtt_min = '"+minimum_time+"', code = '"+code+"', error_message = '"+error_message+"', packet_loss_count = '"+packet_loss_count+"', packet_receive = '"+packet_received+"', packet_transmit = '"+packet_transmit_count+"', rtt_avg = '"+average_rate_time+"', updated_date = '"+updation_time+"'  WHERE dns_name ='" + parsed_json['destination'] + "'and state = 'active'; "
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
        else:
            print("INSIDE ELSE")
            status = "up"
            # error_message = ""
            # code = "200"
            # average_rate_time = str(parsed_json['rtt_avg'])
            # minimum_time = str(parsed_json['rtt_min'])
            # maximum_time = str(parsed_json['rtt_max'])
            # updation_time = str(time.time())
            sqlQuery = "UPDATE sites_collection SET status = '"+status+"', rtt_max = '"+maximum_time+"',rtt_min = '"+minimum_time+"', code = '"+code+"', error_message = '"+error_message+"', packet_loss_count = '"+packet_loss_count+"', packet_receive = '"+packet_received+"', packet_transmit = '"+packet_transmit_count+"', rtt_avg = '"+average_rate_time+"', updated_date = '"+updation_time+"'  WHERE dns_name ='" + parsed_json['destination'] + "'and state = 'active'; "
            conn = server.mysqlConnection('shubham')
            cursor = conn.cursor()
            cursor.execute(sqlQuery)
            conn.commit()
        logger.info("Entry update in sites_collection function:updateConnectioninDB, filename:checkConnection " +updation_time + " value: " + parsed_json['destination'])
        return("success")


checkConnection()