from flask import Flask, render_template, request
import datetime
import json
import serial
import io

app = Flask(__name__)

def isNumber(value):
    if(len(value) == 0):
        return False
    for char in value:
        if(char.isnumeric()) == True or char == ".":
            continue
        return False
    return True


def write_data():
    print("WRITE DATA CALLED")
    current_file = open("./data/current_data.txt", "r")
    log_file = open("./data/log_data.txt", "r")

    current_data = current_file.readlines()
    log_data = log_file.readlines()

    lines = current_data + log_data
    current_file.close()
    log_file.close()
    current_file.close()

    write_file = open("./data/log_data.txt", "w")
    write_file.writelines(lines)
    return

def read_data(sio):
    fout = open("./data/current_data.txt", "w")
    count = 0
    values = []
    print("HERE")
    while count != 256:
        data = sio.readline(50).strip().split(",")
        print(len(values))
        if(len(data) > 1):
            st = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#            temp = [st, ord(data[0]), ord(data[1]), ord(data[2])]
            temp = [st, int(data[0]), int(data[1]), int(data[2])]
            values.append(temp)
            count = count + 1


    print("C")
    voltageRatio = 3.3/256
    #TODO: update current ratio, round current as needed
    currentRatio = .33/256
    for i in range(255, -1, -1):
        time = str(values[i][0]) + "\n"
        voltage = str(round(values[i][1] * voltageRatio, 2)) + "\n"
        charge = str(values[i][2] * currentRatio) + "\n"
        discharge = str(values[i][3] * currentRatio) + "\n\n"
        print(time + voltage + charge + discharge, end = "")
        fout.write(time + voltage + charge + discharge)

    fout.close()
    write_data()
    return

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

                with open("./data/configuration.txt") as fconfig:
                    config = fconfig.readlines()
                baudFile = int(config[0].rstrip())
                #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
                ser = serial.Serial("/dev/ttyS4", baudFile, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("C"))
                sio.flush()
                sio.write(str("b"))
                sio.flush()
                if (baud == 1200):
                    sio.write(str("1"))
                elif (baud == 9600):
                    sio.write(str("2"))
                elif (baud == 19200):
                    sio.write(str("3"))
                else:
                    sio.write(str("4"))
                sio.flush()
                ser.close()

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
                with open("./data/configuration.txt") as fconfig:
                    config  = fconfig.readlines()
                baudFile = int(config[0].rstrip())
                ser = serial.Serial("/dev/ttyS4", baudFile, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("C"))
                sio.flush()
                sio.write(str("v"))
                sio.flush()
                vmin = str(chr(round(input_vmin * 256 / 3.3)))
                sio.write(str(vmin))
                sio.flush()
                ser.close()
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

                with open("./data/configuration.txt") as fconfig:
                    config  = fconfig.readlines()
                baudFile = int(config[0].rstrip())
                ser = serial.Serial("/dev/ttyS4", baudFile, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("C"))
                sio.flush()
                sio.write(str("v"))
                sio.flush()
                vmax = str(chr(round(input_vmax * 256 / 3.3)))
                sio.write(str(vmax))
                sio.flush()
                ser.close()
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

                with open("./data/configuration.txt") as fconfig:
                    config  = fconfig.readlines()
                baudFile = int(config[0].rstrip())
                ser = serial.Serial("/dev/ttyS4", baudFile, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("C"))
                sio.flush()
                sio.write(str("v"))
                sio.flush()
                #TODO: charge current ratio needs to be updated
                currentRatio = .33/256
                charge = str(chr(round(input_chargeCurrent * currentRatio)))
                sio.write(str(charge))
                sio.flush()
                ser.close()
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
                with open("./data/configuration.txt") as fconfig:
                    config  = fconfig.readlines()
                baudFile = int(config[0].rstrip())
                ser = serial.Serial("/dev/ttyS4", baudFile, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("C"))
                sio.flush()
                sio.write(str("v"))
                sio.flush()
                #TODO: charge current ratio needs to be updated
                currentRatio = .33/256
                discharge = str(chr(round(input_dischargeCurrent * currentRatio)))
                sio.write(str(discharge))
                sio.flush()
                ser.close()
        except:
            pass

        with open("./data/configuration.txt", 'w') as f:
            for value in value_list:
                f.write(value + "\n")

    for i in range(len(value_list)):
        value_list[i] = float(value_list[i])

    return render_template('configure.html', baud_rate = value_list[0],
            vmin = value_list[1], vmax = value_list[2], chargeI = value_list[3],
            dischargeI = value_list[4], configuration_list = value_list,
            numElements=len(value_list))

