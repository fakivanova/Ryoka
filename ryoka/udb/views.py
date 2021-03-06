from flask import render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..udbmodels import Base, Disease, Equipment, Employee, Degree
from .. import db
from . import udb
from .forms import (DiseaseForm, EquipmentForm, EmployeeForm, EmployeeEquipmentForm,
                    EmployeeDiseaseForm)

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

@udb.route('/employees', methods=['POST', 'GET'])
@login_required
def employees():
    form = EmployeeForm()
    udb_session = current_user.session
    form.degree.choices = [(degree.id, degree.name) 
                           for degree in udb_session.query(Degree).order_by(Degree.name).all()]
    employees = udb_session.query(Employee).order_by(Employee.name).all()

    employeeEquipmentForm = EmployeeEquipmentForm()
    employeeEquipmentForm.name.choices = [(employee.id, employee.name) for employee in employees]
    employeeEquipmentForm.equipment.choices = [(equipment.id, equipment.name)
        for equipment in udb_session.query(Equipment).order_by(Equipment.name).all()]

    employeeDiseaseForm = EmployeeDiseaseForm()
    employeeDiseaseForm.name.choices = [(employee.id, employee.name) for employee in employees]
    employeeDiseaseForm.disease.choices = [(disease.id, disease.name)
        for disease in udb_session.query(Disease).order_by(Disease.name).all()]


    if form.validate_on_submit():
        employee = Employee(name=form.name.data,
                            experience=form.experience.data,
                            degree=udb_session.query(Degree).get(form.degree.data))
        udb_session.add(employee)
        udb_session.commit()
        return redirect(url_for('.employees'))

    if employeeEquipmentForm.validate_on_submit():
        employee = udb_session.query(Employee).get(employeeEquipmentForm.name.data)
        employee.equipments.append(udb_session.query(Equipment).get(employeeEquipmentForm.equipment.data))
        udb_session.add(employee)
        udb_session.commit()
        return redirect(url_for('.employees'))

    if employeeDiseaseForm.validate_on_submit():
        employee = udb_session.query(Employee).get(employeeDiseaseForm.name.data)
        employee.diseases.append(udb_session.query(Disease).get(employeeDiseaseForm.disease.data))
        udb_session.add(employee)
        udb_session.commit()
        return redirect(url_for('.employees'))
        
    return render_template('udb/employees.html', form=form, employees=employees,
                           employeeEquipmentForm=employeeEquipmentForm,
                           employeeDiseaseForm=employeeDiseaseForm)

@udb.route('/history')
@login_required
def history():
    entries = [entry.entry for entry in current_user.udb_entries]
    current_user.udb_entries.clear()
    db.session.commit()
    return jsonify(entries)
