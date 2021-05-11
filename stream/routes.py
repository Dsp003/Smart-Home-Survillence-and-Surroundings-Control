import cv2
import RPi.GPIO as GPIO
from flask import render_template, Response, flash, redirect, url_for
from stream import app, db, bcrypt
from stream.models import accounts, logs, weather
from stream.forms import RegisterForm, LoginForm
from flask_login import login_user, login_required
from random import randint
import pymysql


t, l = [0], [0]
labels = [0]

m_en1 = 22
m_1A = 27
m_2A = 17
led = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

cloud = pymysql.connect(host='database-1.cs6s6dbdkpt2.ap-south-1.rds.amazonaws.com', user='admin', password='z42NkQvEUe8y')
cursor = cloud.cursor()
sql = '''use IoTWeatherSystem'''
cursor.execute(sql)


def insData(temp, light):
    print(f"Inserting values Temperature {temp}, Light {light}")
    sql = '''insert into weatherData (Temperature, Light) values ('%s','%s')''' % (temp, light)
    cursor.execute(sql)
    cloud.commit()


def dispTab():
    print("The table:")
    sql = '''select * from weatherData'''
    cursor.execute(sql)
    print(cursor.fetchall())


def sensor():
    tp, lt = randint(20, 40), randint(0, 10)
    data = weather(temp=tp, light=lt)
    db.session.add(data)
    db.session.commit()
    
    insData(tp, lt)
    
    if tp > 35:
        GPIO.output(m_1A, 1)
        GPIO.output(m_2A, 0)
        GPIO.output(m_en1, 1)
    else:
        GPIO.output(m_1A, 0)
        GPIO.output(m_en1, 0)
        
    if lt < 7:
        GPIO.output(led, 1)
    else:
        GPIO.output(led, 0)
    
    t.append(tp)
    l.append(lt)

    if len(t) > 17:
        t.pop(0)
        l.pop(0)
    else:
        labels.append(labels[-1] + 1)

    return render_template('device.html', t=t, l=l, labels=labels)


@app.route('/')
@app.route('/device', methods=['GET', 'POST'])
@login_required
def device():
    sensor()
    return render_template('device.html', t=t, l=l, labels=labels)


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    video = cv2.VideoCapture(0)

    def gen(vid):
        while True:
            success, image = vid.read()
            ret, jpeg = cv2.imencode('.jpg', image[:, ::-1, :])
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            if cv2.waitKey(1) & 0xFF == 27:
                break

    return Response(gen(video), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_passwd = bcrypt.generate_password_hash(form.passwd.data).decode('utf-8')
        user = accounts(user=form.user.data, email=form.email.data, passwd=hash_passwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.user.data}, account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = accounts.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.passwd, form.passwd.data):
            login_user(user, remember=form.rem.data)
            log = logs(user_id=user.id)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('device'))
        else:
            flash('OOPS!, your email and password does not match', 'danger')
    return render_template('login.html', form=form)


