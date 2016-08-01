import sys, glob, serial, atexit, logging, time, getopt, winsound

versionNumber = '1.0'
mute = False

def serial_ports():
    ''' Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    '''
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal '/dev/tty'
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#write to file
def writeToFile(string, fileprefix):
    filename = '{}-{}.txt'.format( fileprefix, time.strftime("%Y-%m-%d") )
    try:
        with open(filename, 'a') as logfile:
            logfile.write(string + "\n")
    except IOError:
        printAndLog(logging.DEBUG, 'ERROR: unable to open file {}'.format(filename))
        sys.exit(5)

def main():
    print('')
    print('PRINTER FOR MIDMARK M9/M11 STERILIZERS', 'V', versionNumber)
    print('')

    #get arguments
    debugLevel = logging.INFO
    fileprefix = 'sterilizer-log'
    baud = 9600
    mute = False
    optionString = 'Options: [--baud=<baud_rate>] [--help] [--debug] [--logfile=<filename_prefix>] [--mute]'
    try:
        options, remainder = getopt.getopt(sys.argv[1:],'b:hdl:', ['baud=','help','debug','logfile='])
        for opt, arg in options:
            if opt in ('-h', '--help'):
                print(optionString)
                print('Support: devinkwok.com/sterilizer-printer')
                print('Contact: devin@devinkwok.com')
                sys.exit(0)
            elif opt in ('-b', '--baud'):
                baud = arg
            elif opt in ('-d', '--debug'):
                debugLevel = logging.DEBUG
            elif opt in ('-l', '--logfile'):
                fileprefix = arg
            elif opt in ('-m', '--mute'):
                mute = True
    except getopt.GetoptError:
        print(optionString)
        sys.exit(2)

    #set up logging
    try:
        logging.basicConfig(filename='sterilizer-printer.log', format='%(asctime)s %(message)s', level=debugLevel)
    except:
        print('ERROR: unable to start logging')
        sys.exit(3)

    #select serial port
    ports = serial_ports()
    port = None
    if len(ports) == 0:
        print('No usable serial ports found')
        sys.exit(1)
    elif len(ports) == 1:
        port = ports[0]
    else:
        print('Select serial port from list:\n{}\n'.format('\n'.join('{}: {}'.format(*k) for k in enumerate(ports))))
        while port is None:
            try:
                port = ports[ int(input('>> ')) ]
            except (TypeError, IndexError, ValueError):
                print('Invalid port selection')

    #open serial port
    try:
        ser = serial.Serial(port, baud, timeout=1)
    except (serial.SerialException, ValueError):
        print('Unable to open serial: port={} baud={}'.format(port, baud))
        sys.exit(4)
    printAndLog(logging.DEBUG, 'Serial initialized: port={} baud={}'.format(port, baud))

    #open log file
    writeToFile('', fileprefix)
    printAndLog(logging.INFO, 'Program started, saving data to filenames starting with {}'.format(fileprefix))

    #decode and write serial data to file as it arrives
    try:
        while True:
            try:
                bytes = ser.readline()
                line = bytes.decode('ascii', errors='strict')
            except UnicodeError:
                msg = 'ERROR: unable to decode {}'.format(bytes)
                writeToFile(msg, fileprefix)
                printAndLog(logging.ERROR, msg)
            if line != '':
                line = line.rstrip('\r\n')
                #fill in date
                if line == ' __ / __ / ____  __ : __':
                    timestring = time.strftime(' %m / %d / %Y  %H : %M')
                    writeToFile(timestring, fileprefix)
                    printAndLog(logging.DEBUG, 'Timestamp inserted: {}'.format(timestring))
                else:
                    writeToFile(line, fileprefix)
                    printAndLog(logging.DEBUG, 'Read line: {}'.format(line))
                if not mute:
                    winsound.PlaySound('printer-sound.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
    except serial.SerialException:
        printAndLog(logging.ERROR, 'ERROR: serial connnection lost')
        sys.exit(1)
    except KeyboardInterrupt:
        printAndLog(logging.INFO, 'Program stopped')
        sys.exit(0)

def printAndLog(loglevel, string):
    print(string)
    logging.log(loglevel, string)
    if loglevel > logging.INFO and not mute:
        winsound.Beep(2000, 300)

#start program
if __name__ == "__main__":
    main()
