import MySQLdb
import logging
import sys
from datetime import datetime, date
import re
from lxml import etree
from StringIO import StringIO
import settings


def db_connect(host=settings.DB_SERVER, user=settings.DB_USR, passwd=settings.DB_PWB, db=settings.DB_DB):
    """
    Connects to the AWS database, default parameters supplied for normal connection
    """
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        logging.error("failed to connect to DB in get_station_aws_id()\n" + str(e))
        sys.exit(1)

    return conn


def db_disconnect(conn):
    conn.close()


def get_station(conn, aws_id):
    sql = "SELECT * FROM tbl_stations WHERE aws_id = '" + aws_id + "';"
    try:
        if conn is None:
            conn = db_connect()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)

        results = []
        while 1:
            row = cursor.fetchone()
            if row is None:
                break
            results = [
                {'aws_id': str(row['aws_id'])},
                {'bom_number': str(row['bom_number'])},
                {'dfw_id': str(row['dfw_id'])},
                {'name': str(row['name'])},
                {'filename': str(row['filename'])},
                {'scm': str(row['scm'])},
                {'owner': str(row['owner'])},
                {'district_id': str(row['district_id'])},
                {'lon': str(row['lon'])},
                {'lat': str(row['lat'])},
                {'elevation': str(row['elevation'])},
                {'status': str(row['status'])},
                {'deploydate': str(row['deploydate'])},
                {'message': str(row['message'])}
            ]
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        logging.error("failed to connect to DB in get_station()\n" + str(e))
        sys.exit(1)
    finally:
        cursor.close()
        conn.commit()
        #conn.close()

    if len(results) == 0:
        return None
    else:
        return results


def get_stations(conn):
    sql = "SELECT aws_id, name, owner FROM tbl_stations ORDER BY name;"
    try:
        if conn is None:
            conn = db_connect()

        cursor = conn.cursor()
        cursor.execute(sql)

        results = []
        while 1:
            row = cursor.fetchone()
            if row is None:
                break
            results.append({
                'aws_id': str(row[0]),
                'name': str(row[1]),
                'owner': str(row[2]),
            })
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        logging.error("failed to connect to DB in get_districts()\n" + str(e))
        sys.exit(1)
    finally:
        cursor.close()
        conn.commit()
        #conn.close()

    if len(results) == 0:
        return None
    else:
        return results


def get_districts(conn):
    sql = "SELECT id, name FROM tbl_districts ORDER BY name;"
    try:
        if conn is None:
            conn = db_connect()

        cursor = conn.cursor()
        cursor.execute(sql)

        results = []
        while 1:
            row = cursor.fetchone()
            if row is None:
                break
            #district_id, scm
            results.append({'district_id': str(row[0]), 'name': str(row[1])})
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        logging.error("failed to connect to DB in get_districts()\n" + str(e))
        sys.exit(1)
    finally:
        cursor.close()
        conn.commit()
        #conn.close()

    if len(results) == 0:
        return None
    else:
        return results


def add_station(conn, aws_id, bom_number, dfw_id, name, filename, scm, owner, district, lon, lat, elevation, status, deploydate, message):
    if len(str(bom_number)) < 6:
        bom_number = None
    if len(str(bom_number)) < 6:
        bom_number = None
    if len(str(deploydate)) < 6:
        deploydate = None
    if len(str(message)) < 6:
        message = None
    try:
        if conn is None:
            conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_stations VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (aws_id, bom_number, dfw_id, name, filename, scm, owner, district, lon, lat, elevation, status, deploydate, message))
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        logging.error("failed to connect to DB in add_station()\n" + str(e))
    finally:
        cursor.close()
        conn.commit()
        conn.close()