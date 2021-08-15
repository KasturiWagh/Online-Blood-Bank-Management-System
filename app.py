from flask import Flask, redirect, url_for, request,render_template,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///info.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Donername = db.Column(db.String(200), nullable=False)
    bloodT = db.Column(db.String(500), nullable=False)
    contactME = db.Column(db.String(500), nullable=False)
 
    def __repr__(self) -> str:
        return f"{self.sno} - {self.Donername}"





#Main page
@app.route('/' ,methods=['GET', 'POST'],)
def hello_world():
    if request.method == 'POST':
        if request.form.get('action1') == 'Doner':
            return render_template('doner.html')
             # do something
        elif  request.form.get('action2') == 'Patient':
            pass 
            return render_template('patient.html')
            # do something
        else:
            pass # unknown

    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

# DONER
@app.route('/successDoner/<Donername>/<bloodT>/<contactME>')
def success( Donername, bloodT, contactME):
    print(Donername)
    print(bloodT)
    print(contactME)
    

    info = Info( Donername = Donername , bloodT = bloodT ,contactME = contactME)
    db.session.add(info)
    db.session.commit()
    allinfo = Info.query.all()
    return render_template('infotable.html', allinfo = allinfo)


@app.route('/doner', methods = ['POST' , 'GET'])
def Donation():
    if request.method == 'POST':
        print("hello doner")
        user = request.form['nm']
        user2 = request.form['blood']
        user3 = request.form['contact']
        return redirect(url_for('success', Donername = user , bloodT = user2 ,contactME = user3))
    else:
        return render_template('doner.html')


#Patient 
@app.route('/successpatient/<Patientname>')
def successD(Patientname):
   return 'welcome %s' % Patientname

@app.route('/patient', methods = ['POST' , 'GET'])
def patient():
    if request.method == 'POST':
        user = request.form['nm']
        user2 = request.form['contact']
        return redirect(url_for('show', NAME = user , CONTACT = user2))
    else:
        return render_template('patient.html')


#this route is just to check the information site table nothing else
@app.route('/show/<NAME>/<CONTACT>')
def show(NAME,CONTACT):
   info = Info(  Donername = "Name", bloodT = "Blood type" ,contactME = "123456789")
   allinfo = Info.query.all()
   return render_template('infotable2.html', allinfo = allinfo , NAME = NAME , CONTACT = CONTACT)



@app.route('/remove')
def pp():
    info = Info(  Donername = "Name", bloodT = "Blood type" ,contactME = "123456789")   
    allinfo = Info.query.all()
    return render_template('infotable.html', allinfo = allinfo)
    


@app.route('/delete/<int:sno>')
def delete(sno):
    info = Info.query.filter_by(sno=sno).first()
    db.session.delete(info)
    db.session.commit()
    return redirect('/remove')

@app.route('/information')
def information():
    return render_template('information.html')
   

@app.route('/donerINFO')
def donerINFO():
    return render_template('donerINFO.html')


@app.route('/bloodBank')
def bloodBank():
    return render_template('bloodBank.html')

@app.route('/sendRequest/<int:sno>/<NAME>/<CONTACT>')
def sendRequest(sno,NAME,CONTACT):
    info = Info.query.filter_by(sno=sno).first()
    return render_template('sendRequest.html', info = info , NAME = NAME , CONTACT = CONTACT)


@app.route('/list3')
def pp3():
    info = Info(  Donername = "Name", bloodT = "Blood type" ,contactME = "123456789")   
    allinfo = Info.query.all()
    return render_template('infotable3.html', allinfo = allinfo)

if __name__ == '__main__':
   app.run(debug = True, port = 8000)