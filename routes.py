from flask import Blueprint, Response, request, render_template
import json
import settings
import functions
import pprint
import StringIO
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html')


@routes.route('/functions/stations_manage')
def manage_stations():
    return render_template('stations_manage.html')


@routes.route('/functions/station_add', methods=['GET', 'POST'])
def stations_add():
    if request.method == 'POST':
        # inputs assumed valid
        functions.add_station(
            request.form.get('aws_id'),
            request.form.get('bom_number'),
            request.form.get('dfw_id'),
            request.form.get('station_name'),
            request.form.get('file_name'),
            request.files['scm'].read(),
            request.form.get('owner'),
            request.form.get('district'),
            request.form.get('lon'),
            request.form.get('lat'),
            request.form.get('elevation'),
            request.form.get('status'),
            request.form.get('deploydate'),
            request.form.get('message')
        )

        return Response('<h2>Inserted<h2><p>Go to the <a href="/stations">list of stations</a> to view</p>', status=200, mimetype='text/html')
    else:
        conn = functions.db_connect()
        districts = functions.get_districts(conn)
        functions.db_disconnect(conn)
        return render_template('stations_add.html', districts=districts)


@routes.route('/functions/station_edit')
def stations_edit():
    return render_template('stations_edit.html')