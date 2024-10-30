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

    # HTML untuk menampilkan data suhu dan kelembaban dengan tampilan lebih menarik
    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ESP Web Server - DHT11</title>
        <link rel="icon" href="data:,">
        <style>
            html {{
                font-family: Arial, sans-serif;
                display: inline-block;
                margin: 0 auto;
                text-align: center;
                background-color: #f2f2f2;
                color: #333;
            }}
            h1 {{
                color: #0F3376;
                padding: 20px;
                margin-top: 20px;
            }}
            .card {{
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                display: inline-block;
                margin: 20px;
                padding: 20px;
                width: 300px;
            }}
            .data-label {{
                font-size: 1.25rem;
                color: #555;
            }}
            .data-value {{
                font-size: 2.5rem;
                font-weight: bold;
                color: #0F3376;
            }}
        </style>
    </head>
    <body>
        <h1>ESP Web Server - DHT11</h1>
        <div class="card">
            <p class="data-label">Suhu:</p>
            <p class="data-value">{temperature} &#8451;</p>
            <p class="data-label">Kelembaban:</p>
            <p class="data-value">{humidity} %</p>
        </div>
    </body>
    </html>"""
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
