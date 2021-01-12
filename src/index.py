# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random as ra
import types
import sqlite3
import json
from functools import wraps
from hashlib import md5
from flask import Flask, jsonify
from flask import render_template
from flask import request

app = Flask(__name__)


class MissingColumnError(Exception):
    """缺少資料庫欄位錯誤"""
    def __init__(self, column):
        super().__init__(f'自定義錯誤：缺少資料庫欄位{column}')


class NameToShortError(Exception):
    """帳號名稱過短"""
    def __init__(self, username):
        super().__init__(f'自定義錯誤：帳號名稱過短，使用者名稱{username}長度只有{len(username)}，規定為10')


def schema(*columns):
    """檢查request資料欄位"""
    def _mid(f):
        @wraps(f)
        def _inside(*args, **kws):
            data = request.args.to_dict()
            for column in columns:
                if not data.get(column):
                    raise MissingColumnError(column)
            kws.update(**data)
            return f(*args, **kws)

        return _inside

    return _mid


class Users:
    """資料庫"""
    def __init__(self):
        self._columns_schema = ['username', 'student_id', 'password_hash']
        self._id = 1
        self._columns = list()

    def create(self, **data) -> None:
        """新增"""
        _data = self._schema(data, d=True)
        _data['id'] = self._id
        self._columns.append(_data)
        print(self._columns)
        self._id += 1

    def filter_by(self, username: str) -> dict or str:
        """查詢"""
        for column in self._columns:
            if column.get('username') == username:
                return column
        return {}

    def get(self, id_: int) -> dict:
        """index精準查詢"""
        return self._columns[id_ - 1]

    def _schema(self, data: dict, d=False) -> dict:
        """檢查資料是否符合格式"""
        for _column in self._columns_schema:
            print(f'{_column}--->', data.get(_column.lower()))
            if not data.get(_column.lower()):
                if not d:
                    raise KeyError(f'Missing column {_column}!!')
                else:
                    data[_column.lower()] = None
        return data


# 資料庫實例化
# users = Users()


class Server:
    """伺服器"""
    def __init__(self):
        self._register = Register()  # 註冊
        self._login = Login()  # 登入

    def register(self, username, student_id):
        register_data = self._register.get_register_data(username=username, student_id=student_id)
        users.create(**register_data)

    def login(self, username, pw):
        return self._login.do(username=username, pw=pw)


class Login:
    """登入相關邏輯"""

    def do(self, username, pw):
        user = users.filter_by(username)
        origin_pw_hash = user.get('password_hash')
        check = self._valid_pw(username=username, pw=pw, origin_pw_hash=origin_pw_hash)
        return check

    @classmethod
    def _valid_pw(cls, username, pw, origin_pw_hash):
        _md5 = md5()
        target_str = username + pw
        _md5.update(target_str.encode('utf-8'))
        check_pw_hash = _md5.hexdigest()
        if check_pw_hash != origin_pw_hash:
            return False
        return True


class Register:
    """註冊相關邏輯"""

    def get_register_data(self, username: str, student_id: str) -> dict:
        _username = self._valid_username(username=username)
        _password = self._get_default_pw(from_=student_id)
        _crypto_str = self._info_crypto(username=_username, pw=_password)
        return {'username': _username, 'student_id': student_id, 'password_hash': _crypto_str}

    @classmethod
    def _valid_username(cls, username: str) -> str:
        """檢查username格式"""
        if len(username) < 10:
            raise NameToShortError(username)
        return username

    @staticmethod
    def _get_default_pw(from_: str) -> str:
        student_id = from_
        """預設密碼"""
        if not student_id:
            raise ValueError('Please key in your student_id.')
        length = len(student_id)
        if length >= 4:
            return student_id[length - 4:]
        else:
            return student_id

    @classmethod
    def _info_crypto(cls, username: str, pw: str):
        """資料加密"""
        _md5 = md5()
        target_str = username + pw
        _md5.update(target_str.encode('utf-8'))
        crypto_str = _md5.hexdigest()
        return crypto_str


# 伺服器實例化
# server = Server()


