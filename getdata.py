import overpy 
import pandas as pd 
import json
import requests

def hospital(input):
    prefix = """[out:json][timeout:50];(node["amenity"="hospital"](around:"""
    suffix = """););out body;>;out skel qt;"""

    q=input[2]+','+input[0]+','+input[1]
    dquery= prefix + q + suffix
    print(dquery)
    return dquery



def overpassurl(dataquery):
    api = overpy.Overpass()
    result = api.query(dataquery)
    listofnodetags = []
    name = []
    lat = []
    longit = []
    for node in result.nodes:
        node.tags['lattitude'] = node.lat 
        node.tags['longitude'] = node.lon
        node.tags['id'] = node.id
        # name.append(node.tags['name']) #name only
        # ltt = str(node.tags['lattitude']) #working
        # lgt = str(node.tags['longitude'])
        # addr = str(node.tags['emergency']) not working since not all data have this content
        # print(node.tags['addr']+"\n")
        # lat.append(str(node.tags['lattitude'])) not working
        # longit.append(str(node.tags['longitude'])) not working 
        # lat.append(ltt) #working
        # longit.append(lgt) #working
        listofnodetags.append(node.tags)

    # data = pd.DataFrame(listofnodetags)
    # data.to_csv('outputdata.csv')
    # print(listofnodetags)
    print("Output done")
    # print(name)
    # return [name,lat,longit,listofnodetags]
    return listofnodetags

def runcode(lattitude,longitude,radius):
    input = [lattitude,longitude,radius]
    # print(input)
    nquery=hospital(input)
    data = overpassurl(nquery)
    output = ""
    # size = len(data[0])
    for i in data:
        string = ""
        for j,k in i.items():
            if(j=="addr:full"):
                string = string+"Address : "+k+"\n"
            if(j=="addr:postcode"):
                string = string+"Postcode : "+str(k)+"\n"
            if(j=="name"):
                string = "Name : "+k+"\n"+string
            if(j=="lattitude"):
                string = string+"Lattitude : "+str(k)+"\n"
            if(j=="longitude"):
                string = string+"Longitude : "+str(k)+"\n"
        output = output+"\n\n"+string
    #     output=output + "\n"
    # for i in range(size):
    #     output = output+data[0][i]+"\nLattitude = "+data[1][i]+"\nLongitude = "+data[2][i]+"\n\n"
    return output


