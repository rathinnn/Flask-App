from flask import Flask, render_template, request, url_for, redirect, flash
import MySQLdb
from datetime import datetime


app = Flask(__name__)
#app.config["DEBUG"] = True

conn = MySQLdb.connect("localhost","rathinn","ayushrlr","shalstor" )
cursor = conn.cursor()



now = datetime.now()


month=now.month
print(month)
year=now.year
day=now.day
daystr=str(day)
if(day<10):
    daystr='0'+str(day)
    






@app.route('/')
def home():
   
  

        
  
      
    return render_template("index.html")

@app.route('/display2',methods=['GET'])
def display2():
    cursor.execute("select *from datesheet ORDER BY s_id DESC LIMIT 15;")
    data = cursor.fetchall()
    

    

    return render_template("display2.html",value=data)

    

    
    
@app.route('/Add/chore',methods=['POST'])
def Addchore():
    msg=''
    if'work' in request.form and 'earned' in request.form:
        details = request.form
        work = details['work']
        earned = details['earned']
        earned=int(earned)
        execution = 'INSERT INTO Balancesheet(typeof, Earned, thedate) VALUES ("%s", %s, curdate());'
        cursor.execute(execution %(work,earned))
        cursor.execute("select *from datesheet ORDER BY s_id DESC LIMIT 1;")
        data = cursor.fetchall()
        data=data[0]
        s_id=int(data[0])
        mont=int(data[1])
        yea=int(data[2])
        due=int(data[3])
        if(year>=yea and month>mont):
            
            execution = 'INSERT INTO datesheet(Mont, Years, Due) VALUES (%s, current_date(), %s);'
            cursor.execute(execution %(month,earned))

        else:
            
            due=due+earned
            
            execution = 'update datesheet Set Due=%s Where s_id=%s;'
            
            cursor.execute(execution %(due,s_id))
            

        
        conn.commit()
        
        

          
    return redirect(url_for('display'))


@app.route('/Add/story',methods=['POST'])
def Addstory():
    msg=''
    if'text' in request.form and 'count' in request.form:
        details = request.form
        text = details['text']
        count2 = details['count']
        cost=int(count2)*0.625
        execution = 'INSERT INTO Balancesheet(typeof, Earned, thedate) VALUES ("Story", %s, curdate());'
        cursor.execute(execution %(cost))
        conn.commit()

          
    return redirect(url_for('display'))

@app.route('/display/',methods=['GET'])
def display():
    msg=''
    cursor.execute("select *from balancesheet ORDER BY s_id DESC LIMIT 15;")
    data = cursor.fetchall()
    

    

    return render_template("display.html",value=data)
    



app.run(host='0.0.0.0')

conn.close()
    
    
