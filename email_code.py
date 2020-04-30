# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:24:14 2020

@author: ashish
"""
from email.mime.text import MIMEText
import smtplib
from new_sql import get_sensor_details


def trigger_email_alert():
    loop_flag = get_sensor_details(query="SELECT status, min_threshold, max_threshold FROM sensor_details WHERE type='Temperature'")
    if loop_flag == []:
        return
    min_value = loop_flag[0][1]
    max_value = loop_flag[0][2]
    max_flag = False
    min_flag = False
    if (str(loop_flag[0][0])) == 'ON':
        current_temp = get_sensor_details(query="SELECT reading FROM temperature_data ORDER BY id DESC LIMIT 1")
        current_temp = float(current_temp[0][0])
        if (current_temp > float(max_value)) and max_flag!=True:
            max_flag = True
            send_email(current_temp,threshold=max_value)
        elif (current_temp < float(min_value)) and min_flag!=True:
            min_flag = True
            send_email(current_temp,threshold=min_value)
        elif (current_temp < float(max_value)) and max_flag==True:
            max_flag = False
            send_email(current_temp, threshold=max_value, tag="normal")
        elif (current_temp > float(min_value)) and min_flag==True:
            min_flag = False
            send_email(current_temp, threshold=min_value, tag="normal")
    

def send_email(current_temp,threshold,tag="exceeded"):
    from_email="ashish.kadam120@gmail.com"
    from_password="Optimusprime12"
    to_email="ashish.jkadam12@gmail.com"

    subject="Sensor Temperature has crossed the threshold value"
    if tag == "normal":
        subject="Sensor Temperature has returned to the NORMAL state"

    message="Your current temperature is <strong>%s</strong>. Your threshold value is <strong>%s</strong>." % (current_temp,threshold) 
    #<br> Average height of all is <strong>%s</strong> and that is calculated out of <strong>%s</strong> people. <br> Thanks!" % (height, average_height, count)

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
    
    
