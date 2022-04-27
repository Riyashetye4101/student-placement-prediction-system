from flask import Flask,render_template,redirect,url_for,request
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
# creating a classifier using sklearn
from sklearn.linear_model import LogisticRegression

application=Flask(__name__)
application.config['SECRET_KEY']='3483dd03f2cb409aba821cd2a27c64b3'

def calulate(lst):
	dataset = pd.read_csv('newdata.csv')
	# selecting the features and labels
	X = dataset.iloc[:, :-1].values
	Y = dataset.iloc[:, -1].values
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.2)
	clf = LogisticRegression(random_state=0, solver='lbfgs',max_iter=1000).fit(X_train,Y_train)
	# printing the acc
	clf.score(X_test, Y_test)
	# predicting for random value
	Y_pred=clf.predict([[lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6]]])
	return Y_pred[0]


@application.route('/test')
def home():
	return render_template('index.html')

@application.route('/')
def aboutus():
	return render_template('/aboutus.html')

@application.route('/go',methods=['GET','POST'])
def go():
	skl=request.form['skill']
	lst=[int(request.form['age']),int(request.form['gender']),int(request.form['stream']),int(request.form['intern_no'])
	,float(request.form['cgpa']),0,int(request.form['backlog'])]
	if len(skl)!=0:
		skills=request.form['skill'].split(",")
	else:
		skills='no skill found'
		
	detail={
		'username':request.form['username'],'intern_type':request.form['intern_type'],
		 'intern_details':request.form['intern_details'],'skills':skills,
		 'age':lst[0],'cgpa':lst[4],'intern_no':lst[3]
	}
	stream={
		"0":'Electronics And Communication',
		"1":'Computer Science',
        "2":'Information Technology',
        "3":'Mechanical',
        "4":'Electrical',
        "5":'Civil'
	}
	detail['stream']=stream[str(lst[2])]
	if lst[1]==1:
		detail['gender']='Female'
	else:
		detail['gender']='Male'

	if request.form['backlog']==1:
		return render_template('/demo.html',detail=detail,lst=lst)
	else:
		result=calulate(lst)
		if result==1:
			mssg='yes'
		else:
			mssg='no'
		return render_template('/result.html',detail=detail,mssg=mssg)

@application.route('/result',methods=['GET','POST'])
def result():
	lst=[int(request.form['age']),int(request.form['gender']),int(request.form['stream']),int(request.form['intern'])
	,float(request.form['cgpa']),0,int(request.form['backlog'])]
	result=calulate(lst)
	if result==1:
		string="Congratulation! you can able to get the placement based on your academic data"
	else:
		string="Sorry to say but you need to improve yourself"

	return render_template('result.html',mssg=string)

if __name__ == '__main__':
	application.run(debug=True)
