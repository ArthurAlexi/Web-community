from flask import render_template, url_for, redirect, flash, request, abort
from community import app, dataBase, bcrypt
from community.forms import FormLogin, FormCreateAccount, FormEditProfile, FormPost
from community.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def homepage():
    posts = Post.query.all()
    return render_template('homepage.html', posts=posts)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/users")
@login_required
def showUsers():
    list_users = User.query.all()
    return render_template('users.html', list_users=list_users)


@app.route("/login", methods=['GET', 'POST'])
def login():
    formLogin = FormLogin()
    formCreateAccount = FormCreateAccount()

    if formLogin.validate_on_submit() and 'btnSubmitLogin' in request.form:
        user = User.query.filter_by(email=formLogin.email.data).first()
        if user and bcrypt.check_password_hash(user.password, formLogin.password.data):
            login_user(user, remember=formLogin.remember)
            flash(f'successful login to email: {formLogin.email.data}', category='alert-success')
            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash(f'unsuccessful login to email: {formLogin.email.data}', category='alert-danger')
    if formCreateAccount.validate_on_submit() and 'btnSubmitCreate' in request.form:
        # criar conta
        senha_cry = bcrypt.generate_password_hash(formCreateAccount.password.data)
        user = User(name=formCreateAccount.name.data, email=formCreateAccount.email.data, password=senha_cry)
        # adicionar a sessao
        dataBase.session.add(user)
        # dar commit
        dataBase.session.commit()
        flash(f'account successfully created for email: {formCreateAccount.email.data}', category='alert-success')
        return redirect(url_for('homepage'))
    return render_template('login.html', formLogin=formLogin, formCreateAccount=formCreateAccount)


@app.route("/submitLogin")
def submitLogin():
    return render_template('login.html')


@app.route("/login")
def SubmitNewAcount():
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'Successful logout', category='alert-success')
    return redirect(url_for('homepage'))


@app.route("/profile")
@login_required
def profile():
    photo_profile = url_for('static', filename='photos_profile/{}'.format(current_user.profile_picture))
    return render_template('profile.html', photo_profile=photo_profile)


def salve_picture(img):
    # Add  code
    code = secrets.token_hex(8)
    name, ext = os.path.splitext(img.filename)
    name_arq = name + code + ext
    # reduzir a img
    size = (200, 200)
    img_size = Image.open(img)
    img_size.thumbnail(size)
    # salvar a img na pasta
    path = os.path.join(app.root_path, 'static/photos_profile', name_arq)
    img_size.save(path)

    return name_arq


def editCourses(form):
    temp = []
    for field in form:
        if 'course_' in field.name:
            if field.data:
                temp.append(field.label.text)

    return ';'.join(temp)


@app.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def editProfile():
    form = FormEditProfile()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data

        if form.photo.data:
            name_img = salve_picture(form.photo.data)
            current_user.profile_picture = name_img

        current_user.courses = editCourses(form)
        dataBase.session.commit()
        flash(f'successfully edited profile', category='alert-success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
    photo_profile = url_for('static', filename='photos_profile/{}'.format(current_user.profile_picture))
    return render_template('editProfile.html', photo_profile=photo_profile, form=form)


@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def createPost():
    form = FormPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, id_user=current_user.id)
        dataBase.session.add(post)
        dataBase.session.commit()
        flash('Post created successfully', category='alert-success')
        return redirect(url_for('homepage'))
    return render_template('createPost.html', form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def showPost(post_id):
    post = Post.query.get(post_id)
    if post.id_user == current_user.id:
        form = FormPost()
        if request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            dataBase.session.commit()
            flash('Successfully edited post ', category='alert-success')
            return redirect(url_for('homepage'))
    else:
        form=None
    return render_template('showPost.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        dataBase.session.delete(post)
        dataBase.session.commit()
        flash(' Successfully deleted post', category='alert-success')
        return redirect(url_for('homepage'))
    else:
        abort(403)