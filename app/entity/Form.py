#-*- coding:utf-8 -*-
#!/usr/bin/env python
# @Time    : 2018/3/1 14:45
# @File    : App.py
# @Author  : 陈威彪

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import  Required
from wtforms.validators import DataRequired,EqualTo


'''
使用wtf实现表单
自定义表单类
登录表单
'''

class Login_Form(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password = PasswordField('密码:',validators=[DataRequired()])
    password2 = PasswordField('确认密码:',validators=[DataRequired(),EqualTo('password','密码填入的不一致')])
    #submit1 = SubmitField('注册')
    submit = SubmitField('登录')
'''
使用wtf实现表单
自定义表单类
注册表单
'''
class Register_Form(FlaskForm):
    username=StringField('用户名',validators=[DataRequired()])
    password=PasswordField('密码',validators=[DataRequired()])
    password2 = PasswordField('确认密码:', validators=[DataRequired(), EqualTo('password', '密码填入的不一致')])
    submit=SubmitField('注册')