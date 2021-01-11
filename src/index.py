# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sqlalchemy as sa
import abc
import random as ra
import types
import sqlite3
import json
from abc import ABC
from functools import wraps
from flask import Flask, jsonify
from flask import render_template
from flask import request

app = Flask(__name__)


class Tables:
    """
    資料表管理
        - 存放資料物件
    """
    def __init__(self, columns):
        self._id = 1
        self._tables = dict()

    def get(self, _table):
        if hasattr(_table, '__Type__'):
            raise TypeError
        key = _table.__class__.__name__
        return self._tables.get(key)

    def post(self, _table: object):
        key = _table.__class__.__name__
        value = _table
        self._tables.update({key: value})


class _ModelBase:
    """
    資料庫模型基類:
        - abc.ABC為強迫實作方法
    """
    def __init_subclass__(cls, **kwargs):
        cls.__Type__ = 'model'
        cls.__columns__ = dict()

    def get(self, *args, **kws):
        """資料庫查詢欄位"""
        if args:
            result = self.__columns__.get(args[0])
        elif kws:
            for k, v in self.__columns__.items():...

    def add(self, **kws):
        """資料庫新增欄位"""
        self.__columns__.update({**kws})


class Db:

    db_path = "db.sqlite"

    def __init__(self):
        self.__conn = sqlite3.connect(self.db_path)

    def new_member(self, user, password):
        cursor = self.__conn.cursor()
        sql = "select * from member where user=?"
        result = cursor.execute(sql, (user,))
        result = result.fetchone()
        if(result != None):  # 可以修飾
            return "此帳號已有人使用"
        else:
            sql = "insert into member(user, password) values(?,?)"
            cursor.execute(sql, (user, password))
            self.__conn.commit()
            return "ok"
        cursor.close()

    def login(self, user, password):
        cursor = self.__conn.cursor()
        sql = "select * from member where user=?"
        result = cursor.execute(sql, (user,))
        result = result.fetchone()
        cursor.close()
        if(result != None):  # 可以修飾
            if(result[1] == password):
                
                return "登入成功"
            else:
                return "密碼錯誤"
        else:
            return "沒這個帳號"

    def figure(self):
        cursor = self.__conn.cursor()
        sql = "select count(*) from figure"
        result = cursor.execute(sql)
        result = result.fetchone()[0]
        sn = ra.randint(1, result)
        sql = "select * from figure where sn=?"
        result = cursor.execute(sql, (sn,))
        result = result.fetchone()
        path = result[1]
        cursor.close()
        return path


class MySQL:
    def __init__(self, *dbs):
        self._tables = {}
        self._init(*dbs)

    def _init(self, *dbs):
        for db in dbs:
            if not hasattr(db, 'get'):
                print(f'== DataBase: {db.__name__} Default FAIL ==')
            self._tables.update({db.__class__.__name__: db})

    def query(self, model):
        model_name = model.__class__.__name__
        return self._tables.get(model_name)


class MissingColumnError:
    ...


class Users:
    """資料庫"""
    def __init__(self):
        self._columns_schema = ['username', 'student_id', 'password_hash']
        self._id = 1
        self._columns = list()

    def create(self, **data) -> None:
        """新增"""
        _data = self._schema(data, d=True)
        data['id'] = self._id
        self._columns.append(_data)
        print(self._columns)
        self._id += 1

    def filter_by(self, username: str) -> dict or str:
        """查詢"""
        for column in self._columns:
            if column.get('username') == username:
                return column
        return f'User {username} is not exist!!'

    def get(self, id_: int) -> dict:
        """index精準查詢"""
        return self._columns[id_-1]

    def _schema(self, data: dict, d=False) -> dict:
        """檢查資料是否符合格式"""
        for _column in self._columns_schema:
            if not data.get(_column.lower()):
                if not d:
                    raise KeyError(f'Missing column {_column}!!')
                else:
                    data[_column.lower()] = None
        return data


def schema(*columns):

    def _mid(f):
        @wraps(f)
        def _inside(*args, **kws):
            data = request.args.to_dict()
            for column in columns:
                if not data.get(column):
                    raise KeyError(f'Missing Column {column}')
            kws.update(**data)
            return f(*args, **kws)
        return _inside
    return _mid


users = Users()


def init():
    username = 'jojo'
    student_id = '0000'
    pw_hash = hash(username + student_id)
    data = {
        'username': username,
        'student_id': student_id,
        'password_hash': pw_hash,
    }
    users.create(**data)
    print('== db init SUCCESS ==')


init()


@app.route("/kevin", methods=["GET"])
@schema('username')
def kevin(**kws):
    data = users.filter_by(**kws)
    data.pop('password_hash')
    return jsonify(data)


@app.route("/register")
@schema('username', 'student_id', 'password')
def register(**kws):
    pw = kws.pop('password')
    username = kws.get('username')
    _hash = hash(pw + username)
    print(f'this is pw: {pw}')
    print(f'this is username: {username}')
    print(f'this is _hash: {_hash}')
    kws['password_hash'] = _hash
    users.create(**kws)
    return 'SUCCESS'


@app.route("/login")
@schema('username', 'password')
def _login(**kws):
    pw = kws.get('password')
    username = kws.get('username')
    print(f'this is username: {username}')
    print(f'this is password: {pw}')
    pwh = hash(username + pw)
    print(f'this is pwh: {pwh}')
    user = users.filter_by(username=username)
    if user.get('password_hash') != pwh:
        return '== LOGIN FAIL =='
    return 'LOGIN SUCCESS!!!'


@app.route("/index")
def index():
    return render_template("index.html")  


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/new_member")
def new_member():
    return render_template("newmember.html")


@app.route("/member_ok", methods=['POST'])
def member_ok():
    user = request.values["user"]
    password = request.values["password"]
    confirm = request.values["confirm"]
    if(password != confirm):
        result = "密碼不一致"
        return render_template("check.html", **locals())
    else:
        db_result = Db()
        result = db_result.newmember(user, password)
        if(result == "此帳號已有人使用"):
            return render_template("check.html", **locals())
        else:
            result = user
            return render_template("welcome.html", **locals())
        #return render_template("login.html")


@app.route("/submit",methods=['POST'])
def submit():
    user = request.values["user"]
    password = request.values["password"]
    result = Db()
    result1 = result.login(user,password)
    if(result1 == "登入成功"):
        result = user
        return render_template("welcome.html", **locals())
    elif(result1 == "密碼錯誤"):
        result = "密碼錯誤"
        return render_template("check.html", **locals())
    else:
        result = "沒有這個帳號"
        return render_template("check.html", **locals())


@app.route("/ok", methods=['GET'])
def ok():
    user = request.args.get("user")
    result = Db()
    path = result.figure()
    return render_template("figure.html", **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)
