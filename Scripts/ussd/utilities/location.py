import requests
def dist(elem):
    return elem[1]['travelDistance']


def sortlocations(lat,lon,destlist):
    origin=str(lat)+","+str(lon)
    dest=""
    for i in range(len(destlist)):
        dest+=str(destlist[i].lat)+","+str(destlist[i].lon)+";"
    dest=dest[:-1]
    url="https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins="+origin+"&destinations="+dest+"&travelMode=driving&key=Aqxws6GyR0KaQH-uo9w92nqNeePHAzsbkVDbrpiayIiAwfTbXcML-wj1XLEBPQcQ"
    result=requests.get(url)
    result=result.json()
    result=result['resourceSets'][0]['resources'][0]['results']
    destlist, _ = (list(t) for t in zip(*sorted(zip(destlist,result),key=dist)))
    return destlist

def reversegeocode(lat,lon):
    point=lat+","+lon
    url="http://dev.virtualearth.net/REST/v1/Locations/"+point+"?o=json&key=Aqxws6GyR0KaQH-uo9w92nqNeePHAzsbkVDbrpiayIiAwfTbXcML-wj1XLEBPQcQ"
    result=requests.get(url)
    result=result.json()
    result=result['resourceSets'][0]['resources'][0]['name']
    return result