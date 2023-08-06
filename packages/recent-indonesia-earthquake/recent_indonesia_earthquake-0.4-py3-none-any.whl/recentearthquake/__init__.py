import requests
import bs4

description = 'To get the recent earthquake in Indonesia from BMKG.go.id'
def ekstraksi_data():

    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None
    if content.status_code == 200:
        soup = bs4.BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        for res in result:
            if i == 1:
                magnitudo =  res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['koordinat'] = {'ls': ls, 'bt': bt}
        hasil['lokasi'] = lokasi
        hasil['dirasakan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print('Tidak bisa menemukan data gempa terkini')
        return

    print('The last earthquake based on BMKG')
    print(f"Date {result['tanggal']}")
    print(f"Time {result['waktu']}")
    print(f"Magnitude {result['magnitudo']}")
    print(f"Depth {result['kedalaman']}")
    print(f"Coordinate: {result['koordinat']['ls']}, {result['koordinat']['bt']}")
    print(f"Location {result['lokasi']}")
    print(f"{result['dirasakan']}")

if __name__ == '__main__':
    print('Package description', description)
    result = ekstraksi_data()
    tampilkan_data(result)
