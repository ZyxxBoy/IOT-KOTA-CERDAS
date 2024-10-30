from machine import Pin
import dht
import socket
import time

# Inisialisasi sensor DHT11 di pin yang sesuai
dht_sensor = dht.DHT11(Pin(14))  # Sesuaikan dengan pin yang Anda gunakan untuk DHT11

def web_page():
    try:
        # Membaca data suhu dan kelembaban dari DHT11
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
    except OSError as e:
        temperature = 'Error'
        humidity = 'Error'

    # HTML untuk menampilkan data suhu dan kelembaban
    html = f"""<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}}
    h1{{color: #0F3376; padding: 2vh;}}p{{font-size: 1.5rem;}}.data{{font-size: 2rem; color: #333;}}</style></head>
    <body> <h1>ESP Web Server - DHT11</h1>
    <p>Suhu: <strong class="data">{temperature} &#8451;</strong></p>
    <p>Kelembaban: <strong class="data">{humidity} %</strong></p>
    </body></html>"""
    return html

# Setup socket untuk web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))

    # Memanggil halaman web untuk dikirimkan sebagai respons
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    time.sleep(1)  # Delay untuk mencegah pembacaan berlebihan dari sensor
