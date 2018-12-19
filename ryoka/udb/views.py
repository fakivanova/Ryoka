from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from ..udbmodels import Base
from . import udb

@udb.route('/initialize', methods=['GET'])
@login_required
def create_all():
    udb_session = current_user.session
    Base.metadata.create_all(udb_session.get_bind())
    return redirect(url_for('main.index'))

