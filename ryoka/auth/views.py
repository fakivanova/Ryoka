from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db
from .forms import LoginForm, RegistrationForm
from ..models import User
from ..udbmodels import Base, Degree

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Неверный позывной или секретное слово!')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы покинули расположение')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    rank=form.rank.data.lower(),
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        initialize_udb(udb_session)
        flash('Теперь можете предъявить пропуск.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

def initialize_udb(udb_session):
    Base.metadata.create_all(udb_session.get_bind())
    db.session.add_all([Degree(name='Кандидат наук'),
                        Degree(name='Доктор наук')])
    db.session.commit()

