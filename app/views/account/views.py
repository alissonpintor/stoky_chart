from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_uploads import UploadNotAllowed
from app import db, imageSet

# Imports dos Forms do Account View
from app.views.account.forms import UpdateUserForm, UpdatePasswordForm

# Import dos Models utilizados na View
from app.models.userAccess import User


account = Blueprint('account', __name__)


@account.route('/')
@login_required
def index():
    title = 'Minha Conta'
    return render_template('account/main.html', title=title)


@account.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id=None):
    form = UpdateUserForm()
    user = User.query.filter_by(id=id).first()

    if user and form.userId.data == 0:
        form.userId.data = user.id
        form.userName.data = user.firstName
        form.userLastName.data = user.lastName
        form.userEmail.data = user.email
        form.userGender.data = user.gender

    if form.validate_on_submit():
        user.firstName = form.userName.data
        user.lastName = form.userLastName.data
        user.email = form.userEmail.data
        user.gender = form.userGender.data

        if form.userImage.data:
            try:
                image = imageSet.save(form.userImage.data)
                user.image = imageSet.url(image)
            except UploadNotAllowed:
                message = {'type': 'warning', 'content': 'Somente Arquivos de Imagens são aceitas'}                
                flash(message)

                return redirect(url_for('account.update', id=id))

        db.session.add(user)
        db.session.commit()

        message = {'type': 'success', 'content': 'Dados alterados com sucesso.'}
        flash(message)

        return redirect(url_for('account.index'))

    content = {
        'title': 'Minha Conta',
        'form': form
    }
    return render_template('account/update.html', **content)


@account.route('/update-password/<int:id>', methods=['GET', 'POST'])
@login_required
def updatePassword(id):
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(id=id).first()
        
        if user and user.verifyPassword(form.currentPassWord.data):
            user.password = form.newPassWord.data
            db.session.add(user)
            db.session.commit()

            message = {'type': 'success', 'content': 'Senha alterada com sucesso.'}
            flash(message)

            return redirect(url_for('account.index'))
        
        else:
            message = {'type': 'error', 'content': 'A Senha Atual está incorreta.'}
            flash(message)

    content = {
        'title': 'Minha Conta',
        'form': form
    }
    return render_template('account/update-password.html', **content)
