import os
import json

import requests
from flask import Flask, render_template, redirect, request

from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from forms.user import RegisterForm
from forms.login import LoginForm

from cell import info_yach
from main import func_api
from testing_time import sr_zn_oborud, for_graph, for_graph_status

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wtf-msi'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/cell/<cell_number>')
def info_yacheika(cell_number):
    cell_number = int(cell_number)
    arr = info_yach(cell_number)
    return render_template('info_yach.html', cell_num=arr[0], name=arr[1],
                           avg_d=arr[2], avg_h=arr[3], int_d=arr[4], int_h=arr[5],
                           data_pie=[round(x, 2) for x in arr[6]], status_cell=arr[7],
                           time_status_d=arr[8], per_d=arr[9], time_status_h=arr[10],
                           per_h=arr[11], status_wait=arr[12], sum_st_wait_d=arr[13][0],
                           per_wait_d=arr[13][1], sum_st_wait_h=round(arr[13][2] / 60), per_wait_h=arr[13][3],
                           for_graph=for_graph_status())


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/all_about')
def abouting():
    x = func_api()
    arr = []
    api_1_count = 'http://roboprom.kvantorium33.ru/api/current'
    for i in range(len(x[1])):
        arr.append(x[1][i][f'Ячейка №{i + 1}'])
    print(arr)
    if x != 'error':
        return render_template('svodka2.html', s1=x[0]['Количество включенных ячеек'],
                               s2=x[0]['Количество выключенных ячеек'],
                               s3=x[0]['Количество ожидающих ячеек'],
                               s4=x[0]['Количество ячеек с ошибкой'], data1=arr[0], data2=arr[1],
                               data3=arr[2], data4=arr[3], data5=arr[4], data6=arr[5],
                               brak=round(requests.get(api_1_count).json()['data'][1]['count_d'] /
                                          requests.get(api_1_count).json()['data'][0][
                                              'count_d'] * 100),
                               kol_vo_brak=requests.get(api_1_count).json()['data'][1]['count_d'],
                               sr_ob=sr_zn_oborud(),
                               graphs=for_graph())
    else:
        return render_template('error.html')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/info')
def informating():
    return 'Hello!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация | РобоПром2023', auth=True,
                                   form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация | РобоПром2023', auth=True,
                                   form=form, message='Электронная почта уже используется')
        elif db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация | РобоПром2023', auth=True,
                                   form=form, message='Имя пользователя уже занято')
        elif form.nickname.data.count(' ') > 0:
            return render_template('register.html', title='Регистрация | РобоПром2023', auth=True,
                                   form=form,
                                   message='Имя пользователя не должно содержать пробелов!')
        user = User()
        user.email = form.email.data
        user.nickname = form.nickname.data

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация | РобоПром2023', auth=True,
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.login.data).first()
        if not user:
            user = db_sess.query(User).filter(User.nickname == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/home')
        return render_template('login.html', title='Войти | РобоПром2023',
                               message='Неверный логин или пароль', auth=True, form=form)
    return render_template('login.html', title='Войти | РобоПром2023', auth=True, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    db_session.global_init('db/knight_users.sqlite')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
