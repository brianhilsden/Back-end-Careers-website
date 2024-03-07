from sqlalchemy import create_engine,text
""" engine = create_engine("mysql+pymysql://root:-BgbEEE646GGeEF-Fg316DAG2ff55Gce@roundhouse.proxy.rlwy.net:51741/railway?charset=utf8mb4") """

engine = create_engine("mysql+pymysql://avnadmin:AVNS_cVN41Ne4egx4yWk35tZ@mysql-7a9d636-royalty-inc20.a.aivencloud.com:16051/defaultdb?charset=utf8mb4")
with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs=result.all()
    titles=["id","Job","Location","Salary","Currency","Responsibilities","Requirements"]
    newjobs=[]
    for job in jobs:
       item=dict(zip(titles,job))
       newjobs.append(item)
        
    print(newjobs)




""" def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from applications"))
    jobs=result.all()
    return jobs
  
print(load_jobs_from_db()) """