import socket 
from views import *

URLS = {
    '/': index,
    '/home': home
}

def pars_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]

    return (method, url)

def generate_headers(method, url):
    if method != 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    elif not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)

def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not Found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()

def generate_response(request):
    if request != '':
        method, url = pars_request(request)
        headers, code = generate_headers(method, url)
        body = generate_content(code, url)

        return (headers + body).encode()
    else:
        return  ('HTTP/1.1 200 OK\n\n').encode()

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 5000))
   
    server_socket.listen()
    print('Сокет сервера слушает порт')

    while True:
        client_soket, addr = server_socket.accept()
        print('К серверу подключился пользователь')
        request = client_soket.recv(1024)
        print('Информация о запросе пользовтеля:')
        print(request)
        print('ADDR: ' + str(addr))

        reponse = generate_response(request.decode('utf-8'))

        client_soket.sendall(reponse)
        print('Ответ клиенту завершён')
        client_soket.close()
        print('Соеденения закрыто')


if __name__ == '__main__':
    run()