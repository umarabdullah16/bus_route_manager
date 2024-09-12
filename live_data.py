import requests

response = requests.get('https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key=pZGVvc07g5r0tZ46x8gbIMhp2mLiHXFg')

if response.status_code == 200:
    binary_data = response.content
    with open('output_file.pb', 'wb') as f:
        f.write(binary_data)