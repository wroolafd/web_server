import time
#import date
URL_list = dict()
def router(url):
    def add_func(fun):
        URL_list[url]=fun
        def set_func(*args, **kwargs):
            return fun(*args, **kwargs)
        return set_func
    return add_func
@router("index.py")
def index():
    try:
        f = open("./templates/file","w+")
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        f.close()
    except Exception as f:
        print("can't write")
        return
    with open("./templates/file") as f:
        return f.read()
@router("center.py")
def center():
    return "center"

def application(env,start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8'),('server','mini_server')])
    filename = env['PATH_INFO']
    #if result == "index.py":
    #    ret = index()
    #elif result == "center.py":
    #    ret = center()
    #else:
    #    ret = "not found 404"

    try:
        return URL_list[filename]()
    except Exception as f:
        print("产生了异常%s"%str(f))
