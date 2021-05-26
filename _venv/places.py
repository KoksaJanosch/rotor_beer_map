import folium
import os, sys, json
from folium.plugins import MarkerCluster


def nahraj_geojson(jmeno_souboru):
    """ Načte soubor typu geojson a ošetří nekorektní vstupy. """
    try:
        with open(os.path.join(sys.path[0], jmeno_souboru+".json"), "r", encoding="utf-8-sig") as file:
            data = json.load(file)

    except PermissionError:
        print(f"K souboru {jmeno_souboru} nemá program přístup.")
        exit()
    except FileNotFoundError:
        print(f"Soubor {jmeno_souboru} nebyl nenalezen.")
        exit()
    except ValueError:
        print(f"Soubor {jmeno_souboru} je chybný.")
        exit()

    return data


# ! Hlavní část programu
data = nahraj_geojson("rozvoz")

# ? mapa
mapa = folium.Map(location=[49.8323483, 15.6985767], zoom_start=8)
marker_cluster = MarkerCluster().add_to(mapa)

# geojson parcelování
for feature in data['features']:
    x_geo = feature['lat']
    y_geo = feature['lon']
    nazev = feature['nazev']
    adresa = feature['adresa']
    kraj = feature['kraj']
    url = feature['url']

    html = """<b>{nazev}</b><br>
                    {adresa}<br>
                    {kraj}<br>
                    <a href="{url}">{url}</a> """

    html_complete = html.format(nazev=nazev, adresa=adresa, kraj=kraj, url=url)
    info = folium.Html(html_complete, script=True)
    popup = folium.Popup(info, max_width=2650)

    tooltips = f'''<b>{nazev}</b> <br />\
                {adresa}<br />\
                {kraj}'''

    # ? Vytváření bodů
    folium.Marker(location=[x_geo, y_geo], tooltip=tooltips, popup=popup,
                  icon=folium.Icon(color="green", icon_color="white", icon="glyphicon glyphicon-ok-sign")).add_to(marker_cluster)

mapa.save("./index.html")


