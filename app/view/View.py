#-*- coding:utf-8 -*-
#!/usr/bin/env python
# @Time    : 2018/3/1 14:45
# @File    : App.py
# @Author  : William

#导入Flask扩展
from flask import render_template, Blueprint,request,flash,redirect,url_for
from entity.Form import Login_Form,Register_Form
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from entity.User import Users
from App import db



view = Blueprint('pi',__name__)  #视图

@view.route('/')
def index():
    login_Form=Login_Form()
    return render_template('login.html',form=login_Form)

@view.route('/index',methods=['GET','POST'])
def index():
    #比如需要传入一个网址
    url_str = 'www.baidu.com'

    my_list =[1,3,5,7,8]
    my_disk = {
        'name': 'william',
        'sex' : 'man',
        'age' : 23
    }
    my_int =10
    return render_template("index.html",url_str=url_str,my_list = my_list,my_disk=my_disk,my_int=my_int)



@view.route('/login',methods=['GET','POST'])
def login():
    login_form = Login_Form()
    #request:请求对象--获取请求方式、数据
    #1.判断请求方式
    if request.method == "POST":
        #2.获取请求方式
        username = request.form.get('username')
        password = request.form.get( 'password')
        password2 = request.form.get('password2')

        # print(username)
        # print(password)
        # print(password2)
        #3.判断参数是否填写，密码是否相同

        if login_form.validate_on_submit(username = login_form.data):
            user = Users.query.filter_by(username = login_form.data).first()
            if user is not None and user.password == login_form.password.data:
                print(username,password)
                flash('登录成功')
                return redirect('index')
        else:
            flash('填入的参数有误')
    return render_template("login.html",form=login_form)


#<>定义一个理由是参数<>内需要起名字
#使用同一个视图函数，来显示不同用户的订单信息
@view.route('/order/<int:order_id>')
def get_order_id(order_id):
    #
    return 'order_id is %s' % order_id

@view.route('/register',methods=['GET','POST'])
def register():
    register_Form=Register_Form()
    if register_Form.validate_on_submit():
        user=Users(username=register_Form.username.data,password=register_Form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('view.index'))
    return render_template('register.html',form=register_Form)