def init():
    """
    初始化伺服器:
        - 設置訪客帳號
    """
    username = 'iam69master'
    student_id = '123456789'
    pw_hash = hash(username + student_id)
    data = {
        'username': username,
        'student_id': student_id,
        'password_hash': pw_hash,
    }
    users.create(**data)
    print('== db init SUCCESS ==')


@app.route("/home", methods=["GET"])
def home(**kws):
    """首頁"""
    return '首頁'


##############################
#           普通API          #
##############################
@app.route("/search", methods=["GET"])
@schema('username')
def search(**kws):
    """搜尋使用者"""
    data = users.filter_by(**kws)
    data.pop('password_hash')
    return jsonify(data)


@app.route("/register")
@schema('username', 'student_id')
def register(**kws):
    """使用者註冊"""

    # 取得使用者資訊
    student_id = kws.pop('student_id')
    username = kws.get('username')

    if len(username) < 10:
        """檢查帳號長度"""
        return '帳號名稱過短'

    # 設置密碼(學號末四碼)
    pw = student_id[:len(student_id)-4]  # 學號末四碼

    # 取得、設置雜湊(用帳號+密碼進行運算) -> 務必密碼在前、帳號在後 pw+username, 反過來結果會不同
    kws['password_hash'] = hash(pw + username)

    # 存db
    users.create(**kws)
    return '註冊成功'


@app.route("/login")
@schema('username', 'password')
def _login(**kws):
    """使用者登入"""

    # 取得使用者資訊
    pw = kws.get('password')
    username = kws.get('username')

    # 以使用者輸入的密碼與帳號運算雜湊
    pwh = hash(pw + username)

    # 查詢資料庫
    user = users.filter_by(username=username)

    # 比對帳號密碼
    if user.get('password_hash') != pwh:
        """比對雜湊值"""
        return '帳號或密碼錯誤'
    return '登入成功'


##############################
#           優化API          #
##############################
@app.route("/search2", methods=["GET"])
@schema('username')
def search2(**kws):
    """搜尋使用者(優化版)"""
    data = users.filter_by(**kws)
    data.pop('password_hash')
    return jsonify(data)


@app.route("/register2")
@schema('username', 'student_id')
def register2(**kws):
    """使用者註冊(優化版)"""
    username = kws.get('username')
    student_id = kws.get('student_id')
    server.register(username, student_id)
    return '註冊成功'


@app.route("/login2")
@schema('username', 'password')
def _login2(**kws):
    """使用者登入(優化版)"""
    pw = kws.get('password')
    username = kws.get('username')
    login_success = server.login(username, pw)
    if not login_success:
        return '帳號或密碼錯誤'
    return '登入成功'
##############################


users = Users()
server = Server()
init()



# @app.route("/index")
# def index():
#     return render_template("index.html")
#
#
# @app.route("/login")
# def login():
#     return render_template("login.html")
#
#
# @app.route("/new_member")
# def new_member():
#     return render_template("newmember.html")
#
#
# @app.route("/member_ok", methods=['POST'])
# def member_ok():
#     user = request.values["user"]
#     password = request.values["password"]
#     confirm = request.values["confirm"]
#     if (password != confirm):
#         result = "密碼不一致"
#         return render_template("check.html", **locals())
#     else:
#         db_result = Db()
#         result = db_result.newmember(user, password)
#         if (result == "此帳號已有人使用"):
#             return render_template("check.html", **locals())
#         else:
#             result = user
#             return render_template("welcome.html", **locals())
#         # return render_template("login.html")
#
#
# @app.route("/submit", methods=['POST'])
# def submit():
#     user = request.values["user"]
#     password = request.values["password"]
#     result = Db()
#     result1 = result.login(user, password)
#     if (result1 == "登入成功"):
#         result = user
#         return render_template("welcome.html", **locals())
#     elif (result1 == "密碼錯誤"):
#         result = "密碼錯誤"
#         return render_template("check.html", **locals())
#     else:
#         result = "沒有這個帳號"
#         return render_template("check.html", **locals())
#
#
# @app.route("/ok", methods=['GET'])
# def ok():
#     user = request.args.get("user")
#     result = Db()
#     path = result.figure()
#     return render_template("figure.html", **locals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)
