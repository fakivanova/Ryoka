from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..udbmodels import Base, Disease, Equipment
from .. import db
from . import udb
from .forms import DiseaseForm, EquipmentForm

@udb.route('/initialize', methods=['GET'])
@login_required
def create_all():
    udb_session = current_user.session
    Base.metadata.create_all(udb_session.get_bind())
    return redirect(url_for('main.index'))

@udb.route('/diseases', methods=['POST', 'GET'])
@login_required
def diseases():
    form = DiseaseForm() 
    udb_session = current_user.session
    diseases = udb_session.query(Disease).order_by(Disease.name).all()
    if form.validate_on_submit():
        disease = Disease(name=form.name.data)
        udb_session.add(disease)
        udb_session.commit()
        return redirect(url_for('.diseases'))
    return render_template('udb/diseases.html', form=form, diseases=diseases)

@udb.route('/equipments', methods=['POST', 'GET'])
@login_required
def equipments():
    form = EquipmentForm()
    udb_session = current_user.session
    equipments = udb_session.query(Equipment).order_by(Equipment.name).all()
    if form.validate_on_submit():
        equipment = Equipment(name=form.name.data)
        udb_session.add(equipment)
        udb_session.commit()
        return redirect(url_for('.equipments'))
    return render_template('udb/equipments.html', form=form, equipments=equipments)

@udb.route('/history')
@login_required
def history():
    entries = [entry.entry for entry in current_user.udb_entries]
    current_user.udb_entries.clear()
    db.session.commit()
    return jsonify(entries)
