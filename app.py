from flask import Flask
from flask import render_template, request
import sqlite3
import yaml
import paho.mqtt.client as mqtt
import json
import pandas as pd
from new_sql import sensor_Data_Handler, delete_sensor_details
from new_sql import add_sensor_details, get_sensor_details, update_sensor_details
from graph_code import display_graph
import time
import datetime
from email_code import trigger_email_alert



app = Flask(__name__)


sampleData = []

config = yaml.load(open("config.yaml"))

# get the value of the broker and topics to subscribe from the config file
broker = config['mqtt']['broker']
Cleint_id = config['mqtt']['client_id']
topic_list = config['list']


def on_message(mqttc, obj, msg):
    sensor_Data_Handler(msg.topic, msg.payload)
    trigger_email_alert()
    data = json.loads(msg.payload)
    sampleData.append(data)
    #print("sampleData: %s"%sampleData)
    #print("MQTT Topic: " + msg.topic)
    print("Data: " + msg.payload)


# function to subscribe all the topics mentioned in config file
def sub_multiple():
    for topic in topic_list:
        mqttc.subscribe(config[topic]['subscribe'], config[topic]['QOS'])


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/loginfarmer', methods = ['POST', 'GET'])
def loginfarmer():
    conn = sqlite3.connect('Cloud281.db')
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            print(username)
            print(password)
            statement = conn.execute('SELECT username FROM farmers')
            msg = "SUCCESS"
            count = -1
            for row in statement:
                count = count + 1
                if username in row:
                    fnstatement = conn.execute("SELECT firstname FROM farmers WHERE username=username")
                    firstname = fnstatement.fetchall()[count][0]
                    lnstatement = conn.execute("SELECT lastname FROM farmers WHERE username=username")
                    lastname = lnstatement.fetchall()[count][0]
                    return render_template('index-farmer.html', firstname=firstname, lastname=lastname)
            conn.close()
        except:
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            conn.close() 

@app.route('/show_graphs', methods = ['POST', 'GET'])
def show_graphs():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        start_date = request.form['StartDate']
        end_date = request.form['EndDate']
        display_graph(s_date=start_date,e_date=end_date,mont=month,saal=year)
        time.sleep(1)
        return render_template('date-range-graph.html')
    
@app.route('/graphical-analysis', methods = ['POST', 'GET'])
def default_graph():
    return render_template('graphical-analysis.html')

#class TestThreading(object):
#    def __init__(self,sensor_type, min_value, max_value):
#        self.sensor_type = sensor_type
#        self.min_value = min_value 
#        self.max_value = max_value
#        thread = threading.Thread(target=self.send_email_alert, args=(self.sensor_type,self.min_value,self.max_value))
#        thread.daemon = True
#        thread.start()
#
#    def send_email_alert(self,sensor_type, min_value, max_value):
#        if str(sensor_type) == "Temperature":
#            loop_flag = get_sensor_details(query="SELECT status FROM sensor_details WHERE type='Temperature'")
#            print(loop_flag)
#            #if loop_flag != None:
#            loop_flag = (loop_flag)[0][0]
#            max_flag = False
#            min_flag = False
#            while str(loop_flag) == "ON":
#                current_temp = get_sensor_details(query="SELECT reading FROM temperature_data ORDER BY id DESC LIMIT 1")
#                current_temp = float(current_temp[0][0])
#                if (current_temp > float(max_value)) and max_flag!=True:
#                    max_flag = True
#                    send_email(current_temp)
#                elif (current_temp < float(min_value)) and min_flag!=True:
#                    min_flag = True
#                    send_email(current_temp)
#                elif (current_temp < float(max_value)) and max_flag==True:
#                    max_flag = False
#                    send_email(current_temp, tag="normal")
#                elif (current_temp > float(min_value)) and min_flag==True:
#                    min_flag = False
#                    send_email(current_temp, tag="normal")
#                loop_flag = get_sensor_details(query="SELECT status FROM sensor_details WHERE type='Temperature'")
#                loop_flag = (loop_flag)[0][0]
#                if str(loop_flag) == "OFF":
#                    break

@app.route('/sensor_control', methods = ['POST', 'GET'])
def sensor_control():
    if request.method == 'POST':
        Stype = request.form['sensorType']
        Slocation = request.form['location']
        MinThreshold = request.form['min_threshold']
        MaxThreshold = request.form['max_threshold']
        now = datetime.datetime.now()
        Sdate_time = now.strftime("%Y-%m-%d %H:%M")
        sensor_dict = {'type': Stype, 'location':Slocation,'min_threshold': MinThreshold,'max_threshold': MaxThreshold, 'date_time':Sdate_time}
        add_sensor_details(sensor_dict)
        #email_thread = threading.Thread(target=send_email_alert, args=('Stype','MinThreshold','MaxThreshold'))
        #email_thread.start()
        #tr = TestThreading(sensor_type=Stype, min_value=MinThreshold, max_value=MaxThreshold)
        #tr.terminate()
        #tr.send_email_alert(sensor_type=Stype, min_value=MinThreshold, max_value=MaxThreshold)
        sensor_data = get_sensor_details(query="SELECT * FROM sensor_details")
        #send_email_alert(sensor_type=Stype, min_value=MinThreshold, max_value=MaxThreshold)
        return render_template('farmer-services.html', sensor_data=sensor_data)
    


    
