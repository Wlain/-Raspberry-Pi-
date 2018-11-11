#-*- coding:utf-8 -*-
#!/usr/bin/env python
# @Time    : 2018/3/1 14:45
# @File    : App.py
# @Author  : 陈威彪

#-*- coding:utf-8 -*-
from importlib import import_module
import os
import smbus
#导入Flask扩展
from flask import Flask, render_template, Response,request,flash,redirect,url_for,jsonify
#from flask.ext.bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from entity.Form import Login_Form,Register_Form
from camera.camera_opencv import Camera
from flask.ext.bootstrap import Bootstrap
from cmd.cmd import cmd
from classify import classify_image
import subprocess
import json
import Adafruit_DHT
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
import sys
#重新加载sys模块
reload(sys)
#重新设置字符集
sys.setdefaultencoding("utf-8")


#创建Flask应用实例
app = Flask(__name__)
bootstrap  = Bootstrap(app)
#bootstrap = Bootstrap(app)
#各项插件的配置
app.secret_key = 'passwd'
#配置数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:unix_socket@127.0.0.1/pi'
#跟踪数据库的修改----》不建议开启，未来的版本中会移除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

db.init_app(app)
login_manger=LoginManager()
login_manger=LoginManager()
login_manger.session_protection='strong'
login_manger.login_view='view.login'
login_manger.init_app(app)

#初始化GPIO

