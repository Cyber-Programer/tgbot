import telebot
import time
import socket
from threading import Thread

love = telebot.TeleBot('6106338436:AAGB6cLSsI0DTGdRRlEVCBs1d_9YCkkOARY')

def wok():
    print('wait')

wok()

def ok():
    print('ok')

@love.message_handler(commands=['start'])
def start(message):
    wok()
    msg = '''Welcome to Cyber_portscanner:
    You can scan any website ports using this bot.'''
    love.reply_to(message, msg)
    ok()

def make_port(start_port: int, end_port: int):
    for port in range(start_port, end_port + 1):
        yield port

def scan_port(IP, ports):
    open_ports = []
    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((IP, port))
            open_ports.append(port)
        except (ConnectionRefusedError, socket.timeout):
            continue
        finally:
            s.close()
    return open_ports

def make_thread(thread, IP, ports, verbose_output=True):
    open_ports = []
    thread_list = []
    for _ in range(thread):
        thread_list.append(Thread(target=lambda: open_ports.extend(scan_port(IP, ports))))
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
    return open_ports

@love.message_handler(commands=['scan'])
def scan(message):
    try:
        ip = message.text.split()[1]
        port1 = int(message.text.split()[2])
        port2 = int(message.text.split()[3])
        thread = int(message.text.split()[4]) if len(message.text.split()) > 4 else 500

        start_time = time.time()
        ports = make_port(port1, port2)
        open_ports = make_thread(thread, ip, ports, verbose_output=False)
        end_time = time.time()

        result_msg = f"Open ports found for {ip}:\nport : {open_ports}\n"
        result_msg += f"Total time taken: {round(end_time - start_time, 2)} seconds"
        love.reply_to(message, result_msg)

    except IndexError:
        msg = '''
        I can't see any target or port.😶
        Please follow this format:
        /scan <target> <first port> <last port> <thread>

        Example:
        /scan google.com 1 100 500
        OR
        /scan google.com 1 100
        '''
        love.reply_to(message, msg)
    except OverflowError:
        msg='port must be 1-65535'
        love.reply_to(message,msg)
    except RuntimeError:
        pass

while True:
    try:
        love.polling(none_stop=True)  # Run the code non-stop
    except telebot.apihelper.ApiException as e:
        if e.result.status_code == 409:
            time.sleep(1)
            continue
        else:
            raise
