from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app =Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(20),nullable=False)
    age = db.Column(db.Integer,nullable =False)
    phone =db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<Customer %r>' %self.id 

@app.route('/',methods=['POST','GET'])
def register():
    if request.method =='POST':
        cust_id=request.form['cust_id']
        cust_name = request.form['cust_name']
        cust_age = request.form['cust_age']
        cust_phone = request.form['cust_phone']
        cust_addr = request.form['cust_addr']
        customer =Customer(id=cust_id,name=cust_name,age=cust_age,phone=cust_phone,address=cust_addr)
        try:
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            return 'Customer ID already exist'
       

    else:
        return render_template('register.html')

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    entry = Customer.query.all()
    return render_template('dashboard.html',entry = entry)

@app.route('/delete/<int:id>')
def delete(id):
    cust_to_delete = Customer.query.get_or_404(id)
    try:
        db.session.delete(cust_to_delete)
        db.session.commit()
        return redirect(url_for('dashboard'))
    except:
        return 'There was some issue in deletion'

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    cust_to_update = Customer.query.get_or_404(id)
    if request.method =='POST':
        cust_to_update.cust_phone= request.form['cust_phone']
        cust_to_update.cust_addr= request.form['cust_addr']

        try:
            db.session.commit()
            return redirect(url_for("dashboard"))
        except:
           return 'There was an issue updating the information'

        
    else:
        return render_template('custupdate.html',customers=cust_to_update)

        


if __name__=="__main__":
    app.run(debug=True)