# Importing essential libraries and modules

from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import sqlite3
import pickle
import random
from warnings import filterwarnings
filterwarnings('ignore')
# Load ML model
rft = pickle.load(open('models/rff_TOEFL.pkl', 'rb'))  
rfg = pickle.load(open('models/rff_gre.pkl', 'rb'))  
rfb = pickle.load(open('models/rff_both.pkl','rb'))


# ------------------------------------ FLASK APP -------------------------------------------------
app = Flask(__name__)
###############################################################################################
ur5=['University of Oxford','Stanford University','Massachusetts Institute of Technology','Harvard University','University of Cambridge','California Institute of Technology','Imperial College London','Yale University']
ur4=['University of Toronto','Columbia University','PSL University','The University of Hong Kong','University of California, Los Angeles (UCLA)','The University of EDINBURGH','Australian National University (ANU)','Kings College London']
ur3=['Monash University','The London School of Economics and Political Science (LSE)','Northwestern University','Fudan University','Carnegie Mellon University','University of Amsterdam','Duke University','Sorbonne University']
ur2=['University of California San Diego (UCSD)','University of Illinois at Urbana-Champaign','The University of Warwick','The University of Auckland','Université Paris-Saclay','The University of Western Australia','Brown University','University of Leeds']
ur1=['University of Southampton','Pennsylvania State University','The University of Adelaide','University of Zurich','Universidad de Buenos Aires (UBA)','University of Nottingham','Purdue University','University of St Andrews']

urr=[ur1,ur2,ur3,ur4,ur5]

# render home page


@ app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index11.html')

@app.route('/index12')
def index12():
    return render_template('index.html')


########################################################### LOGIN REGISTER LOGOUT  #############################################

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return render_template('index.html') 
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/home_page')
def home_page():
    return render_template('index.html')

##############################################################################################################################
###########################################################   BOTH    ########################################################

@ app.route('/bothgt')
def bothgt():
    return render_template('both.html')



@ app.route('/both_predict', methods=['POST'])
def both_predict():
    title = 'University Recommended'

    if request.method == 'POST':
        head,typee="GRE AND TOEFL BASED",1
        name = request.form['name']
        val1 = float(request.form['val1'])
        val2 = float(request.form['val2'])
        val3 = int(request.form['val3'])
        val4 = float(request.form['val4'])
        val5 = float(request.form['val5'])
        val6 = float(request.form['val6'])
        val7 = float(request.form['val7'])

        data = np.array([[val1, val2, val3, val4, val5, val6, val7]])
        my_prediction = rfb.predict(data)[0]
        my_prediction=  int(my_prediction*100)
        university_list = random.sample(urr[val3-1], 5)
        ul1=university_list[0]
        ul2=university_list[1]
        ul3=university_list[2]
        ul4=university_list[3]
        ul5=university_list[4]
        return render_template('predict.html', prediction=my_prediction, ul1=ul1,ul2=ul2,ul3=ul3,ul4=ul4,ul5=ul5,head=head,typee=typee,name=name)
    
##############################################################################################################################
###########################################################   GRE    ########################################################


@ app.route('/gre_page')
def gre_page():
    return render_template('gre.html')



@ app.route('/gre_predict', methods=['POST'])
def gre_predict():
    title = 'Admission Recommended'

    if request.method == 'POST':
        head,typee="GRE AND TOEFL BASED",2
        name = request.form['name']
        val1 = float(request.form['val1'])
        val3 = int(request.form['val3'])
        val4 = float(request.form['val4'])
        val5 = float(request.form['val5'])
        val6 = float(request.form['val6'])
        val7 = float(request.form['val7'])

        data = np.array([[val1, val3, val4, val5, val6, val7]])
        my_prediction = rfg.predict(data)[0]
        my_prediction=int(my_prediction*100)
        university_list = random.sample(urr[val3-1], 5)
        ul1=university_list[0]
        ul2=university_list[1]
        ul3=university_list[2]
        ul4=university_list[3]
        ul5=university_list[4]
        return render_template('predict.html', prediction=my_prediction, ul1=ul1,ul2=ul2,ul3=ul3,ul4=ul4,ul5=ul5,head=head,typee=typee,name=name)

##############################################################################################################################
###########################################################   TOEFL    ########################################################

@ app.route('/toefl_page')
def toefl_page():
    return render_template('toefl.html')



@ app.route('/toefl_predict', methods=['POST'])
def toefl_predict():
    title = 'Admission Recommended'

    if request.method == 'POST':
        head,typee="GRE AND TOEFL BASED",3
        # val1 = float(request.form['val1'])
        name = request.form['name']
        val2 = float(request.form['val2'])
        val3 = int(request.form['val3'])
        val4 = float(request.form['val4'])
        val5 = float(request.form['val5'])
        val6 = float(request.form['val6'])
        val7 = float(request.form['val7'])

        data = np.array([[ val2, val3, val4, val5, val6, val7]])
        my_prediction = rft.predict(data)[0]
        my_prediction=int(my_prediction*100)
        university_list = random.sample(urr[val3-1], 5)
        ul1=university_list[0]
        ul2=university_list[1]
        ul3=university_list[2]
        ul4=university_list[3]
        ul5=university_list[4]
        return render_template('predict.html', prediction=my_prediction, ul1=ul1,ul2=ul2,ul3=ul3,ul4=ul4,ul5=ul5,head=head,typee=typee,name=name)




# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)
