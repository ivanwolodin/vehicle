Проект в котором реализован сервис, предоставляющий информацию об утилизации ресурсов сервера на сокетах, поддерживающих асинхронные запросы.

Для запуска сервера:
    python server_w.py

Далее, для запуска клиента:
    python client_w.py

Порядок важен. Сначала сервер, потом клиент.
Запросы, которые поддерживаются:
    memory
    cpu
    servertime ---> только в случае, если перед этим будет собран модуль, написанный на C++ (делается командой python setup.py install)

Команды вида:
    command-<int>
    command_<int>
    где <int> - это время, через которое сервер отправляет запросы по сокетам
    Пример команды:
        cpu-1 ----> сработае команда cpu и сервер будет отправлять запросы с интервалом в секунду

Проблемы:
    консоли работают по разному. windows-консоли, *nix-консоли.
    это неприятно, поэтому не до конца имплементирована функция прерывания сообщений и
    отправки новой команды по существующему сокету.
    На windows-консоли это работает, в cmd, на Ubuntu - пока не сделано.


Докер-образ проекта: https://hub.docker.com/repository/docker/ivanwolodin/vehicle

---------------------------------------------------------------------------------------------------------------------

A project that implements a service that provides information about server resource utilization on sockets that support asynchronous requests.

To start the server:
    python server_w.py

Next, to launch the client:
    python client_w.py

Order is important. First the server, then the client.
Requests from client that are supported:
    memory
    cpu
    servertime ---> only if a module written in C++ is built first (to do the following, execute: python setup.py install)

Problems:
    consoles on different machines (windows, *nix) have different behavior,
    which is kind of unpleasant, so the output interrupting from server
    and sending a new request over the existing socket is not fully implemented in client.py.
    On the windows console this works in cmd, on Ubuntu - is not done yet.

Docker image of the project: https://hub.docker.com/repository/docker/ivanwolodin/vehicle