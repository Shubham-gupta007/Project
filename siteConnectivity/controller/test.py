import server
import collections
import json
import pingparsing

def siteConnection():
    conn = server.mysqlConnection('shubham')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites_collection WHERE state='active';")
    # myresult = mycursor.fetchall()
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
        rowarray_list.append(d)
    result = json.dumps(rowarray_list)
    parsed_json = (json.loads(result))
    all_dns = ""
    for i in range(len(parsed_json)):
        all_dns += parsed_json[i]['dns_name'] + ","

    print(all_dns)
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
        transmitter.count = 10
        result = transmitter.ping()

        print(json.dumps(ping_parser.parse(result).as_dict(), indent=4))




checkConnection()