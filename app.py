from hack import app, create_db,db
from flask import render_template, redirect, url_for, send_from_directory, request, abort
from flask_login import current_user, login_required, login_user, logout_user
from hack.forms import FileForm, LoginForm, RegForm, RepoForm
from hack.models import File, User, Repo
from werkzeug.security import check_password_hash, generate_password_hash
import os

app.config['UPLOAD_FOLDER'] = 'hack/static/uploads/'

create_db(app)

# @app.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     form = FileForm()
#     if form.validate_on_submit():
#         fname = form.file_name.data
#         file = request.files['file']
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
#         new_file = File(file_name=fname, file=file_path, uploader=current_user.id)
#         db.session.add(new_file)
#         db.session.commit()
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
#     return render_template('index.html', form=form)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createrepo', methods=['GET', 'POST'])
@login_required
def create_repo():
    form = RepoForm()
    if form.validate_on_submit():
        name = form.name.data
        private = form.private.data
        new_repo = Repo(name=name, is_private=private, user=current_user.id, files=[])
        db.session.add(new_repo)
        db.session.commit()
        return redirect('/')
    return render_template('create_repo.html', form=form)

@app.route('/viewrepo/<id>', methods=['GET', 'POST'])
@login_required
def view_repo(id):
    repo = Repo.query.filter_by(id=id).first()
    form = FileForm()
    if form.validate_on_submit():
         fname = form.file_name.data
         file = request.files['file']
         file_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
         new_file = File(file_name=fname, file=file_path, uploader=current_user.id)
         db.session.add(new_file)
         db.session.commit()
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
         repo.files.append(new_file)

    return render_template('view_repo.html', repo=repo, form=form)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            mess = 'Account already exists'
        else:
            new_user = User(email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('home'))

    if current_user.is_authenticated:
        return abort(404)
    return render_template('reg.html', form=form, mess=mess)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            mess = 'Email not found'
        else:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                mess = 'Incorrect password'
    if current_user.is_authenticated:
        return abort(404)

    return render_template('login.html', mess=mess, form=form)

@app.route('/view/<id>')
@login_required 
def view(id):
    file = File.query.filter_by(id=id).first()
    return send_from_directory('static/uploads/', file.file_name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/delete/<id>')
@login_required
def delete(id):
    file = File.query.filter_by(id=id).first()
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/deleterepo/<id>')
@login_required
def delete_repo(id):
    repo = Repo.query.filter_by(id=id).first()
    db.session.delete(repo)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/user/<id>')
def view_user(id):
    user = User.query.filter_by(id=id).first()
    repos = user.repos
    # for i in repos:
    #     if i.is_private == 1:
    #         if current_user.id != i.user:
    #             return abort(404)
    #         else:
    #             return render_template('view_user.html', user=user)
    return render_template('view_user.html', repos=repos,user=user)

@app.route('/view_users')
def view_all_users():
    users = User.query.all()
    return render_template('allusers.html', users=users)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    print("i totally did not write this to make the python percent on github 69")

