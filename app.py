from flask import Flask,render_template,request,session, redirect
import mysql.connector
import numpy as np
import pickle
import datetime
from flask_mail import Mail, Message



filename = 'heart-prediction-model.pkl'
model=pickle.load(open(filename, 'rb'))




app=Flask(__name__)
app.secret_key ="Rahul"
# ----------------------------------------------------mail-----------------------------------------------------------------
app.config['SECRET_KEY'] = 'Rahul'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fitheart2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'ufyizsxtfbwntfgp'

mail=Mail(app)




# ---------------------Home-----------------------------

@app.route("/")
def home():
    return render_template("index.html")
# ---------------------Sigup-----------------------------
@app.route("/register")
def reg():

    return render_template("register.html")
@app.route("/sigup", methods=["post"])
def New():
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    password=request.form['pass']
    con=mysql.connector.connect(host='localhost',user='root', database='heart',password='Rahul@123')
    cur=con.cursor()
    cur.execute("insert into users(name,email,pwd,contact) values('"+name+"','"+email+"','"+password+"','"+phone+"')" )
    con.commit()
    
    return redirect("/login")


# ----------Login--Page-------------
@app.route("/login")
def sigin():
    return render_template("login.html")

@app.route("/access",methods=["post"])
def check(): 
    if request.method =="POST":

       username=request.form['eml']
       password=request.form['pas']
       con=mysql.connector.connect(host='localhost',user='root',database='heart',password='Rahul@123')
       cur=con.cursor()
       cur.execute("select * from users where email='"+username+"' and pwd='"+password+"'    ")
       user=cur.fetchone()

       if user is None:

           return render_template('register.html',error='Invalid User')
       else:

            session['logged_in']=True
            session["username"]=username
       
            return render_template("index1.html",user=user)

# -------------------------------------About----------------------------------------------------------
@app.route("/about")
def about():
    con=mysql.connector.connect(host='localhost',user='root',database='heart',password='Rahul@123')
    cur=con.cursor()
    cur.execute("select * from feedback")
    data=cur.fetchall()
    return render_template("about.html", data=data)


# --------------------------------------contact page ------------------------------------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/msg",methods=["post"])
def send_message():
    if request.method=="POST":
        email=request.form['emal']
        name=request.form['nam']
        phone=request.form['num']
        message=request.form['txt']
        msg = Message(
        'New Contact Form Submission',
        sender='fitheart2023@gmail.com',
        recipients=[email,'paalrahul2001@gmail.com'] ,
        body=f'Name: {name}\nEmail: {email}\nPhone Number:{phone}\nYour Message: {message}'
    )
        mail.send(msg)
        sdd="Thanks You"
    
    return  redirect("/")


# -----------------------------------Dashboard--------------------------------------------------------------------

  


@app.route("/user_pannel")
def useer():
    if 'logged_in' not in session:
        return redirect("/login")
    con=mysql.connector.connect(host='localhost',user='root',database='heart',password='Rahul@123')
    cur=con.cursor()
    cur.execute("select * from users where email='"+session["username"]+"'")
    user=cur.fetchone()

    return render_template("index1.html" ,user=user)

@app.route("/prediction",methods=["post"])
def model():
    if request.method=="POST":
        cdate=datetime.date.today()
        age=int(request.form['age'])
        sex=request.form.get('sex')
        cp=request.form.get('cp')
        trestbps=int(request.form['trestbps'])
        chol=int(request.form['chol'])
        fbs=request.form.get('fbs')
        restecg=request.form.get('restecg')
        thalach=int(request.form['thalach'])
        exang=request.form.get('exang')
        oldpeak=float(request.form['oldpeak'])
        slope=request.form.get('slope')
        ca=int(request.form['ca'])
        thal=request.form.get('thal')


        data=np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        prediction=model.predict(data)

        if prediction==0:
            res="Normal"
        else:
            res="Heart Issue"
        con=mysql.connector.connect(host='loaclhost',user='root',database='heart',password='Rahul@123')
        cur=con.cursor()
        cur.execute("insert into heart_attack_data(date_created,age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,user,result) values('"+cdate+"','"+age+"','"+sex+"','"+cp+"','"+trestbps+"','"+chol+"','"+fbs+"','"+restecg+"','"+thalach+"','"+exang+"','"+oldpeak+"','"+slope+"','"+ca+"','"+thal+"','"+session["username"]+"','"+res+"')")
        con.commit()
        cur.close()

        return render_template('result.html',prediction=prediction)
    



    # -----------------------------------------logout-------------------------------------------------------------------------

@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect("/")


# -----------------------------------------------------------History-------------------------------------------------------------


@app.route("/history")
def hist():
    if 'logged_in' not in session:
        return redirect("/login")
    
    con=mysql.connector.connect(host='localhost',user='root',database='heart',password='Rahul@123')
    cur=con.cursor()
    cur.execute("select * from heart_attack_data where user='"+session["username"]+"'")
    user=cur.fetchall()
    return render_template('table.html',data=user)


@app.route("/feed")
def fdb():
    if 'logged_in' not in session:
        return redirect('/login')
    
    return render_template('form.html')
@app.route("/feedback",methods=["post"])
def feedback():
    if request.form=="POST":

        name=request.form['name']
        email=request.form['email']
        rating=request.form['rating']
        comments= request.form['comments']
        con=mysql.connector.connect(host='localhost',user='root',database='heart',password='Rahul@123')
        cur=con.cursor()
        cur.execute("insert into feedback(name,email,rating,comments) values('"+name+"','"+email+"','"+rating+"','"+comments+"')")
        con.commit()

        return render_template('form.html')
        

    
















































if __name__=="__main__":
    app.run(debug=True)