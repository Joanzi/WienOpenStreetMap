# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import json

filename = "D:\Udacity\wien.osm"
tree = ET.parse(filename)
root = tree.getroot()

#valid postcode
pc_pat = re.compile(r"^1[0-1][1-9]0|1100|12[0-3]0|1[3-4]00$")
count = 0
for element in root:
    for child in element:
        if child.tag == "tag":
            if child.get("k") == "postcode" and pc_pat.match(child.get("v")) == None:
                count += 1
print count


#any city name not "wien"
c_pat = re.compile(r".*\bcity\b$")
count = 0
for element in root:
    for child in element:
        if child.tag == "tag":
            if c_pat.match(child.get("k")) and child.get("v") != "Wien":
                    count += 1
print count

                 
#any non-standard phone form
phone_pat = re.compile(r"^\+?43\s1\s\d{3,12}$")
con_pat = re.compile(r".*\bphone\b$")
count = 0
for element in root:
    for child in element:
        if child.tag == "tag":
            if con_pat.match(child.get("k"))and phone_pat.match(child.get("v")) == None:
                count += 1           
print count

#update phone form
def update_phone(element):
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        for child in element:
            if child.tag == "tag":
                if con_pat.match(child.get("k"))and phone_pat.match(child.get("v")) == None:
                    repl_1 = child.get("v").replace("-", " ")
                    repl_2 = repl_1.replace("/", " ")
    
                    num_lst = repl_2.split(" ")
                    if num_lst[0] == "+43" or num_lst == "43":
                        num_lst.remove(num_lst[0])
                        if num_lst[0] == "1" or num_lst[0] == "(0)1" or num_lst[0] == "(1)" or num_lst[0] == "(01)" or num_lst[0] == "01":
                            num_lst.remove(num_lst[0])
                            phone = "+43 1 "
                            for i in range(len(num_lst)):
                                phone += num_lst[i]
                            child.set("v", phone)
    return element
                     
#if sunday availble, returns true, otherwise false
def sun_opening(element):
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        tags = element.findall("tag")
        pat = re.compile('^\d{1,2}:\d{2} ?\- ?\d{1,2}:\d{2}$')
        for tag in tags:
            if "opening_hours" in tag.get("k"):
                if "Su" in tag.get("v") and "Su off" not in tag.get("v") and "Su,PH off" not in tag.get("v") or pat.match(tag.get("v")):
                    tag.set("k", "sun_opening",)
                    tag.set("v", "yes")
                else: 
                    tag.set("k", "sun_opening",)
                    tag.set("v", "no")
    return element


#contact element: phone, website and email
def fetch_contact(element):
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "phone" in v or "website" in v or "email" in v or \
        "contact:phone" in v or "contact:website" in v or "contact:email" in v:
            contact = []
            for child in element:
                if child.tag == "tag": 
                    if "contact" in child.get("k"):
                        k = child.get("k").split(':')[1]
                        if k == "phone": 
                            contact.append(k)
                        elif k == "website":
                            contact.append(k)
                        elif k == "email":
                            contact.append(k)
                    elif "contact" not in child.get("k"):
                        k = child.get("k")
                        if k == "phone": 
                            contact.append(k)
                        elif k == "website":
                            contact.append(k)
                        elif k == "email":
                            contact.append(k)
            return contact
        
def fetch_contact_val(element):
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        element = update_phone(element)
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "phone" in v or "website" in v or "email" in v or \
        "contact:phone" in v or "contact:website" in v or "contact:email" in v:
            contact_val = []
            d = {}
            for child in element: 
                if child.tag == "tag":
                    if "contact" in child.get("k"):
                        k = child.get("k").split(':')[1]
                        d[k] = child.get("v")
                        if k == "phone": 
                            contact_val.append(d[k])
                        elif k == "website":
                            contact_val.append(d[k])
                        elif k == "email":
                            contact_val.append(d[k])
                    elif "contact" not in child.get("k"):
                        k = child.get("k")
                        d[k] = child.get("v")
                        if k == "phone": 
                            contact_val.append(d[k])
                        elif k == "website":
                            contact_val.append(d[k])
                        elif k == "email":
                            contact_val.append(d[k])
            return contact_val

#service element: "sun_opening", "wheelchair" and "smoking"
def fetch_service(element):
    element = sun_opening(element)
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "wheelchair" in v or "sun_opening" in v or "smoking" in v:
            service = []
            for child in element:
                if child.tag == "tag":
                    k = child.get("k")
                    if k == "wheelchair": 
                        service.append(k)
                    elif k == "sun_opening":
                        service.append(k)
                    elif k == "smoking":
                        service.append(k)
            return service

