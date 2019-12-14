from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

import mysql.connector
import validators
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Resource, Api, reqparse
from haversine import haversine

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin: *'

cors = CORS(app)
api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per second"],
)


def get_cnx():
    cnx = mysql.connector.connect(user='root', password='misha_benich228',
                                  host='0.0.0.0',
                                  database='meets')

    return cnx


class TestConnection(Resource):
    def get(self):
        cnx = get_cnx()
        cnx.close()
        return {'status': 'success'}


class GetOrders(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client', type=int)
        args = parser.parse_args()
        _client = args['client']


        cnx = get_cnx()
        cursor = cnx.cursor(buffered=True)
        query = "select * from orders where id_client = %s;"
        data = (_client)

        response = []
        cursor.execute(query, data)
        for item in cursor:
            i = 0
            order = {}
            for value in item:
                if i == 0:
                    order.update({'id_order': value})
                if i == 1:
                    order.update({'id_client': value})
                if i == 2:
                    order.update({'id_product': value})
                if i == 3:
                    order.update({'date_time': value})
                if i == 4:
                    order.update({'remark': value})
                i += 1
            response.append(order)
        cursor.close()
        cnx.close()
        return response


class AddOrder(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client', type=int)
        parser.add_argument('product', type=int)
        parser.add_argument('date_time', type=str)
        parser.add_argument('remark', type=str)
        args = parser.parse_args()
        _client = args['client']
        _product = args['product']
        _date_time = args['date_time']
        _remark = args['remark']

        cnx = get_cnx()
        cursor = cnx.cursor()
        query = "insert into orders values (default, %s, %s %s, %s);"
        data = (_client, _product, _date_time, _remark)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()

        return {'success': True}


class EditOrder(Resource):
    def post(self):
        pass


class CancelOrder(Resource):
    def post(self):
        pass


class ApplyForView(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_client', type=int)
        parser.add_argument('id_car', type=int)
        parser.add_argument('date', type=str)

        args = parser.parse_args()
        _id_client = args['id_client']
        _id_car = args['id_car']
        _date = args['date']


        cnx = get_cnx()
        cursor = cnx.cursor()
        query = "insert into entry values (default, %s %s, %s);"
        data = (_id_client, _id_car, _date)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()

        return {'success': True}


class GetContracts(Resource):
    def get(self):

        cnx = get_cnx()
        cursor = cnx.cursor(buffered=True)
        query = "select * from contract_ws;"

        response = []
        cursor.execute(query)
        for item in cursor:
            i = 0
            order = {}
            for value in item:
                if i == 0:
                    order.update({'id_contract_ws': value})
                if i == 1:
                    order.update({'id_contract': value})
                if i == 2:
                    order.update({'id_work_type': value})
                if i == 3:
                    order.update({'id_spare': value})
                if i == 4:
                    order.update({'id_employee': value})
                i += 1
            response.append(order)
        cursor.close()
        cnx.close()
        return response


class AddContract(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_client', type=int)
        parser.add_argument('id_car', type=int)
        parser.add_argument('date_start', type=str)
        parser.add_argument('date_end', type=str)
        parser.add_argument('status', type=str)


        args = parser.parse_args()
        _id_client = args['id_client']
        _id_car = args['id_car']
        _date_start = args['date_start']
        _date_end = args['date_end']
        _status = args['status']

        cnx = get_cnx()
        cursor = cnx.cursor()
        query = "insert into contract values (default, %s %s, %s, %s, %s);"
        data = (_id_client, _id_car, _date_start, _date_end, _status)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()

        return {'success': True}


class EditContract(Resource):
    def post(self):
        pass


class DeleteContract(Resource):
    def post(self):
        pass


class Auth(Resource):
    def get(self):
        pass


class GetServices(Resource):
    def get(self):
        cnx = get_cnx()
        cursor = cnx.cursor(buffered=True)
        query = "select * from work_type;"

        response = []
        cursor.execute(query)
        for item in cursor:
            i = 0
            order = {}
            for value in item:
                if i == 0:
                    order.update({'id_work_type': value})
                if i == 1:
                    order.update({'name_work': value})
                if i == 2:
                    order.update({'price': value})
                if i == 3:
                    order.update({'time_frame': value})
                i += 1
            response.append(order)
        cursor.close()
        cnx.close()
        return response


class GetUsedServices(Resource):
    def get(self):
        pass


class AddService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client', type=int)
        parser.add_argument('price', type=float)
        parser.add_argument('date_time', type=str)
        args = parser.parse_args()
        _name_work = args['client']
        _price = args['price']
        _date_time = args['date_time']

        cnx = get_cnx()
        cursor = cnx.cursor()
        query = "insert into work_type values (default, %s %s, %s);"
        data = (_name_work, _price, _date_time)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()

        return {'success': True}


class DeleteService(Resource):
    def post(self):
        pass


class AddPart(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('guarantee', type=str)
        args = parser.parse_args()
        _name = args['name']
        _price = args['price']
        _guarantee = args['guarantee']

        cnx = get_cnx()
        cursor = cnx.cursor()
        query = "insert into spares values (default, %s %s, %s);"
        data = (_name, _price, _guarantee)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()

        return {'success': True}


class DeletePart(Resource):
    def post(self):
        pass


class GetParts(Resource):
    def get(self):
        cnx = get_cnx()
        cursor = cnx.cursor(buffered=True)
        query = "select * from spares;"

        response = []
        cursor.execute(query)
        for item in cursor:
            i = 0
            order = {}
            for value in item:
                if i == 0:
                    order.update({'id_spare': value})
                if i == 1:
                    order.update({'name': value})
                if i == 2:
                    order.update({'price': value})
                if i == 3:
                    order.update({'guarantee': value})
                i += 1
            response.append(order)
        cursor.close()
        cnx.close()
        return response


class AddWorker(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('job_title', type=str)

        args = parser.parse_args()
        _name = args['name']
        _surname = args['surname']
        _phone = args['phone']
        _job_title = args['job_title']

        cnx = get_cnx()
        cursor = cnx.cursor()
        query = "insert into employee values (default, %s %s, %s, %s);"
        data = (_name, _surname, _phone, _job_title)
        cursor.execute(query, data)
        cnx.commit()
        cnx.close()

        return {'success': True}


class DeleteWorker(Resource):
    def post(self):
        pass


class GetWorkers(Resource):
    def get(self):
        cnx = get_cnx()
        cursor = cnx.cursor(buffered=True)
        query = "select * from employee;"

        response = []
        cursor.execute(query)
        for item in cursor:
            i = 0
            order = {}
            for value in item:
                if i == 0:
                    order.update({'id_employee': value})
                if i == 1:
                    order.update({'name': value})
                if i == 2:
                    order.update({'surname': value})
                if i == 3:
                    order.update({'phone': value})
                if i == 3:
                    order.update({'job_title': value})
                i += 1
            response.append(order)
        cursor.close()
        cnx.close()
        return response


if __name__ == '__main__':
    context = ('/etc/ssl/vargasoff.ru.crt', '/etc/ssl/private.key')
    app.run(host='0.0.0.0', port='8000', ssl_context=context)