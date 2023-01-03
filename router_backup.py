import paramiko
import datetime
import time
import os



ip_address = {"10.197.0.1":"Router_1",
"10.197.0.2":"Router_2",
"10.197.0.3":"Router_3",
"10.197.0.4":"Router_4",
"10.197.0.5":"Router_5",
"10.197.0.6":"Router_6",
 }



for ip in ip_address:
    try:
        conn = paramiko.SSHClient()  # High-level representation of a session with an SSH server
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # When 1st connection, ask to trust this server or not
        conn.connect(ip, 22, "testuser", "testpassword")  # Initiate SSH connection with IP, Port, Username, Password
        commands = conn.invoke_shell()  # Request an interactive shell session on this channel.
        time.sleep(1)
        commands.send('enable\n')
        time.sleep(0.5)
        commands.send('scroll \n')
        time.sleep(0.5)
        commands.send('\n')
        time.sleep(0.5)
        commands.send('display current-configuration' + '\n' + '\n')
        time.sleep(50)
        output = commands.recv(1000000000)  # .recv() - The maximum amount of data to be received at once is specified by nbytes
        output = output.decode("utf-8")  # Change file type from bytes to string
        time.sleep(1.5)
        olt_folder = (ip_address[ip]+"_AR")
        print(ip_address[ip]+" ip reachable..")

        dirName = '//devices-backup//backup-AR-config//' + (olt_folder)
        # Create target directory & all intermediate directories if don't exists
        os.makedirs(dirName, exist_ok=True)
        filename = datetime.datetime.now()
        f = open((dirName) + "//" + filename.strftime("%d %B %Y " + (olt_folder)) + ".txt", "w")
        f.write(output)
        time.sleep(0.5)
        f.close()
    except TimeoutError:
        olt_folder = (ip_address[ip] + "_AR")
        dirName = '//devices-backup//backup-AR-config//Not detected//'
        # Create target directory & all intermediate directories if don't exists
        os.makedirs(dirName, exist_ok=True)
        filename = datetime.datetime.now()
        try:
            f= open((dirName)+"Devices not found.txt","x")
            f = open((dirName) + "Devices not found.txt", "a")
            f.write(olt_folder + " " + (ip) + " not detected -" + filename.strftime("%d %B %Y \n"))
            f.close()
            print(ip_address[ip] + " Not found ")
        except FileExistsError:
            f = open((dirName) + "Devices not found.txt", "a")
            f.write(olt_folder + " " + (ip) + " not detected -" + filename.strftime("%d %B %Y \n"))
            f.close()
            print(ip_address[ip] + " Not found ")