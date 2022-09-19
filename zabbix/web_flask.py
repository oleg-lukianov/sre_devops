"""Script for add host in group controller"""
import os
from zabbix_api import *
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def path_root():
    information()
    return "<p>GET/POST method!</p><br><Hello>"

@app.route("/get", methods=['GET'])
def path_get():
    information()
    return "<p>GET method!</p>"

@app.route("/post", methods=['POST'])
def path_post():
    information()
    return "<p>POST method!</p>"

@app.before_request
def log_request_info():
    print(f'Headers: {request.headers}')
    print(f'Body: {request.get_data()}')

# @app.after_request
# def log_request_info():
#     # print(f'Headers: {request.headers}')
#     print(f'Body: {request.get_data()}')

def information():
    print('http://apple.pro:443/')

@app.route("/host_create", methods=['GET'])
def host_create():
    """Main function"""
    zabbix_api = ZabbixAPI()
    auth = zabbix_api.zabbix_user_login()
    zabbix_api.zabbix_host_create_simple(auth, "CN-ICH-S0970744", "127.0.0.1", 10050, 5, 10186, "ci_name", "ci_key",
                        "ci_address", "ci_admin", "ci_owner", "ci_order_number", "ci_main_backup", "ci_searchcode")
    zabbix_api.zabbix_user_logout(auth)
    return "<p>host_create!</p>"


@app.route("/host_create_post", methods=['POST'])
def host_create_post():
    """Main function"""

    search = request.form.get("search")
    page = request.form.get("page")

    print(f'{str(request.form)}')

    zabbix_api = ZabbixAPI()
    auth = zabbix_api.zabbix_user_login()
    zabbix_api.zabbix_host_create_simple(auth, "CN-ICH-S0970744", "127.0.0.1", 10050, 5, 10186, "ci_name", "ci_key",
                        "ci_address", "ci_admin", "ci_owner", "ci_order_number", "ci_main_backup", "ci_searchcode")
    zabbix_api.zabbix_user_logout(auth)
    body = (f'<p>host_create_post!</p>'
            f'<br>search = {search}'
            f'<br>page = {page}')
    return body


app.run(host='0.0.0.0', port=8081, debug=True)

