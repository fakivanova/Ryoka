from datetime import datetime
from pprint import pprint
from flask import session, redirect, url_for, render_template
import flask_sqlalchemy
from .. import db
from ..models import User
from .forms import NameForm
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        pprint(flask_sqlalchemy.get_debug_queries())
        return redirect(url_for('.index'))
    return render_template('index.html',
                                 form=form,
                                 known=session.get('known', False),
                                 name=session.get('name'),
                                 current_time=datetime.utcnow())
