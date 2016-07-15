**Challenges Encountered During the Wrangling**   
  * Getting Sunday Service Time
  * Update Phone Format
  
**Data Overview**
  * data querying
  * overview of statistics
  
**Additional Data Exploring**
**Contribution Suggestion**

&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;

##**Challenges Encountered During the Wrangling**  
There are two formatting problems I need to deal with:
  * opening_hours tags have differents formats, some put Monday through Friday together, with separate weekends and public holiday, in the form of Mo-Fr, Sa, Su, PH; some just separate them all with different opening time for some day, others distinct opening hours for seasons, and I need to get Sunday service time.  
  * phone formats are not very standard, either with too many dashes and slashes, or with no space between numbers at all.

###Getting Sunday Service Time
When checking the small sample osm file, I found that in the "opening_hours" tag, there are lots of different expressions, in the form of
day and time or time-only, some with PH(public holiday) but some not, etc. I want to find out how many of them are available on Sundays.

**_\# number of restaurants or cafes open on Sundays and with wheelchair available_**  
>db.wien.aggregate([
    {"$match": {"$or": [{"amenity": "restaurant"}, {"amenity": "cafe"}], "$and": [{"service.sun_opening": "yes"}, {"service.wheelchair": "yes"}]}},{"$group": {"_id": "service_avai", "count": {"$sum": 1}}}])
  
  \>>>{u'count': 35, u'_id': u'service_avai'}


###Update Phone Format

    def update_phone(element):
        if (element.tag == "node" or element.tag == "way") and element.find("tag") != None:
            for child in element:
                if child.tag == "tag":
                    if con_pat.match(child.get("k"))and phone_pat.match(child.get("v")) == None:
                        repl_1 = child.get("v").replace("-", " ")
                        repl_2 = repl_1.replace("/", " ")<

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
        
##**Data Overview**
  * **Here is the data querying part**
  
###File Size
wien.osm -------- 757MB  
wien.json ------- 699MB

**_\# number of documents_**
>db.wien.count()

\>>>3309431

**_\# number of nodes_**
>db.wien.find({"type": "node"}).count()

\>>>3261548

**_\# number of ways_**
>db.wien.find({"type": "way"}).count()

\>>>47883

**_\# number of unique users_**
>len(db.wien.distinct("created.user"))
    
\>>>2735

**_\# top 3 contributor user_**
>db.wien.aggregate([
    {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 3}])
    
\>>>{u'count': 545146, u'_id': u'Linie29'}  
    {u'count': 222737, u'_id': u'ecdos'}  
    {u'count': 220243, u'_id': u'Dima M'}
    
