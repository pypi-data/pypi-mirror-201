# Recent Indonesia Earthquake
This package will get recent earthquake from BMKG (Meteorological, Climatological, and Geophysical Agency)

## HOW IT WORKS?
This package will scrape from [BMKG](https://www.bmkg.go.id.com) to get recent earthquake happened in Indonesia

This package will use BeautifulSoup4 and Request, to then produce output in the form of JSON that is ready to be used in web or mobile applications

## HOW TO USE
    import recentearthquake

    if __name__ == '__main__':
        result = recentearthquake.ekstraksi_data()
        recentearthquake.tampilkan_data(result)

## Author
Arif Setyadi