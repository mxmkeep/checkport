#encoding=utf-8

import sys, getopt
import datetime
import socket

def phelp():
    print('''chkport.py -d <dst IP> -p <dst port> -b <local ip>
    python chkport.py  -d 192.168.47.222 -p10000 -b 127.0.0.1 -v
    -h help
    -b dst IP
    -p dst port
    -b local ip
    -v show req and rps data''')
    
def main(argv):

    addr_local = "0"
    dstip = ""
    dstport = 0
    shwdata = 0
    try:
        opts, args = getopt.getopt(argv,"hvd:p:b:")
    except getopt.GetoptError:
        phelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            phelp()
            sys.exit()
        elif opt == "-d":
            dstip = arg
        elif opt == "-p":
            dstport = int(arg)
        elif opt == "-b":
            addr_local = arg
        elif opt == "-v":
            shwdata = 1

    #print("\n----start----", datetime.datetime.now())
    
    sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if len(addr_local) > 6:
        sk.bind((addr_local,0))
    sk.settimeout(1)
    
    ipinfo = "connect to %s %s"%(dstip,dstport)
    try:
        sk.connect((dstip,dstport))
    except Exception:
        print(ipinfo + " failed.")
        sk.close()
        exit()
        
    req="GET / HTTP/1.1\r\nHost: %s\r\n"\
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100\r\n"\
        "Sec-WebSocket-Key: JbD4n0d6+nvPee/Nx/ufsg==\r\n"\
        "Sec-WebSocket-Version: 13\r\n"\
        "Upgrade: websocket\r\n"\
        "Connection: Upgrade\r\n\r\n"% dstip
    if shwdata == 1:
        print(req)
    try:
        sk.send(req)
        ret = sk.recv(2048).lower()
        if shwdata == 1:
            print(ret)
        if ret.find("websocket", 0, 1024) > -1:
            print(ipinfo + " successed, protocol websocket")
        elif ret.find("400 bad", 0, 1024)>-1 and ret.find("https", 0, 1024)>-1 :
            print(ipinfo + " successed, protocol https")
        elif ret.find("http", 0, 1024) > -1:
            print(ipinfo + " successed, protocol http")
        else :
            print(ipinfo + " successed, protocol tcp")
    except  socket.error as e:
        print(ipinfo + " successed, protocol tcp")
      
    sk.close()
        
        
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