def fetch_service_val(element):
    element = sun_opening(element)
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "wheelchair" in v or "sun_opening" in v or "smoking" in v:
            service_val = []
            d = {}
            for child in element:  
                if child.tag == "tag":
                    k = child.get("k")
                    d[k] = child.get("v")
                    if k == "wheelchair": 
                        service_val.append(d[k])
                    elif k == "sun_opening":
                        service_val.append(d[k])
                    elif k == "smoking":
                        service_val.append(d[k])
            return service_val

#address element: "housenumber", "postcode" and "street"            
def fetch_address(element):
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "housenumber" in v or "postcode" in v or "street" in v or \
        "addr:housenumber" in v or "addr:postcode" in v or "addr:street" in v:
            address = []
            for child in element:
                if child.tag == "tag":
                    if "addr" in child.get("k"):
                        k = child.get("k").split(":")[1]
                        if k == "housenumber": 
                            address.append(k)
                        elif k == "postcode":
                            address.append(k)
                        elif k == "street":
                            address.append(k)
                    elif "addr" not in child.get("k"):
                        k = child.get("k")
                        if k == "housenumber": 
                            address.append(k)
                        elif k == "postcode":
                            address.append(k)
                        elif k == "street":
                            address.append(k)
            return address

def fetch_address_val(element):
    if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "housenumber" in v or "postcode" in v or "street" in v or \
        "addr:housenumber" in v or "addr:postcode" in v or "addr:street" in v:
            address_val = []
            d ={}
            for child in element:
                if child.tag == "tag":
                    if "addr" in child.get("k"):
                        k = child.get("k").split(":")[1]
                        d[k] = child.get("v")
                        if k == "housenumber": 
                            address_val.append(d[k])
                        elif k == "postcode":
                            address_val.append(d[k])
                        elif k == "street":
                            address_val.append(d[k])
                    elif "addr" not in child.get("k"):
                        k = child.get("k")
                        d[k] = child.get("v")
                        if k == "housenumber": 
                            address_val.append(d[[k]])
                        elif k == "postcode":
                            address_val.append(d[k])
                        elif k == "street":
                            address_val.append(d[k])
            return address_val

#show the limited speed of this way.
def fetch_lit_speed(element):
    if element.tag == "way" and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "lit" in v or "maxspeed" in v:
            lit_speed = []
            for child in element:
                if child.tag == "tag":
                    k = child.get("k")
                    if k == "lit":
                        lit_speed.append(k)
                    elif k == "maxspeed":
                        lit_speed.append(k)
            return lit_speed

def fetch_lit_speed_val(element):
    if element.tag == "way" and element.find("tag") != None:
        tags = element.findall("tag")
        v = []
        for tag in tags:
            k = tag.get("k")
            v.append(k)
        if "lit" in v or "maxspeed" in v:
            lit_speed_val = [] 
            d = {}
            for child in element: 
                if child.tag == "tag":
                    k = child.get("k")
                    d[k] = child.get("v")
                    if k == "lit":
                        lit_speed_val.append(d[k])
                    elif k == "maxspeed":
                        lit_speed_val.append(d[k])
            return lit_speed_val
                
                
                
# "created" field in data model
created = ["version", "changeset", "timestamp", "user", "uid"]

def jsn_doc(element):
    if element.tag == "node" or element.tag == "way":
        doc = {}
        #another two fields "id" and "visible"
        doc["id"] = element.get("id")
        doc["visible"] = element.get("visible")
        #add "created" field values into the json document
        created_val = [element.get("version"), element.get("changeset"), element.get("timestamp"), element.get("user"), element.get("uid")]
        created_dic = dict(zip(created, created_val))
        doc["created"] = created_dic
        #add "address" field values into the json document
        address = fetch_address(element)
        address_val = fetch_address_val(element)
        if address != None and address_val != None:
            address_dic = dict(zip(address, address_val))
            doc["address"] = address_dic
        #add "contact" field values into the json document
        contact = fetch_contact(element)
        contact_val = fetch_contact_val(element)
        if contact != None and contact_val != None:
            contact_dic = dict(zip(contact, contact_val))
            doc["contact"] = contact_dic
        #add "service" field values into the json document    
        service = fetch_service(element)
        service_val = fetch_service_val(element)
        if service != None and service_val != None:
            service_dic = dict(zip(service, service_val))
            doc["service"] = service_dic
        #add "name", "amenity", "cuisine", "shop" and "sport" fields and respective values into the json document
        #if they don't exist in the osm file tag, they will be "Null" in json data, which could be easily filtered by Mongo query 
        d = {}
        if element.find("tag") != None:
            for child in element:
                if child.tag == "tag":
                    k = child.get("k")
                    d[k] = child.get("v")
                    if k == "name":
                        doc["name"] = d[k]
                    if k == "amenity":
                        doc["amenity"] = d[k]
                    if k == "cuisine":
                        doc["cuisine"] = d[k]
                    if k == "shop": 
                        doc["shop"] = d[k]
                    if k == "sport":
                        doc["sport"] = d[k]
        #add "type" and "pos" fields and respective values into json document if the tag is "node"            
        if element.tag == "node":
            doc["type"] = "node"
            doc["pos"] = [element.get("lat"), element.get("lon")]
        #add "type" field value into the json document if the tag is "way"    
        elif element.tag == "way":
            doc["type"] = "way"
            #add "lit_speed" field values into json document
            lit_speed = fetch_lit_speed(element)
            lit_speed_val = fetch_lit_speed_val(element)
            if lit_speed != None and lit_speed_val != None:
                lit_speed_dic = dict(zip(lit_speed, lit_speed_val))
                doc["lit_speed"] = lit_speed_dic
            #add "ref" field values into json document
            ref = []
            for child in element:
                if child.tag == "nd":
                    ref.append(child.get("ref"))
            doc["ref"] = ref
        
        return doc
   
