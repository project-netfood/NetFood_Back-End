import pymongo


plats = pymongo.Mongoplats("mongodb://localhost:27017/")

#To get database list:
print("List of Database : {}".format(plats.list_database_names()))

#To get collection/table in database
dblist = plats.list_database_names()
for i in dblist:
    collectionlist = plats[i].list_collection_names()
    print("Collection in database {} is : {}".format(i,collectionlist))

    
)


#Select * from collection with result sorted in descending:
where = { "nom_plat": ""}
select_find = netfood.find(where).sort("age",-1)   #<--- remove where to get full result set
for x in select_find:
    print(x)
#print(select_find)

#To delete items from collection:
Delete item from netfood:
item = {"name" : "azhar"}
dlt_items = netfood.delete_one(item)   #mycollection.delete_many(item) <-- To delete many items
print(dlt_items.deleted_count, " documents deleted.")

# print("List of Database : {}".format(plats.list_database_names()))
# print("List of Collection : {}".format(plats['shop'].list_collection_names()))
