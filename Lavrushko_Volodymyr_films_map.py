#Lavrushko_Volodymyr_films_map.py
#This program reads file locations.list and creates a html map with locations
#of films, choosed by user

from geopy.geocoders import ArcGIS
import folium

def read_file(path):
    '''(str) -> list
    Reads file with films and returns pre-edited list
    '''
    print('Opening {}...'.format(path))
    lst = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as loc:
        for i in range(14):
            loc.readline()
        for line in loc:
            lst.append(line.replace("'", "’").strip('\n').split('\t'))
    del lst[-3:]
    lst = [list(filter(None, x)) for x in lst]
    return lst


def year_dict(lst, years, num):
    '''(list, list, int) -> dict
    Turns pre-edited list into dictionary with years as keys.
    Only returns years that given in second list
    '''
    print('Building dictionary...')
    dic = {year : [] for year in years}
    for line in lst:
        check = False
        for year in years:
            if len(dic[year]) < num:
                check = True
                if year in line[0]:
                    dic[year].append(line)
        if not check:
            break
    return dic

def check_locations(dic):
    '''(dict) -> dict
    Creates new dictionary with locations as keys.
    This is requiered because there can be more than 1 film at each location
    '''
    print('Updating dictionary...')
    dic1 = {}
    for year in dic:
        dic2 = {}
        for line in dic[year]:
            if line[1] in dic2:
                dic2[line[1]][0] += '<br/>'+line[0]
            else:
                dic2.update({line[1] : [line[0]]})
        dic1.update({year : dic2})
    return dic1


def add_coordinates(dic):
    '''(dict) -> dict
    Uses geolocator ArcGIS to find exact location of each film
    '''
    geolocator = ArcGIS(timeout=10)
    for year in dic:
        for loc in dic[year]:
            print('Looking for location of {}...'.format(loc))
            location = geolocator.geocode(loc)
            dic[year][loc].append((location.latitude, location.longitude))
    return dic


def create_map(dic):
    '''(dict) -> None
    Creates map
    '''
    print('Creating map...')
    map_ = folium.Map()
    for year in dic:
        year1 = folium.FeatureGroup(name=year)
        for loc in dic[year]:
            year1.add_child(folium.Marker(location=dic[year][loc][-1],\
            popup=dic[year][loc][0], icon=folium.Icon(icon='camera')))
        map_.add_child(year1)
    map_.add_child(folium.LayerControl())
    map_.save('Map.html')


def main():
    '''(None) -> None
    The main part of program. Has two inputs from console.
    '''
    inp1 = input("Input at least three years you want to see: ").split(' ')
    assert len(inp1) >= 3
    for year in inp1:
        assert 1888 <= int(year) <= 2024, 'year is not valid'
    inp2 = int(input("How many films you want to see (from each year): "))
    assert inp2 > 0, 'Has to be bigger then 0'
    dict_ = year_dict(read_file('locations.list'), inp1, inp2)
    dict_ = add_coordinates(check_locations(dict_))
    create_map(dict_)
    print('Done.')

main()
