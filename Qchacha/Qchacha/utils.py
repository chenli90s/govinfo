from datetime import datetime
import time
import threading
import functools
import base64
import scrapy
from Qchacha.zmProxy import ZmProxy
import random

PROXY_LIST = [
    {"ip_port": "121.199.1.230:16816", "user_passwd": "morganna_mode_g:ggc22qxp"},
    {"ip_port": "171.36.208.6:8118"}
]


class ProxyIp:

    def __init__(self):
        self._ip_port = None
        self._user_passwd = None
        self._flush_time = None
        self._del_time = None

    @property
    def ip_port(self):
        return self._ip_port

    @ip_port.setter
    def ip_port(self, ip_port):
        self._ip_port = ip_port

    @property
    def user_passwd(self):
        return self._user_passwd

    @user_passwd.setter
    def user_passwd(self, user_passwd):
        self._user_passwd = user_passwd

    @property
    def flush_time(self):
        return self._flush_time

    @flush_time.setter
    def flush_time(self, flush_time):
        self._flush_time = flush_time

    def flush(self):
        self.flush_time = datetime.now()
        return self

    @property
    def del_time(self):
        return self._del_time

    @del_time.setter
    def del_time(self, _del_time):
        self._del_time = _del_time


class ProxyIPpool:
    __instance_obj = None
    __is_first = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance_obj:
            cls.__instance_obj = super(ProxyIPpool, cls).__new__(cls)
        return cls.__instance_obj

    def __init__(self):
        if self.__instance_obj and not self.__is_first:
            return None
        self.__is_first = False
        self._ip_dict = dict()
        self._idle_list = list()
        self._busy_list = list()
        self._err_list = list()
        self.mutex = threading.Lock()

    def init_ip_pool(self):
        print("ip池初始化")
        zm = ZmProxy()
        res = zm.get_proxy_ip()
        print(res)
        self.ip_pool_flush(res)
        print('池更新成功')

    def ip_pool_flush(self, proxy_list):
        for index, ip in enumerate(proxy_list):
            proxy_ip = ProxyIp()
            proxy_ip.ip_port = ip.get('ip', '') + ':' + str(ip.get('port', ''))
            proxy_ip.flush_time = datetime.now()
            proxy_ip.del_time = datetime.strptime(ip.get('expire_time', ''), '%Y-%m-%d %H:%M:%S')
            self._ip_dict[proxy_ip.ip_port] = proxy_ip
            self._idle_list.append(proxy_ip)
            # print(proxy_ip.ip_port,'---------------------------')
        # print('---------', self._ip_dict,'---------------------------')
        # print('---------', self._idle_list,'---------------------------')

    def __getattr__(self, item):
        return self._ip_dict.get(item, '')

    def get(self, ip):
        return self._ip_dict.get(ip, '')

    def get_ip(self):
        # self.mutex.acquire()
        ip = self._get_ip()
        # self.mutex.release()
        return ip

    def _get_ip(self):
        self._gc_ip()
        # print('********', self._idle_list, '********')
        ip = random.choice(self._idle_list)
        if ip.ip_port in self._ip_dict:
            print("拿到ip:", ip.ip_port)
            return ip
        else:
            self._idle_list.remove(ip)
            return self.get_ip()

    def flush_ip(self, ip):
        self._err_list.remove(self.get(ip))
        self._idle_list.append(self.get(ip).flush())

    def release_ip(self, ip):
        self._idle_list.append(self.get(ip))

    def gc_ip(self, ip):
        self._err_list.append(self.get(ip))

    def _gc_ip(self):
        self.mutex.acquire()
        if len(self._ip_dict) < 1:
            self.init_ip_pool()
        self.mutex.release()
        for ip in self._ip_dict.values():
            if (ip.del_time - datetime.now()).seconds < 30:
                self._ip_dict.pop(ip.ip_port)
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                print('<<<  回收了一个IP：', ip.ip_port, '<<<<<<<<<<<')
                print('<<<<                                 <<<<')
                print('<<<<                                 <<<<')
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        for ip in self._err_list:
            self._ip_dict.pop(ip.ip_port)
            self._err_list.remove(ip)
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            print('<<<  回收了一个IP：', ip.ip_port, '<<<<<<<<<<<')
            print('<<<<                                 <<<<')
            print('<<<<                                 <<<<')
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    def process_request(self, request):
        ipob = self.get_ip()
        # print("wrapper_____", ipob.ip_port)
        # print("wrapper_____", ipob.user_passwd)
        if ipob.user_passwd:
            res = base64.b64encode(ipob.user_passwd.encode())
            request.headers['Proxy-Authorization'] = 'Basic ' + res.decode()
            request.meta['proxy'] = ipob.ip_port

        else:
            request.meta['proxy'] = ipob.ip_port

    def wrapper_request(self, process_request):
        @functools.wraps(process_request)
        def wrapper(request, spider):
            ipob = self.get_ip()
            print("wrapper_____", ipob.ip_port)
            print("wrapper_____", ipob.user_passwd)
            if ipob.user_passwd:
                res = base64.b64encode(ipob.user_passwd.encode())
                request.headers['Proxy-Authorization'] = 'Basic ' + res.decode()
                request.meta['proxy'] = ipob.ip_port
            else:
                request.meta['proxy'] = ipob.ip_port

        return wrapper


if __name__ == '__main__':
    pool0 = ProxyIPpool()
    # time.sleep(5)
    pool = ProxyIPpool()
    ip1 = pool.get_ip()
    ip2 = pool.get_ip()
    print(ip1.flush_time, ip1.ip_port)
    print(ip2.flush_time, ip2.ip_port)
    time.sleep(3)
    pool.err(ip1.ip_port)
    pool.flush_ip(ip1.ip_port)
    pool.err(ip2.ip_port)
    pool.flush_ip(ip2.ip_port)
    print(ip1.flush_time, ip1.ip_port)
    print(ip2.flush_time, ip2.ip_port)
    pool.release_ip(ip1.ip_port)
    pool.release_ip(ip2.ip_port)
    request = scrapy.Request('http://www.baidu.com')
    request2 = scrapy.Request('http://www.baidu.com')


    @pool.wrapper_request
    def call_func(request, sipder):
        pass


    call_func(request, None)
    call_func(request2, None)
    print(request.meta)
    print(request.headers)
    print(request2.meta)
    print(request2.headers)