fname = open("D:\Udacity\wien.json","w")
for _, element in ET.iterparse(filename):
    doc = jsn_doc(element)
    if doc != None:
        fname.write(json.dumps(doc))
        

#load file from MongoDB
from pymongo import MongoClient
client = MongoClient()

db = client.UdaPro
collection = db.wien

#file size
wien.osm -------- 757MB
wien.json ------- 699MB

#number of documents
print db.wien.count()
 
#number of nodes
print db.wien.find({"type": "node"}).count()

#number of ways
print db.wien.find({"type": "way"}).count()

#number of unique users
uni_users = db.wien.aggregate([
    {"$group": {"_id": "$created.user"}},
    {"$group": {"_id": "uni_users", "count": {"$sum": 1}}}                              
])
for doc in uni_users:
    print doc
#simple way to calculate the number:
print len(db.wien.distinct("created.user"))


#top 3 contributor user
users = db.wien.aggregate([
    {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 3}                           
])
for doc in users:
    print doc


#number of users who posted only once
users = db.wien.aggregate([
    {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
    {"$group": {"_id": "$count", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}},
    {"$limit": 1}
])
for doc in users:
    print doc



# top 10 cuisine
top_cui = db.wien.aggregate([
    {"$match": {"cuisine": {"$exists": True}}},
    {"$group": {"_id": "$cuisine", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}                             
])
for doc in top_cui:
    print doc

    
#street with the most cafes
cafe = db.wien.aggregate([
    {"$match": {"amenity": "cafe", "address.street": {"$exists": True}}},
    {"$group": {"_id": "$address.street", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 1}
])
for doc in cafe:
    print "street: %s, count: %d" % (doc["_id"].decode("utf-8"), doc["count"])



#number of restaurants or cafes open on Sundays and with wheelchair available
service_avai = db.wien.aggregate([
    {"$match": {"$or": [{"amenity": "restaurant"}, {"amenity": "cafe"}], "$and": [{"service.sun_opening": "yes"}, {"service.wheelchair": "yes"}]}},
    {"$group": {"_id": "service_avai", "count": {"$sum": 1}}}                             
])
for doc in service_avai:
    print doc


#district with the most pubs
pub = db.wien.aggregate([
    {"$match": {"amenity": "pub", "address.postcode": {"$exists": True}}},
    {"$group": {"_id": "$address.postcode", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 1}                         
])
for doc in pub:
    print doc


#top 3 popular sports
pop_spt = db.wien.aggregate([
    {"$match": {"sport": {"$exists": True}}},
    {"$group": {"_id": "$sport", "count": {"$sum": 1}}}, 
    {"$sort": {"count": -1}},
    {"$limit": 3}                         
])    
for doc in pop_spt:
    print doc 


#top 3 sport-type-clubs that have both website and email contacts
wemail = db.wien.aggregate([
    {"$match": {"$or": [{"contact.email": {"$exists": True}}, {"contact.website":{"$exists": True}}], "sport": {"$exists": True}}},
    {"$group": {"_id": "$sport", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 3}                           
])
for doc in wemail:
    print doc



#the number of restaurant amenity in the dataset:
print db.wien.find({"amenity": "restaurant"}).count()

#the number of restaurant with wheelchair and 
ws = db.wien.aggregate([
    {"$match": {"$and": [{"service.wheelchair": {"$exists": True}}, {"service.smoking": {"$exists": True}}]}},
    {"$project": {
            "wheelchair": {"$eq": ["$service.wheelchair", "yes"]},
            "smoking": {"$or": [{"$eq": ["$service.smoking", "separated"]}, {"$eq": ["$service.smoking", "isolated"]}, {"$eq": ["$service.smoking", "no"]}]},
            "amenity": {"$eq": ["$amenity", "restaurant"]}        
        }},
    {"$group": {"_id": {"smoking": "$smoking", "wheelchair": "$wheelchair", "amenity": "$amenity"}, "count": {"$sum": 1}}}                    
])
for doc in ws:
    if doc["_id"]["amenity"] == True:
        print doc 

