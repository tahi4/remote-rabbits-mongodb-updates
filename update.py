from pymongo import MongoClient

client = MongoClient("mongodb+srv://tahi:74391200@cluster0.ipj2m8y.mongodb.net/?retryWrites=true&w=majority")

db = client.remoterabbits
posts = db.posts

results = posts.find({})



posts.update_many({}, [{"$set": {"jobtype": {"$replaceAll": {"input": "$jobtype", "find": "_" ,"replacement": " "}}}}])
posts.update_many({}, [{"$set": {"jobtype": {"$replaceAll": {"input": "$jobtype", "find": "-", "replacement": " "}}}}])


# CAPS ALL FIRST WORDS 
for post in posts.find({}):
    for field in post:
        if type(post[field]) == str:
            post[field] = " ".join([word.capitalize() for word in post[field].split(" ")])
    posts.update_one({"_id": post["_id"]}, {"$set": post})



# ARRAYS FOR MULTIPLE VALUES

for doc in posts.find({}):
    # Iterate through all fields in the document
    for field in doc:
        # Skip the "title" and "company" fields
        if field in ["title", "company"]:
            continue
        # If the value is a string with a comma, split it into a list
        if isinstance(doc[field], str) and "," in doc[field]:
            doc[field] = [x.strip() for x in doc[field].split(",")]
    # Update the document in the collection
    posts.update_one({"_id": doc["_id"]}, {"$set": doc})













# SETTING VALUES ACCORDING TO ARRAY

# posts.update_many({"location": {"$in": ["Global", "Remote Job", "International", "Anywhere", "Anywhere In The World"]}}, [{"$set": {"location": "Worldwide"}}])




# x_y_z =  ["Global", "Remote Job", "International", "Anywhere", "Anywhere In The World", "Worldwide"]
# one_two_three = ["Europe", "Europe - Remote", "Anywhere, But European Timezones Preferred (or At Least A Significant Overlap With European Timezones).", "Uk", "Europe, Uk", "Germany, Switzerland", "Portugal", "Europe, Germany, Belgium", "Germany", "European Timezones", "Uk, Germany", "Uk, Ireland", "Portugal, Spain", "Finland", ]


# for post in posts.find():
#     if post['field'] in x_y_z:
#         posts.update_one({'_id': post['_id']}, {'$set': {'field': 'Anywhere In The World'}})
#     elif post['field'] in one_two_three:
#         posts.update_one({'_id': post['_id']}, {'$set': {'field': 'Europe'}})
#     else:
#         posts.update_one({'_id': post['_id']}, {'$set': {'field': 'Others'}})