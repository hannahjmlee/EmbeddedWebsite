from flask import Flask, render_template, request
import time
import datetime
import json

app = Flask(__name__)

def isNumber(value):
    if(len(value) == 0):
        return False
    for char in value:
        if(char.isnumeric()) == True or char == ".":
            continue
        return False
    return True


@app.route('/')
def website():
    return render_template('home.html')

@app.route('/configure/', methods=['GET', 'POST'])
def configure():
    with open("./data/configuration.txt") as f:
        value_list = f.readlines()
    for i in range(len(value_list)):
        value_list[i] = value_list[i].rstrip()
    if request.method == "POST":
        try:
            input_baud = request.form['baud']
            input_baud = input_baud.rstrip()
            print("New Baud rate:", input_baud)
            num = isNumber(input_baud)
            if(num):
                input_baud = str(int(round(float(input_baud))))
                value_list[0] = input_baud
        except:
            pass

        try:
            input_vmin = request.form['vmin']
            input_vmin = input_vmin.rstrip()
            print("New Min Voltage:", input_vmin)
            num = isNumber(input_vmin)

            if(num):
                input_vmin = str(float(input_vmin))
                value_list[1] = input_vmin
        except:
            pass

        try:
            input_vmax = request.form['vmax']
            input_vmax = input_vmax.rstrip()
            print("New Max Voltage:", input_vmax)
            num = isNumber(input_vmax)

            if(num):
                input_vmax = str(float(input_vmax))
                value_list[2] = input_vmax
        except:
            pass

        try:
        # max charge current
            input_chargeCurrent = request.form['chargeI']
            input_chargeCurrent = input_chargeCurrent.rstrip()
            print("New Charge Current: ", input_chargeCurrent)
            num = isNumber(input_chargeCurrent)
            if(num):
                input_chargeCurrent = str(float(input_chargeCurrent))
                value_list[3] = input_chargeCurrent
        except:
            pass
        try:
            input_dischargeCurrent = request.form['dischargeI']
            input_dischargeCurrent = input_dischargeCurrent.rstrip()
            print("New Discharge Current: ", input_dischargeCurrent)
            num = isNumber(input_dischargeCurrent)
            if(num):
                input_dischargeCurrent = str(float(input_dischargeCurrent))
                value_list[4] = input_dischargeCurrent
            # max discharge current
        except:
            pass

        try:
            input_minTemp = request.form['minTemp']
            input_minTemp = input_minTemp.rstrip()
            print("New Minimum Temperature: ", input_minTemp)
            num = isNumber(input_minTemp)
            if(num):
                input_minTemp = str(int(round(float(input_minTemp))))
                value_list[5] = input_minTemp
            # min temperature
        except:
            pass

        try:
            input_maxTemp = request.form['maxTemp']
            input_maxTemp = input_maxTemp.rstrip()
            print("New Maximum Temperature: ", input_maxTemp)
            num = isNumber(input_maxTemp)
            if(num):
                input_maxTemp = str(int(round(float(input_maxTemp))))
                value_list[6] = input_maxTemp
            # max temperature
        except:
            pass

        with open("./data/configuration.txt", 'w') as f:
            for value in value_list:
                f.write(value + "\n")

    for i in range(len(value_list)):
        if (i >= 1) and (i <= 4):
            value_list[i] = float(value_list[i])
        else:
            value_list[i] = int(value_list[i])

    return render_template('configure.html', baud_rate = value_list[0],
            vmin = value_list[1], vmax = value_list[2], chargeI = value_list[3],
            dischargeI = value_list[4], minTemp = value_list[5],
            maxTemp = value_list[6], configuration_list = value_list,
            numElements=len(value_list))

@app.route('/graphs/')
def graphs():
    f_log = open("./data/log_data.txt", "r")
    lines = f_log.readlines()
    f_log.close()

    tmp = []
    logged_data = []

    for i in range(len(lines)):
        if (len(logged_data) == 10):
            break
        if(lines[i] == "\n"):
            if(len(tmp) == 5):
                logged_data.append(tmp)
            tmp = []
            continue
        tmp.append(str(lines[i]).rstrip())

    input_current_in = []
    input_current_out = []
    voltage = []
    temp = []

    for row in logged_data:
        input_current_in.insert(0, float(row[1]))
        input_current_out.insert(0, float(row[2]))
        voltage.insert(0, float(row[3]))
        temp.insert(0, float(row[4]))

    x_values= list(range(1, len(logged_data)+1))
    return render_template('graphs.html', inputCurrentIn=input_current_in,
            inputCurrentOut=input_current_out, batteryVoltage=voltage,
            temperature=temp, xPoints=x_values, numElements=len(logged_data))

@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/data/', methods=['GET', 'POST'])
def data():
    f = open("./data/current_data.txt", "r")
    if request.method == "POST":
        try:
            sine_discharge = request.form['sine_discharge']
            sine_discharge = sine_discharge.rstrip()
            print("Sine Discharging: ", sine_discharge)
            num = isNumber(sine_discharge)
            if(num):
                sine_discharge = float(sine_discharge)
            # do stuff with charge
            return redirect(url_for('data'))
        except:
            pass

        try:
            prbs = request.form['PRBS_discharge']
            prbs = prbs.rstrip()
            print("Pseudo Random Binary Sequence Discharge: ", prbs)
            num = isNumber(prbs)
            if(num):
                prbs = float(prbs)
            # do stuff with charge
            return redirect(url_for('data'))
        except:
            pass
    current_lines = f.readlines()
    data = ["0000-00-00 00:00", "0.0", "0.0", "0.0", "0.0"]
    size = 5
    i = 0
    if(len(current_lines) != 0):
        for value in current_lines:
            data[i] = str(value).rstrip()
            i += 1
            if(i == size):
                break
    f.close()

    f_log = open("./data/log_data.txt", "r")
    lines = f_log.readlines()
    f_log.close()

    tmp = []
    logged_data = []

    for i in range(len(lines)):
        if (len(logged_data) == 10):
            break
        if(lines[i] == "\n"):
            if(len(tmp) == 5):
                logged_data.append(tmp)
            tmp = []
            continue
        tmp.append(str(lines[i]).rstrip())

    logged_size = len(logged_data)

    return render_template('data.html', current_data=data, current_elements = size, logged_elements = logged_size, log_data = logged_data)


@app.route('/read_data')
def read_data():
    f = open("./data/input_data.txt", "r")
    fout = open("./data/current_data.txt", "w")
    value_list = []
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
    value_list.append(st+"\n")
    lines = f.readlines()
    for value in lines:
        value_list.append(str(float(value))+"\n")
    fout.writelines(value_list)
    f.close()
    fout.close()
    return "nothing"

@app.route('/write_data')
def write_data():
    print("SHITS")
    current_file = open("./data/current_data.txt", "r")
    log_file = open("./data/log_data.txt", "r")

    current_data = current_file.readlines()
    current_data.append("\n")
    log_data = log_file.readlines()

    lines = current_data + log_data
    current_file.close()
    log_file.close()
    current_file.close()

    write_file = open("./data/log_data.txt", "w")
    write_file.writelines(lines)
    return "nothing"


@app.route('/charge_data')
def charge_data(): 
    print("FUCKING HELL")
    return "nothing"
    #with open("./data/configuration.txt") as f:
    #    value_list = f.readlines()
    #baud = int(value_list[0].rstrip())
    #print("BAUD RATE IS: ", baud)
    #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
    #sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    #sio.write(str("H"))
    #sio.flush()
    #response = sio.readline(15).strip()
    #print("Sent C: ", response)
    #ser.close()
    #open('./data/current_data.txt', 'w').close()