#def send_email_alert(sensor_type, min_value, max_value):
#    if str(sensor_type) == "Temperature":
#        loop_flag = get_sensor_details(query="SELECT status FROM sensor_details WHERE type='Temperature'")
#        loop_flag = (loop_flag)[0][0]
#        max_flag = False
#        min_flag = False
#        if str(loop_flag) == "ON":
#            current_temp = get_sensor_details(query="SELECT reading FROM temperature_data ORDER BY id DESC LIMIT 1")
#            current_temp = float(current_temp[0][0])
#            if (current_temp > float(max_value)) and max_flag!=True:
#                max_flag = True
#                send_email(current_temp)
#            elif (current_temp < float(min_value)) and min_flag!=True:
#                min_flag = True
#                send_email(current_temp)
#            elif (current_temp < float(max_value)) and max_flag==True:
#                max_flag = False
#                send_email(current_temp, tag="normal")
#            elif (current_temp > float(min_value)) and min_flag==True:
#                min_flag = False
#                send_email(current_temp, tag="normal")
##            loop_flag = get_sensor_details(query="SELECT status FROM sensor_details WHERE type='Temperature'")
##            loop_flag = (loop_flag)[0][0]
##            if str(loop_flag) == "OFF":
##                break
            
                
@app.route('/delete_sensor', methods = ['POST', 'GET'])
def delete_sensor():
    if request.method == 'POST':
        d_id = request.form['delete_id']
        delete_sensor_details(d_id)
        sensor_data = get_sensor_details(query="SELECT * FROM sensor_details")
        return render_template('farmer-services.html', sensor_data=sensor_data)
    
@app.route('/start_stop', methods = ['POST', 'GET'])
def start_stop():
    if request.method == 'POST':
        senor_id = request.form['senor_status']
        sensor_data_status = get_sensor_details(query="SELECT status FROM sensor_details WHERE id = %s"%senor_id)
        sensor_data_status = (sensor_data_status)[0][0]
        if str(sensor_data_status) == "ON":
            update_sensor_details(update_id=senor_id, sensor_flag=True)
            sensor_data = get_sensor_details(query="SELECT * FROM sensor_details")
            mqttc.publish('ashish12/temprature_sensor','OFF')
        else:
            update_sensor_details(update_id=senor_id, sensor_flag=False)
            sensor_data = get_sensor_details(query="SELECT * FROM sensor_details")
        return render_template('farmer-services.html', sensor_data=sensor_data)

@app.route('/farmer-register')
def farmer_register():
    return render_template('farmer-register.html')

@app.route('/addfarmer', methods = ['POST', 'GET'])
def addfarmer():
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            email = request.form['email']
            password = request.form['inputpassword']
            usertype = 'farmer'
            data = (firstname, lastname, username, email, password, usertype)
            with sqlite3.connect("Cloud281.db") as con:
                cur = con.cursor()
                statement = """INSERT INTO 'farmers' (firstname, lastname, username, email, password, usertype) VALUES (?,?,?,?,?,?);"""
                cur.execute(statement, data)
                con.commit()
                print('SUCCESS')
                msg = "SUCCESS"
        except:
            con.rollback()
            msg = "ERROR"
        finally:
            return render_template('message.html', msg=msg)
            con.close()

@app.route('/loginstaff', methods = ['POST', 'GET'])
def loginstaff():
    conn = sqlite3.connect('Cloud281.db')
    if request.method == 'POST':
        try:
            employeeID = request.form['employeeID']
            password = request.form['password']
            statement = conn.execute('SELECT employeeID FROM staffmembers')
            count = -1
            for row in statement:
                msg = "SUCCESS"
                count = count + 1
                if employeeID in row:
                    fnstatement = conn.execute("SELECT firstname FROM staffmembers WHERE employeeID=employeeID")
                    firstname = fnstatement.fetchall()[count][0]
                    lnstatement = conn.execute("SELECT lastname FROM staffmembers WHERE employeeID=employeeID")
                    lastname = lnstatement.fetchall()[count][0]
                    if (int(employeeID[0])) == 0:
                        return render_template('index-staff.html', firstname=firstname, lastname=lastname)
                    else:
                        return render_template('index-controller.html', firstname=firstname, lastname=lastname)
            conn.close()
        except:
            print('ERROR')
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            conn.close()

