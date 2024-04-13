# lsusb to check device name
# dmesg | grep "tty" to find port name

import serial,time
import pandas as pd

if __name__ == '__main__':
    
    started = False
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 115200, timeout=1) as ser:
        time.sleep(0.1) #wait for serial to open
        if ser.isOpen():
            print("{} connected!".format(ser.port))
            try:
                # Initialize data arrays
                encoderG, encoderD, vitesseG, vitesseD, PidOutputG, PidOutputD, consigneG, consigneD = ([] for _ in range(8))
                data_map = {"A": encoderG, "B": encoderD, "C": vitesseG, "D": vitesseD, "E": PidOutputG, "F": PidOutputD, "G": consigneG, "H": consigneD}
                while True:
                    
                    try:
                        # Read data from serial
                        line = ser.readline().decode().strip()
                        if not started and line[0] != 'A':
                            continue
                        else:
                            started = True
                        print(line)

                        if line[0] in data_map :
                            # Append data to corresponding array
                            data_map[line[0]].append(float(line[1:]))
                    except IndexError:
                        continue

            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
                
            finally:
                length = min(map(len, (encoderG, encoderD, vitesseG, vitesseD, PidOutputG, PidOutputD,  consigneG,  consigneD)))

                print(length, list(map(len, (encoderG, encoderD, vitesseG, vitesseD, PidOutputG, PidOutputD,  consigneG,  consigneD))))

                # Initialize time array
                t = [i * 0.05 for i in range(length)]

                redata_map = {"encoderG": encoderG[:length], "encoderD": encoderD[:length], "vitesseG": vitesseG[:length], "vitesseD": vitesseD[:length], "PidOutputG": PidOutputG[:length], "PidOutputD": PidOutputD[:length], "consigneG": consigneG[:length], "consigneD": consigneD[:length], "t": t}
                #print(redata_map)

                # Create DataFrame
                df = pd.DataFrame(redata_map)
                print(df)
                # Save DataFrame to CSV file
                df.to_csv("data.csv", index=False)
                # Close serial port
                ser.close()

                
