import flask
from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
#initialize flask
app=Flask(__name__)
#database configurations
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:admin123@localhost/staff_management'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
#initialize database
db=SQLAlchemy(app)
#define staff model
class staff(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    designation=db.Column(db.String(100),nullable=False)
    dept=db.Column(db.String(100),nullable=False)
    salary=db.Column(db.Float(10,2),nullable=False)
    def __str__(self) -> str:  
        return super().__str__()
#route for home page
@app.route('/')
def home():
    StaffData=staff.query.all()
    return render_template('index.html',sData=StaffData)

@app.route('/add',methods=['Post'])
def add_staff():
    #adding to database logic here
    sName=request.form['staffName']
    sDesig=request.form['designation']
    sDept=request.form['dept']
    sSal=request.form['salary']
    #create new staff record
    new_staff=staff(name=sName,designation=sDesig,dept=sDept,salary=sSal)
    db.session.add(new_staff)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit<int:id>',methods=['POST','GET'])
def edit_staff(id):
    sData=staff.query.get_or_404(id)
    if request.method =='POST':
        sData.name=request.form['name']
        sData.designation=request.form['designation']
        sData.dept=request.form['dept']
        sData.salary=request.form['salary']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',staff=sData)

@app.route('/delete<int:id>',methods=['POST'])
def delete_staff(id):
    sData=staff.query.get_or_404(id)
    db.session.delete(sData)
    db.session.commit()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)