**_\# number of users who posted only once_**
>db.wien.aggregate([
    {"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
    {"$group": {"_id": "$count", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}},
    {"$limit": 1}])
    
\>>>{u'count': 686, u'_id': 1}


  * **And here is an overview of some statistics**
  
**_\# Obviously, there are quite a lot of restaurant "amenity"s in the dataset, here is the number of restaurant amenity in the dataset_**
>db.wien.find({"amenity": "restaurant"}).count()

\>>>2416

**_\# I wonder how many of them are supplied with wheelchair and different smoking setups, here is the number of restaurant with wheelchair and smoking setups_**
>db.wien.aggregate([  
    {"$match": {"$and": [{"service.wheelchair": {"$exists": True}}, {"service.smoking": {"$exists": True}}]}},  
    {"$project": {  
            "wheelchair": {"$eq": ["$service.wheelchair", "yes"]},  
            "smoking": {"$or": [{"$eq": ["$service.smoking", "separated"]}, {"$eq": ["$service.smoking", "isolated"]}, {"$eq": ["$service.smoking", "no"]}]},  
            "amenity": {"$eq": ["$amenity", "restaurant"]}            
        }},  
    {"$group": {"_id": {"smoking": "$smoking", "wheelchair": "$wheelchair", "amenity": "$amenity"}, "count": {"$sum": 1}}}])
    
\>>>{u'count': 9, u'_id': {u'smoking': False, u'wheelchair': False, u'amenity': True}}  
{u'count': 58, u'_id': {u'smoking': True, u'wheelchair': False, u'amenity': True}}  
{u'count': 20, u'_id': {u'smoking': True, u'wheelchair': True, u'amenity': True}}  
{u'count': 4, u'_id': {u'smoking': False, u'wheelchair': True, u'amenity': True}}

**_\# There are 9 restaurants out of 2416, say 0.3% don't have either wheelchair or smoking setup, which sounds nice;_**  
**_there are 58 restaurants out of 2416, say 2.4% do have smoking setups but no wheelchair supply;_**  
**_there are 20 restaurants out of 2416, say 0.8% have both setups, which is not very a high number;_**  
**_finally, there are 4 restaurants out of 2416 don't have smoking setup but do have wheelchair supply, which is incredibly low._**

**_The numbers here are challenging, there could be many reasons why they are so low compared to the total number of restaurants. Probably, most of the restaurants don't realize that it is necessary to make smoking setups for people who don't smoke or who don't like that smoky smell; more than smoking-resistant awareness, restaurants may pay less attention to the importance of wheelchair accommodation. But as likely as the situation above, it is possible that the dataset is not complete enough, contributors made their huge efforts to contribute the dataset, it's nothing but normal that some details could be missed, if this is the case, all we need is just a little more carefulness to make the dataset more perfect._**
  
##**Additional Data Exploring**
**_\# top 10 cuisine_**
>db.wien.aggregate([
    {"$match": {"cuisine": {"$exists": True}}},
    {"$group": {"_id": "$cuisine", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}])
    
\>>>{u'count': 434, u'_id': u'regional'}  
{u'count': 211, u'_id': u'pizza'}  
{u'count': 181, u'_id': u'italian'}  
{u'count': 133, u'_id': u'asian'}  
{u'count': 126, u'_id': u'chinese'}  
{u'count': 86, u'_id': u'heuriger'}  
{u'count': 63, u'_id': u'burger'}  
{u'count': 58, u'_id': u'ice_cream'}  
{u'count': 57, u'_id': u'cake'}  
{u'count': 55, u'_id': u'kebab'}  

**_\# street with the most cafes_**

    cafe = db.wien.aggregate([
        {"$match": {"amenity": "cafe", "address.street": {"$exists": True}}},
        {"$group": {"_id": "$address.street", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}])
    for doc in cafe:
        print "street: %s, count: %d" % (doc["_id"].decode("utf-8"), doc["count"])   
\>>>street: Hauptstraße, count: 11

**_\# district with the most pubs_**
>db.wien.aggregate([
    {"$match": {"amenity": "pub", "address.postcode": {"$exists": True}}},
    {"$group": {"_id": "$address.postcode", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 1}])
    
\>>>{u'count': 23, u'_id': u'1010'}

**_\# top 3 popular sports_**
>db.wien.aggregate([
    {"$match": {"sport": {"$exists": True}}},
    {"$group": {"_id": "$sport", "count": {"$sum": 1}}}, 
    {"$sort": {"count": -1}},
    {"$limit": 3}]) 
    
\>>>{u'count': 247, u'_id': u'soccer'}  
{u'count': 239, u'_id': u'tennis'}  
{u'count': 72, u'_id': u'swimming'} 

**_\# top 3 sport-type-clubs that have both website and email contacts_**
>db.wien.aggregate([
    {"$match": {"$or": [{"contact.email": {"$exists": True}}, {"contact.website":{"$exists": True}}], "sport": {"$exists": True}}},
    {"$group": {"_id": "$sport", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 3}])
    
\>>>{u'count': 52, u'_id': u'table_soccer'}  
{u'count': 10, u'_id': u'golf'}  
{u'count': 7, u'_id': u'equestrian'}

##**Contribution Suggestion**
**_The open map is constributed mostly by very few people, and it would be nice that more and more people could make their own contributions to this big open map project. I think one of the reason why so few people did that is because many people don't know it, they don't know that getting started to make contribution actually is very simple, just one account and adding their neighborhood into the map._** 

**_OpenStreetMap is an amazing project that aims at building an open geographical database of the whole world. If it can by all means get more people to know about it, there will be more people that would like to contribute. But the problem is, it is somehow a technical job to contribute to the project, which could be difficult for some people to do it. Futhermore, for those people who don't care about anything about the project, they won't have interest in doing any contribution, so that OpenStreeMap can attract lots of people who do care and make huge contribution, but at the meantime in vain attract those who don't._**
