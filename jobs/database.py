from sqlalchemy import create_engine,text
from jobs import db,login_manager,bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(Admin_id):
  return Admin.query.get(Admin_id)

class Admin(db.Model, UserMixin):
  id=db.Column(db.Integer(),primary_key=True)
  username=db.Column(db.String(length=30))
  email_address=db.Column(db.String(length=70))
  password_hash=db.Column(db.String(length=60),nullable=False)
  
  @property
  def password(self):
    return self.password
  
  @password.setter
  def password(self,plain_text_password):
     self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
     
  
  def confirm_password(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password)
  

class Applicants(db.Model):
  id=db.Column(db.Integer(),primary_key=True)
  email=db.Column(db.String(length=70))
  passwordApp=db.Column(db.String(length=50))
  @property
  def password(self):
    return self.password
  
  @password.setter
  def password(self,plain_text_password):
     self.passwordApp=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
     
  
  def confirm_password(self, attempted_password):
    return bcrypt.check_password_hash(self.passwordApp, attempted_password)


engine = create_engine("mysql+pymysql://root:-BgbEEE646GGeEF-Fg316DAG2ff55Gce@roundhouse.proxy.rlwy.net:51741/railway?charset=utf8mb4")
""" engine = create_engine("mysql+pymysql://avnadmin:AVNS_cVN41Ne4egx4yWk35tZ@mysql-7a9d636-royalty-inc20.a.aivencloud.com:16051/defaultdb?charset=utf8mb4") """
""" engine = create_engine("mysql+pymysql://root:Royalty20@127.0.0.1:3306/sys?charset=utf8mb4") """


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs=result.all()
    return jobs
  
def load_applications():
  with engine.connect() as conn:
    result=conn.execute(text("SELECT * from applications"))
    applications=result.all()
    return applications
  
def load_job_from_db(id):
  with engine.connect() as conn:
    result=conn.execute(text(f'(select * from jobs where id={id})'))
    rows=result.all()
    return rows[0]
    
def add_to_database(applic):
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO applications(job_id,applicant_id,full_name,email,github)VALUES(:job_id,:applicant_id,:name,:email,:github)"),{"job_id":applic['jobId'],"applicant_id":applic['applicantId'],"name":applic['name'],
    "email":applic['email'],"github":applic['github']})
    conn.commit()

def add_new_jobs(job):
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO jobs(title,location,salary,currency,responsibilities,requirements) VALUES(:title,:location,:salary,:currency,:responsibilities,:requirements)"),
                 {"title":job['Title'],"location":job['Location'],"salary":job['Salary'],"currency":job["Currency"],"responsibilities":job["Responsibilities"],"requirements":job["Requirements"]}) 
    conn.commit()
              
def save_edited_job(job,id):
  with engine.connect() as conn:
    conn.execute(text("UPDATE jobs SET title=:title,location=:location,salary=:salary,currency=:currency,responsibilities=:responsibilities,requirements=:requirements WHERE id=:id"),
                 {"title":job['Title'],"location":job['Location'],"salary":job['Salary'],"currency":job["Currency"],"responsibilities":job["Responsibilities"],"requirements":job["Requirements"],"id":id})
    conn.commit()

def delete_job(id):
  with engine.connect() as conn:
    conn.execute(text("DELETE FROM jobs WHERE id=:id"),{"id":id})
    conn.commit()