@app.route('/graphs/')
def graphs():
    f_log = open("./data/log_data.txt", "r")
    lines = f_log.readlines()
    f_log.close()

    tmp = []
    logged_data = []

    for i in range(len(lines)):
        if (len(logged_data) == 256):
            break
        if(lines[i] == "\n"):
            if(len(tmp) == 4):
                logged_data.append(tmp)
            tmp = []
            continue
        tmp.append(str(lines[i]).rstrip())

    input_current_in = []
    input_current_out = []
    voltage = []

    for row in logged_data:
        voltage.insert(0, float(row[1]))
        input_current_in.insert(0, float(row[2]))
        input_current_out.insert(0, float(row[3]))

    x_values= list(range(1, len(logged_data)+1))
    return render_template('graphs.html', inputCurrentIn=input_current_in,
            inputCurrentOut=input_current_out, batteryVoltage=voltage,
            xPoints=x_values, numElements=len(logged_data))

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

                with open("./data/configuration.txt") as fconfig:
                    value_list = fconfig.readlines()
                baud = int(value_list[0].rstrip())
                #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
                print("SINE BAUD: ", baud)
                ser = serial.Serial("/dev/ttyS4", baud, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("S"))
                sio.flush()
                sio.write(str(sine_discharge) + "\r\n")
                sio.flush()

                read_data(sio)
                ser.close()
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
                with open("./data/configuration.txt") as fconfig:
                    value_list = fconfig.readlines()
                baud = int(value_list[0].rstrip())
                #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
                ser = serial.Serial("/dev/ttyS4", baud, timeout = 1)
                sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
                sio.write(str("D"))
                sio.flush()
                sio.write(str(prbs))
                sio.flush()
                read_data(sio)
                ser.close()
            # do stuff with charge
            return redirect(url_for('data'))
        except:
            pass
    current_lines = f.readlines()
    data = ["0000-00-00 00:00:00", "0.0", "0.0", "0.0", "0.0"]
    size = 4
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
        if (len(logged_data) == 256):
            break
        if(lines[i] == "\n"):
            if(len(tmp) == 4):
                logged_data.append(tmp)
            tmp = []
            continue
        tmp.append(str(lines[i]).rstrip())

    logged_size = len(logged_data)

    return render_template('data.html', current_data=data,
            current_elements = size, logged_elements = logged_size,
            log_data = logged_data)



@app.route('/charge_data')
def charge_data():
    print("CHARGE")
    with open("./data/configuration.txt") as f:
        value_list = f.readlines()
    baud = int(value_list[0].rstrip())
    #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
    ser = serial.Serial("/dev/ttyS4", baud, timeout = 1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(str("H"))
    sio.flush()
    ser.close()
    return "nothing"

@app.route('/discharge_data')
def discharge_data():
    print("DISCHARGE")
    with open("./data/configuration.txt") as f:
        value_list = f.readlines()
    baud = int(value_list[0].rstrip())
    #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
    ser = serial.Serial("/dev/ttyS4", baud, timeout = 1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(str("D"))
    sio.flush()
    ser.close()
    return "nothing"



@app.route('/poll_data')
def poll_data():
    print("POLL DATA")
    with open("./data/configuration.txt") as f:
        value_list = f.readlines()
    baud = int(value_list[0].rstrip())
    #ser = serial.Serial("/dev/ttyUSB0", baud, timeout = 1)
    ser = serial.Serial("/dev/ttyS4", baud, timeout = 1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.write(str("P"))
    sio.flush()
    response = sio.readline(15).strip()
    voltageRatio = 3.3/256
    voltage = round(ord(response[0]) * voltageRatio, 2)
    #TODO: update current ratio
    currentRatio = 0.33/256
    chargeCurrent = ord(response[1]) * currentRatio
    dischargeCurrent = ord(response[2]) * currentRatio
    sio.flush()
    ser.close()
    st = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    with open("./data/current_data.txt", "w") as f:
        f.write(st + "\n")
        f.write(str(voltage) + "\n")
        f.write(str(chargeCurrent) + "\n")
        f.write(str(dischargeCurrent) + "\n")


    return "nothing"

@app.route('/load_configuration')
def load_configuration():
    print("LOAD CONFIGURATION")
    with open("./data/configuration.txt") as f:
        value_list = f.readlines()
    baud = int(value_list[0].rstrip())
    ser = serial.Serial("/dev/ttyS4", baud, timeout = 1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    if (baud == 1200):
        sio.write(str("1"))
    elif (baud == 9600):
        sio.write(str("2"))
    elif (baud == 19200):
        sio.write(str("3"))
    else:
        sio.write(str("4"))
    sio.flush()
    # TODO: Update Current Charges
    voltage = round(float(value_list[1]) * 256 / 3.3)
    sio.write(str(chr(round(voltage))))
    sio.flush()
    charge = round(float(value_list[2]))
    sio.write(str(chr(round(charge))))
    sio.flush()
    discharge = round(float(value_list[3]))
    sio.write(str(chr(round(discharge))))
    sio.flush()

    return "nothing"


if __name__ == '__main__':
    app.run(debug=True)
