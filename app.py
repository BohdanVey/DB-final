from flask import Flask, render_template, redirect, request, url_for, flash
import os
from db.alien import Alien
from db.person import Person
from db.ship import Ship
from forms import *

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/alien')
def alien():
    aliens = Alien().get_all()
    print(aliens)
    return render_template('alien.html', length=len(aliens), alien=aliens)


@app.route('/person')
def persons():
    person = Person().get_all()
    print(person)
    return render_template('person.html', length=len(person), person=person)


@app.route('/person/<person_id>')
def person_page(person_id):
    person = Person().get_by_id(person_id)
    full_name = person[1] + ' ' + person[2]
    texsts = [
        ['Escape from ship', 0],
        [f'Make experiment on {full_name}', 1],
        ['Kill alien', 2],
        [f"Get all ships for {full_name} he visit in specific time", 3],
        [f"Get all aliens {full_name} was stolen at least N times in specific time", 4],
        [f"Get all aliens, which was killed by {full_name} in specific time", 5],
        [f"Get all aliens which stole {full_name} and was killed by this person", 6],
        [f"Get mutual excursion for {full_name} and specific alien", 7],
        [f"Get all experiment on {full_name}, where was at least N aliens", 8]
    ]

    return render_template('info.html', length=len(texsts), texsts=texsts, special_id=person_id)


@app.route('/alien/<alien_id>')
def alien_page(alien_id):
    alien = Alien().get_by_id(alien_id)
    full_name = alien[1] + ' ' + alien[2]
    texsts = [
        ['Still person', 100],
        ['Transfer person to another ship', 101],
        ['Make excursion for peoples', 102],
        [f"Get all people for {full_name} he still at least N time in specific time", 103],
        [f"Get mutual excursion for {full_name} and specific person", 104],
        [f"Get all excursion of {full_name}, where was at least N person", 105],
        [f"Get all ships in descending order of total number of experiments with {full_name} in specific time", 106]
    ]
    return render_template('info.html', length=len(texsts), texsts=texsts, special_id=alien_id)


@app.route('/general')
def general_page():
    texsts = [
        ["Get all aliens, which still at least N people at specific time", 200],
        ["Get all peoples, which was stolen at least N times at specific time", 201],
        ["Get total number of abductions during months", 202],

    ]
    return render_template('info.html', length=len(texsts), texsts=texsts, special_id=0)


@app.route('/add/person', methods=["GET", "POST"])
def add_person():
    form = AddFormPerson(request.form)
    if request.method == 'POST' and form.validate():
        print(form.name)
        Person().add_person(form.name.data, form.surname.data, form.url.data)
        return redirect('/')
    return render_template('add.html', form=form, button_text="Add User")


@app.route('/add/alien', methods=["GET", "POST"])
def add_alien():
    form = AddFormAlien(request.form)
    if request.method == 'POST' and form.validate():
        Alien().add_alien(form.name.data, form.surname.data, form.url.data)
        return redirect('/')
    return render_template('add.html', form=form, button_text="Add Alien")


@app.route('/add/ship', methods=["GET", "POST"])
def add_ship():
    form = AddFormShip(request.form)
    if request.method == 'POST' and form.validate():
        Ship().add_ship(form.name.data)
        return redirect('/')
    return render_template('add.html', form=form, button_text="Add Ship")


@app.route('/question/<question_id>/<alive_id>', methods=["GET", "POST"])
def question(question_id, alive_id):
    alive_id = int(alive_id)
    question_id = int(question_id)
    form = None
    text = None
    flash_text = ""
    data = dict()
    if 200 > question_id >= 100:
        alien = Alien().get_by_id(alive_id)
        data['alien'] = alive_id
        full_name = alien[1] + ' ' + alien[2]
        if question_id == 100:
            flash_text = "Person successfully stolen"
            form = StillForm(request.form)
            text = f"Still person for {full_name}"
        if 'person' in form:
            form.person.choices = [[x[0], x[1] + ' ' + x[2]] for x in Person().get_all()]
        if 'ship' in form:
            form.ship.choices = [[x[0], x[1]] for x in Ship().get_all()]
        if 'alien' in form:
            form.alien.choices = [[x[0], x[1] + ' ' + x[2]] for x in Alien().get_all()]
    if request.method == "POST":
        if 'person' in form:
            data['person'] = int(form.person.data)
        if 'ship' in form:
            data['ship'] = int(form.ship.data)
        if 'datetime_' in form:
            data['datetime_'] = form.datetime_.data
        if form.validate():
            form.submit(data)
        else:
            return render_template("question.html", form=form, name=text)
        flash(flash_text)
        return redirect('/')
    return render_template("question.html", form=form, name=text)


if __name__ == '__main__':
    app.run(debug=True)