@app.route('/staff-register')
def staff_register():
    return render_template('staff-register.html')

@app.route('/addstaff', methods = ['POST', 'GET'])
def addstaff():
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            employeeID = request.form['employeeID']
            username = request.form['username']
            email = request.form['email']
            password = request.form['inputpassword']
            usertype = 'staff'
            data = (firstname, lastname, employeeID, username, email, password, usertype)
            with sqlite3.connect("Cloud281.db") as con:
                cur = con.cursor()
                statement = """INSERT INTO 'staffmembers' (firstname, lastname, employeeID, username, email, password, usertype) VALUES (?,?,?,?,?,?,?);"""
                cur.execute(statement, data)
                con.commit()
                print('SUCCESS')
                msg = 'SUCCESS'
        except:
            print('ERROR')
            msg = 'ERROR'
            con.rollback()
        finally:
            return render_template('message.html', msg=msg)
            con.close()


# dashboard pages
@app.route('/farmer')
def farmer():
    return render_template('index-farmer.html')

@app.route('/controller')
def controller():
    return render_template('index-controller.html')

@app.route('/staff')
def staff():
    return render_template('index-staff.html')


# farmer tabs
@app.route('/farmer-services')
def farmer_services():
    sensor_data = get_sensor_details(query="SELECT * FROM sensor_details")
    if sensor_data!= None:
        return render_template('farmer-services.html', sensor_data=sensor_data)
    else:
        return render_template('farmer-services.html')

@app.route('/farmer-catalog')
def farmer_catalog():
    return render_template('farmer-catalog.html')


# machine controller tabs
@app.route('/controller-tasks')
def controller_tasks():
    return render_template('controller-tasks.html')


# service carrier staff tabs
@app.route('/staff-resources')
def staff_resources():
    return render_template('staff-resources.html')

@app.route('/staff-servicerequests')
def staff_servicerequests():
    return render_template('staff-servicerequests.html')

@app.route('/staff-billing')
def staff_billing():
    return render_template('staff-billing.html')

@app.route('/staff-customers')
def staff_customers():
    return render_template('staff-customers.html')

@app.route('/staff-team')
def staff_team():
    return render_template('staff-team.html')


# random
@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/machine-data')
def machine_data():
    return render_template('machine-data.html')

#@app.route('/sensor-data', methods = ['GET'])
#def sensor_data():
#	conn = sqlite3.connect('Cloud281.db')
#	if request.method == 'GET':
#		cur = conn.cursor()
#		cur.execute("SELECT Date_n_Time, Humidity FROM Temperature_Data")
#		rows = cur.fetchall()
#
#		for row in rows:
#			print(row)
#		#conn.execute('SELECT Date_n_Time, Humidity FROM Temperature_Data')
#		#data = conn.fetchall()
#		#	for d in data:
#		#		print(d)
#			#return json.dumps(data)
#			conn.close()
#		except:
#			print("ERROR")
#		finally:
#			conn.close() 

@app.route('/sensor-data')
def sensor_data():
    data = pd.DataFrame(sampleData)
    #print("data: %s"%data)
    temp = data.to_dict('records')
    #print("temp: %s"%temp) 
    columnNames = data.columns.values
    status_flag = get_sensor_details(query="SELECT status FROM sensor_details WHERE type='Temperature'")
    #status_flag = (status_flag)[0][0]
    #print(status_flag)
    if (status_flag == []):
        return render_template('sensor-data.html')
    elif (str(status_flag[0][0])) == 'ON':
        return render_template('sensor-data.html',records=temp, colnames=columnNames)
    elif (str(status_flag[0][0])) == 'OFF':
        off_temp=get_sensor_details(query="SELECT * FROM temperature_data ORDER BY id ASC LIMIT 12")
        temp_off=[]
        for entry in off_temp:
           temp_off.append(entry[1:])
        return render_template('sensor-data-off.html',temp_off=temp_off)

# extras
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/buttons')
def buttons():
    return render_template('buttons.html')

@app.route('/utilities-color')
def utilities_color():
    return render_template('utilities-color.html')

@app.route('/utilities-border')
def utilities_border():
    return render_template('utilities-border.html')

@app.route('/utilities-animation')
def utilities_animation():
    return render_template('utilities-animation.html')

@app.route('/utilities-other')
def utilities_other():
    return render_template('utilities-other.html')


if __name__ == '__main__':

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    # Connect
    mqttc.connect(broker)
    # subscribe topics
    sub_multiple()
    #run the loop forever
    mqttc.loop_start()

    app.run()
    


