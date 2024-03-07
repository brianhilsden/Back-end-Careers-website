from jobs import app,db
from flask import render_template,request,redirect,url_for,flash
from jobs.database import load_jobs_from_db,load_job_from_db,add_to_database,add_new_jobs,load_applications,save_edited_job,delete_job,Admin
from flask_login import login_user,logout_user,login_required,current_user
from jobs.accounts import Registration,Login

@app.route("/data")
def frontend():
   jobs=load_jobs_from_db()
   titles=["id","Job","Location","Salary","Currency","Responsibilities","Requirements"]
   newjobs=[]
   for job in jobs:
     item=dict(zip(titles,job))
     newjobs.append(item)
   return newjobs

@app.route("/")
def home_page():
  return render_template('home.html')


@app.route("/register",methods=['POST','GET'])
def registration():
  form =Registration()
  if form.validate_on_submit():
    new_user=Admin(username=form.username.data,email_address=form.email_address.data,password=form.setPassword.data)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    flash(f'Admin account created.You are logged in as {new_user.username}',category='success')
    return redirect(url_for('jobs_page'))
  if form.errors !={}:
    for err_msg in form.errors.values():
      flash(f'{err_msg[0]}',category='danger')
  return render_template('register.html',form=form)

@app.route("/login",methods=["POST","GET"])
def login():
  form=Login()
  if form.validate_on_submit():
    attempted_user=Admin.query.filter_by(username=form.username.data).first()
    if attempted_user and attempted_user.confirm_password(attempted_password=form.password.data):
      login_user(attempted_user)
      return redirect(url_for('jobs_page'))
    else:
      flash('Username and password do not match',category='danger')
  return render_template('login.html',form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash ("You have been successfully logged out",category='info')
  return redirect(url_for("home_page"))

@app.route("/jobs")
@login_required
def jobs_page():
   jobs=load_jobs_from_db()
   return render_template('index.html',jobs=jobs)


@app.route("/newJobs")
@login_required
def new_job():
  return render_template('new_jobs.html')

@app.route("/jobAdded",methods=["POST"])
@login_required
def added_job():
  job=request.form.to_dict()
  add_new_jobs(job)
  return render_template("addedJobs.html",jobs=job)


@app.route("/viewApplications")
@login_required
def application_data():
   applications=load_applications()
   return render_template("view_applications.html",applications=applications)


@app.route("/job/<id>")
@login_required
def show_job(id):
  job=load_job_from_db(id)
  return render_template('jobpage.html',id=job[0], title=job[1],location=job[2],salary=job[3],currency=job[4],responsibilities=job[5],requirements=job[6])

@app.route("/job/<id>/edit")
@login_required
def edit_job(id):
  job=load_job_from_db(id)
  return render_template('edit_job.html',id=job[0], title=job[1],location=job[2],salary=job[3],currency=job[4],responsibilities=job[5],requirements=job[6])

@app.route("/jobEdited/<id>",methods=["POST"])
@login_required
def edited_job(id):
  job=request.form.to_dict()
  save_edited_job(job,id)
  return render_template('editedJobs.html',jobs=job)

@app.route("/deleted/<id>")
@login_required
def deleted_job(id):  
  job=load_job_from_db(id)
  delete_job(id)
  return render_template('deletedjob.html',title=job[1])

@app.route("/job/<id>/apply",methods=["post"])
@login_required
def apply_to_job(id):
  data=request.form.to_dict()
  job=load_job_from_db(id)
  add_to_database(id,data)
 
  return render_template('application_submitted.html',application=data,job=job)
