from os import abort

from chat_app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, current_app, request
from chat_app.forms import RegistrationForm, LoginForm, MessageFrom
from chat_app.models import User, get_all_users, Message
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully.", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=register_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('chat'))
    return render_template('login.html', form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logout", 'success')
    return redirect(url_for('login'))


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash("Please login")
        return redirect(url_for('login'))
    message_form = MessageFrom()
    if message_form.validate_on_submit():
        if Message.query.filter_by(receiver=message_form.receiver.data):
            message = Message(receiver=message_form.receiver.data, subject=message_form.subject.data,
                              content=message_form.content.data, author=current_user)
            db.session.add(message)
            db.session.commit()
            return 'sent'
        else:
            return redirect(url_for('chat'))

    return render_template('chat.html', form=message_form, users=get_all_users())


@app.route("/inbox/sent", methods=['GET', 'POST'])
@login_required
def inbox_sent():
    x = current_user.id
    posts = db.engine.execute(f'select * from Message where user_id ={x}')
    return render_template('sent.html', po=posts)


@app.route("/inbox/receive", methods=['GET', 'POST'])
@login_required
def inbox_receiver():
    posts = db.engine.execute('select * from Message')
    return render_template('inbox.html', po=posts)


@app.route("/message/<int:msg_id>/delete", methods=['POST', 'GET', 'DELETE'])
@login_required
def delete(msg_id):
    msg = Message.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('deleted')
    return redirect(url_for('chat'))