led_board = 12          #led引脚，board模式
buzzer_channel = 11     #蜂鸣器引脚，board模式
relay_board = 37
dht_bcm = 4
dht_board = 11
rain_board = 13
soil_board = 36
tilt_board = 38
mq2_board = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_board, GPIO.OUT)
GPIO.setup(relay_board, GPIO.OUT)
GPIO.setup(buzzer_channel, GPIO.OUT)
GPIO.setup(rain_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(soil_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(tilt_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(mq2_board, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#蜂鸣器响铃
def beep(seconds):
    GPIO.output(buzzer_channel, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(buzzer_channel, GPIO.LOW)
#关闭蜂鸣器
def beep_off():
    GPIO.output(buzzer_channel, GPIO.HIGH)

def beepBatch(seconds, timespan, counts):
    for i in range(counts):
        beep(seconds)
        time.sleep(timespan)

#拍照
def gen2(camera):
    """Returns a single image frame"""
    frame = camera.get_frame()
    yield frame


'''
@打开LED灯
'''
@app.route('/led_on')
def led_on():
    GPIO.output(led_board, False)
    return render_template('index.html')

'''
@关闭LED灯
'''
@app.route('/led_off')
def led_off():
    GPIO.output(led_board, True)
    return render_template('index.html')


'''
@关闭继电器
'''
@app.route('/relay_off')
def relay_off():
    GPIO.output(relay_board, True)
    return render_template('index.html')

'''
@打开继电器
'''
@app.route('/relay_on')
def relay_on():
    GPIO.output(relay_board, False)
    return render_template('index.html')

'''
@拍照显示照片，这边直接返回一张照片
'''
@app.route('/image.jpg')
def image():
    """Returns a single current image for the webcam"""
    return Response(gen2(Camera()),mimetype='image/jpeg')

'''
@图像识别，这边直接调用谷歌开源的inception V3模型，具体是深度学习的内容
'''
@app.route('/recognition')
def recognition():
    img = requests.get('http://192.168.191.2:5000/image.jpg')  # a bird yo
    curr_img = Image.open(BytesIO(img.content))
    curr_img_cv2 = cv2.cvtColor(np.array(curr_img), cv2.COLOR_RGB2BGR)
    curr_img.save('./image/1.jpg')   
    print('the image is saved')
    print('======================')
    #classify_image.run_inference_on_image(curr_img_cv2)
    #curr_img_cv2.save('/image/image'
    pipe = subprocess.Popen('sudo python /home/pi/code/pi2/classify/classify_image.py --model_dir /home/pi/code/pi2/model/  --image_file /home/pi/code/pi2/image/1.jpg', shell=True, stdout=subprocess.PIPE).stdout
    # str = os.system('sudo python /home/pi/code/pi2/classify/classify_image.py --model_dir /home/pi/code/pi2/model/  --image_file /home/pi/code/pi2/image/1.jpg')
    # str = os.popen('sudo python /home/pi/code/pi2/classify/classify_image.py --model_dir /home/pi/code/pi2/model/  --image_file /home/pi/code/pi2/image/1.jpg')
    str = pipe.read()
    print(str)
    print('======================')   
    return render_template("recognition.html",str = str)


'''
@关闭树莓派
'''
@app.route('/power_off')
def power_off():
    os.system('sudo shutdown -h 0')
    return render_template('index.html')

'''
@重启树莓派
'''
@app.route('/reboot')
def reboot():
    os.system('sudo reboot')
    return render_template('index.html')

'''
@抽象用户类
'''
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True,index=True)
    password = db.Column(db.String(32),unique=True, index=True)

    def __init__(self,name,password):
        self.name=name
        self.password=password
    #repr()方法显示一个可读字符串
    def __repr__(self):
        return '<User:%s %s >'% (self.name,self.password)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False

'''
@初始化界面
'''
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template("index.html")
    #以下是flask框架传值的demo例子
    # cmd()
    #比如需要传入一个网址
    # url_str = 'www.baidu.com'
    # my_list =[1,3,5,7,8]
    # my_disk = {
    #     'name': 'william',
    #     'sex' : 'man',
    #     'age' : 23
    # }
    # my_int =10
    #return render_template("index.html",url_str=url_str,my_list = my_list,my_disk=my_disk,my_int=my_int)

'''
@更多功能按钮组件
'''
@app.route('/more_function',methods=['GET','POST'])
def more_function():
    return render_template('more_function.html')

'''
@打开蜂鸣器，这边设定为报警5秒
'''
@app.route('/buzzer_on',methods=['GET','POST'])
def buzzer_on():
    beep(50)
    return render_template('more_function.html')


'''
@关闭蜂鸣器
'''
@app.route('/buzzer_off',methods=['GET','POST'])
def buzzer_off():
    beepBatch(0.1,0.1,1)
    return render_template('more_function.html')

# 温湿度数据，这边定义为全局变量
history = [['Time', 'Temp', 'Humidity']]
c = 1

'''
@温湿度传感器采集
'''
@app.route("/dht11")
def dht11():
   global history, c
   h, t = Adafruit_DHT.read_retry(11, 4)
   print('Temperature:')
   print t
   print('Humidity:')
   print h
   history.append([str(c), t, h])
   c = c + 1
   return jsonify(history)

# 温湿度数据，这边定义为全局变量
history_lux = [['Time', '可见光值', '全光谱']]
d = 1

'''
@温湿度传感器展示
'''
@app.route('/dht',methods=['GET','POST'])
def dht():
    return render_template('dht.html')


'''
@光敏传感器采集
'''
@app.route("/lux")
def lux():
   global history_lux, d
   # TSL2561
   # Get I2C bus
   bus = smbus.SMBus(1)

   # TSL2561 address, 0x39(57)
   # Select control register, 0x00(00) with command register, 0x80(128)
   #               0x03(03)        Power ON mode
   bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
   # TSL2561 address, 0x39(57)
   # Select timing register, 0x01(01) with command register, 0x80(128)
   #               0x02(02)        Nominal integration time = 402ms
   bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

   time.sleep(0.5)

   # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
   # ch0 LSB, ch0 MSB
   data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

   # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
   # ch1 LSB, ch1 MSB
   data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

   # Convert the data
   ch0 = data[1] * 256 + data[0]
   ch1 = data1[1] * 256 + data1[0]

   # Output data to screen

   print "Full Spectrum(IR + Visible) :%d lux" % ch0
   print "Infrared Value :%d lux" % ch1
   print "Visible Value :%d lux" % (ch0 - ch1)
   history_lux.append([str(d), (ch0 - ch1), ch0])
   d = d + 1
   return jsonify(history_lux)
'''
@光敏传感器展示
'''
@app.route('/lux_show',methods=['GET','POST'])
def lux_show():
    return render_template('lux.html')



'''
@雨滴传感器
'''
@app.route("/raindrop",methods=['GET','POST'])
def raindrop():
    status = GPIO.input(rain_board)
    if status == True:
        judgment = '此时没有下雨'
    else:
        judgment = '此时正在下雨'
    print judgment
    return render_template('raindrop.html', str=judgment)


'''
@烟雾Mq-2传感器
'''
@app.route("/mq2",methods=['GET','POST'])
def mq2():
    status = GPIO.input(mq2_board)
    if status == True:
        judgment = '此时没有检测到烟雾'
    else:
        judgment = '危险！此时校测到烟雾！！！！'
    print judgment
    return render_template('mq2.html', str=judgment)

'''
@土壤湿度传感器
'''
@app.route("/soil",methods=['GET','POST'])
def soil():
    status = GPIO.input(soil_board)
    if status == True:
        judgment = '此时土壤干燥'
    else:
        judgment = '此时土壤湿润！！！！！'
    print judgment
    return render_template('soil.html', str=judgment)

'''
@倾斜传感器
'''
@app.route("/tilt",methods=['GET','POST'])
def tilt():
    status = GPIO.input(tilt_board)
    if status == True:
        judgment = '此时没有倾斜'
    else:
        judgment = '此时物体倾斜了！！！！'
    print judgment
    return render_template('tilt.html', str=judgment)

'''
登录接口
'''
@app.route('/',methods=['GET','POST'])
def login():
    login_form = Login_Form()
    #request:请求对象--获取请求方式、数据
    #1.判断请求方式
    if request.method == "POST":
        #2.获取请求方式
        username = request.form.get('username')
        password = request.form.get( 'password')
        password2 = request.form.get('password2')

        print(username)
        print(password)
        print(password2)
        #3.判断参数是否填写，密码是否相同
        if login_form.validate_on_submit():
            user = Users.query.filter_by( name = login_form.username.data).first()
            if user is not None and user.password == login_form.password.data:
                print(username,password)
                flash('登录成功')
                #return 'success'
                return redirect(url_for('index'))
            else:
                flash('账号或者密码错误，请先注册')
        else:
            flash('填入的参数有误，或者您尚未注册')
    return render_template("login2.html",form=login_form)

'''
<>定义一个理由是参数<>内需要起名字
使用同一个视图函数，来显示不同用户的订单信息
'''
@app.route('/order/<int:order_id>')
def get_order_id(order_id):
    #
    return 'order_id is %s' % order_id


'''
注册接口
'''
@app.route('/register',methods=['GET','POST'])
def register():
    register_Form=Register_Form()
    if register_Form.validate_on_submit():
        user=Users(name=register_Form.username.data,password=register_Form.password.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        #flash('注册成功')
        return redirect(url_for('login'))
    return render_template('register.html',form=register_Form)

'''
给模板传递消息
flash-->需要对内容加密
模板中需要遍历
'''


'''
定义路由及其视图函数
flask中定义路由是通过装饰器实现的
启动程序
'''
if __name__ == '__main__':

    # 删除表
    db.drop_all()
    # #创建表
    db.create_all()
    #
    # user1 = User(name = 'Wang',password ='123456')
    # user2 = User(name='Li', password='123456')
    # db.session.add_all([user1,user2])
    # db.session.commit()

    #执行App.run 就会将flask程序运行在一个建议的服务器上（Flask提供）
    app.run(host='0.0.0.0', threaded=True)
