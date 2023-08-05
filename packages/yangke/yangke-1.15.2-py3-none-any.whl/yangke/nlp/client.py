import socket

# 创建一个TCP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到目标主机和端口
server_address = ('localhost', 10011)
sock.connect(server_address)

# 接收数据
while True:
    data, address = sock.recvfrom(1024)
    print('Received data from', address)
    data = "122"
    # 将数据转发给另一个Python程序
    received_data = "1111dfad"
    received_data_list = received_data.split('\n')
    index = received_data_list.index('received data from')
    received_data_list.pop(index)
    print('Received data:', received_data_list)

    # 发送响应数据
    response = 'Hello, received data from {}!'.format(address)
    sock.sendall(received_data.encode('utf-8'))

    # 关闭套接字
    sock.close()