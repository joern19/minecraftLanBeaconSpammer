import time, socket, sys, os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_PORT = 4445
UDP_IP = "224.0.2.60"

def send(motd, port):
    message = '[MOTD]{0}[/MOTD][AD]{1}[/AD]'.format(str(motd), str(port))
    sock.sendto(bytes(message, 'UTF-8'), (UDP_IP, UDP_PORT))

entrys = []

delay = 1000

def start():
    try:
        while True:
            for entry in entrys:
                send(entry[0], entry[1])
            print("+", end="")
            time.sleep(delay / 1000)
    except KeyboardInterrupt:
        print("\nProgramm cancelled.")
        exit()

def format(line):
    line = line.replace("\n", "")

    a = line.replace("##", "..")
    if not (a.count('#') == 1):
        print("Format Error in: " + line)
        print("The Format is as Follows: 'motd#port'")
        print("If you want to display an '#' just make '##'")
        exit()    
    port = a.split("#", 1)[1]
    
    motd = line[:-(len(port) + 1)]
    return [motd.replace("##", "#"), port]

def file_parser(path, out):
    if os.path.isfile(path):
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if (line.replace(" ", "").replace("\n", "") == ""):
                    return
                entrys.append(format(line))
    else:
        print("The File {0} does not exists.".format(path))
        exit()

if __name__ == '__main__':
    if (2 == len(sys.argv)):
        file_parser(sys.argv[1], entrys)
        start()
    elif(3 == len(sys.argv)):
        file_parser(sys.argv[1], entrys)
        try:
            in_delay = int(sys.argv[2])
        except ValueError:
            print("The Secound Argument(the delay) has to be an Integer.")
            exit()
        delay = in_delay
        start()
    else:
        print("The First Argument is the File.")
        print("The Secound is optional. Here you can define the delay between broadcasts. Default is 1000")
        print("\nFor Example: 'python3 minecraftLanBeaconSpammer.py file.txt 2000'")
        exit()
        
