import socket
import multiprocessing
import threading
import re
import time
import sys
class WSGI_server(object):
    def __init__(self, port, app):
        print("2.web_server")
        self.web_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.web_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.web_socket.bind(("",port))
        print("3.listen")
        self.web_socket.listen(128)
        self.app = app
    def service(self,traffic_socket):
        request = traffic_socket.recv(1024).decode("utf-8")
        request=request.splitlines()
       # print(request[0])
       # print("\r\n")
        ret = re.match(r'([^/]*/)([^ ]*)', request[0])
        filename = ret.group(2)
        print("filename:",filename)
        if not filename.endswith("py"):
            traffic_socket.send("load static page".encode("utf-8"))
        else:
            env = dict()
            env["PATH_INFO"]=filename
            body = self.app(env,self.set_response)
            header = "HTTP/1.1%s\r\n"%self.status
            for temp in self.header:
                header += "%s:%s\r\n" %(temp[0], temp[1])             
            header += "\r\n"
            response = header+body
            traffic_socket.send(response.encode("utf-8"))
        traffic_socket.close()
        self.web_socket.close()

    def set_response(self,status,header):
            self.status = status
            self.header = header


#the above need add application function

    def run(self):
       
        while True:
            traffic_socket, traffic_IP = self.web_socket.accept()
           
            p = multiprocessing.Process(target = self.service,args = (traffic_socket,))
            p.start()
            traffic_socket.close()
        self.web_socket.close()
def main():
    if len(sys.argv)==3:
        try:
            port = int(sys.argv[1])
            frame_app_name = sys.argv[2]
        except Exception as f:
            print("the input is wrong")
            return 
    else:
        print("the right input method is: python xxxxx.py 7788 mini_frame:application")
    ret = re.match(r"([^:]*):([^$]*)",frame_app_name)
    frame_name = ret.group(1)
    app_name = ret.group(2)
    print(frame_name, app_name)
    with open("web_server.conf") as f:
        conf = eval(f.read())
    sys.path.append(conf["dynamic_path"])
    frame = __import__(frame_name)
    app = getattr(frame, app_name)

    wsgi=WSGI_server(port,app)
    wsgi.run()

if __name__ == "__main__":
    print("1.main")
    main() 
