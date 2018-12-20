from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..udbmodels import Base, Disease
from .. import db
from . import udb
from .forms import DiseaseForm

@udb.route('/initialize', methods=['GET'])
@login_required
def create_all():
    udb_session = current_user.session
    Base.metadata.create_all(udb_session.get_bind())
    return redirect(url_for('main.index'))

@udb.route('/add/disease/', methods=['POST', 'GET'])
@login_required
def add_disease():
    form = DiseaseForm() 
    if form.validate_on_submit():
        udb_session = current_user.session
        disease = Disease(name=form.name.data)
        udb_session.add(disease)
        udb_session.commit()
        return redirect(url_for('.add_disease'))
    return render_template('udb/diseases.html', form=form)

@udb.route('/history')
@login_required
def history():
    entries = [entry.entry for entry in current_user.udb_entries]
    current_user.udb_entries.clear()
    db.session.commit()
    return jsonify(entries)
