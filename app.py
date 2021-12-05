import os
from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_hit_count():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'mysqldb',
        'port': '3306',
        'database': 'mydb',
        'auth_plugin': 'mysql_native_password'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT max(hit_count) FROM hit_count_table')
    result = cursor.fetchone()[0]
    cursor.execute(f'INSERT INTO hit_count_table VALUES ({result+10})')
    cursor.close()
    connection.commit()
    connection.close()

    return result

from flask import send_from_directory     
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(
        app.root_path, 'static'), 
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon')
# from flask import url_for
# app.add_url_rule(
#     '/favicon.ico', 
#     redirect_to=url_for('static', filename='favicon.ico'))

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World from tttxxx! I have been seen {} times.\n'.format(count)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
