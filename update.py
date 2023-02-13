from pymongo import MongoClient

client = MongoClient("mongodb+srv://tahi:74391200@cluster0.ipj2m8y.mongodb.net/?retryWrites=true&w=majority")

db = client.remoterabbits
posts = db.posts

results = posts.find({})



# REMOVING '-', '_'

posts.update_many({}, [{"$set": {"jobtype": {"$replaceAll": {"input": "$jobtype", "find": "_" ,"replacement": " "}}}}])
posts.update_many({}, [{"$set": {"jobtype": {"$replaceAll": {"input": "$jobtype", "find": "-", "replacement": " "}}}}])




# CAPS ALL FIRST WORDS 

for post in posts.find({}):
    for field in post:
        if type(post[field]) == str:
            words = post[field].split(" ")
            if words[0].isupper():
                words = [word for word in words]
            else:
                words = [word.capitalize() for word in words]
            post[field] = " ".join(words)
    posts.update_one({"_id": post["_id"]}, {"$set": post})




# ARRAYS FOR MULTIPLE VALUES

for doc in posts.find({}):
    # Iterate through all fields in the document
    for field in doc:
        # Skip the "title" and "company" fields
        if field in ["title", "company", "link", "s_link"]:
            continue
        # If the value is a string with a comma, split it into a list
        if isinstance(doc[field], str) and "," in doc[field]:
            doc[field] = [x.strip() for x in doc[field].split(",")]
    # Update the document in the collection
    posts.update_one({"_id": doc["_id"]}, {"$set": doc})




# WORD CLASSIFIER LOCATION

usa = [ "New York City", 'Americas Only','Central America','USA Only', 'North America Only,' 'Northern America','USA timezones', 'Usa Timezones', 'North America,' 'Us Timezones','Alabama','Alaska', 'Arizona','Arkansas', 'California',  'Colorado',  'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',  'Illinois',    'Indiana',    'Iowa',    'Kansas',    'Kentucky',    'Louisiana',    'Maine',    'Maryland',    'Massachusetts',    'Michigan',    'Minnesota',    'Mississippi',    'Missouri',    'Montana',    'Nebraska',    'Nevada',    'New Hampshire',    'New Jersey',    'New Mexico',    'New York',    'North Carolina',    'North Dakota',    'Ohio',    'Oklahoma',    'Oregon',    'Pennsylvania',    'Rhode Island',    'South Carolina',    'South Dakota',    'Tennessee',    'Texas',    'Utah',    'Vermont',    'Virginia',    'Washington',    'West Virginia',    'Wisconsin',    'Wyoming', "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
europe=["EMEA","Emea","Europe Only", "UK Only", "Europe", "UK", "Uk", "European Timezones", "European timezones","Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kazakhstan", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City"]
asia = ["United Arab Emirates","Asia","APAC","Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar (Burma)", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Russia", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste (East Timor)", "Turkey", "Turkmenistan", "United Arab Emirates (UAE)", "Uzbekistan", "Vietnam", "Yemen"]
canada =["Canada Only", "Canada","Toronto", "Montreal", "Vancouver", "Ottawa", "Calgary", "Edmonton", "Mississauga", "Winnipeg", "Hamilton", "Kitchener"]
latam =[ "Latin America Only", "LATAM", "Latam", "South America","Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", "El Salvador",  "Guatemala", "Haiti","Honduras","Jamaica","Mexico", "Nicaragua","Panama","Paraguay", "Peru","Puerto Rico", "Uruguay", "Venezuela"]
africa = [ "South Africa", "North Africa","Western Africa", "Northern Africa", "Southern Africa", "Eastern Africa",   "Algeria",    "Angola",    "Benin",    "Botswana",    "Burkina Faso",    "Burundi",    "Cameroon",    "Cape Verde",    "Central African Republic",    "Chad",    "Comoros",    "Democratic Republic of the Congo",    "Djibouti",    "Egypt",    "Equatorial Guinea",    "Eritrea",    "Eswatini",    "Ethiopia",    "Gabon",    "Gambia",    "Ghana",    "Guinea",    "Guinea-Bissau",    "Ivory Coast",    "Kenya",    "Lesotho",    "Liberia",    "Libya",    "Madagascar",    "Malawi",    "Mali",    "Mauritania",    "Mauritius",    "Morocco",    "Mozambique",    "Namibia",    "Niger",    "Nigeria",    "Rwanda",    "São Tomé and Principe",    "Senegal",    "Seychelles",    "Sierra Leone",    "Somalia",    "South Africa",    "South Sudan",    "Sudan",    "Tanzania",    "Togo",    "Tunisia",    "Uganda",    "Zambia",    "Zimbabwe"]
worlwide=["Anywhere In The World", "Worldwide", "Remote Job", "Remote Worldwide", "Remote (gmt-3 To Gmt+4)", "Global"]


# SETTING VALUES ACCORDING TO ARRAY LOCATION

for post in posts.find({}):
    if post['location'] in worlwide:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'Anywhere In The World'}})
    elif post['location'] in europe:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'Europe'}})
    elif post['location'] in usa:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'USA'}})
    elif post['location'] in asia:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'Asia'}})
    elif post['location'] in latam:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'LATAM'}}) 
    elif post['location'] in canada:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'Canada'}})
    elif post['location'] in africa:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'Africa'}}) 
    else:
        posts.update_one({'_id': post['_id']}, {'$set': {'location': 'Others'}})





# UPDATE JOBTYPE 

posts.update_many({'jobtype': None}, {"$set": {"jobtype": "Other"}})
posts.update_many({'jobtype': ""}, {"$set": {"jobtype": "Other"}})



# CREATE CATEGORY BASED ON TAGS

def categorize_document(doc):
    if "tags" in doc:
        tag = doc["tags"]
    else:
       return
    if tag in [ "software","cloud", "engineer", "engineering", "golang", "developer", "go", "dev", "javascript", "typescript", "node", "testing", "code", "backend", "technical", "fintech","system", "c++",  "web", "api"]:
        return "Software Development"
    elif tag in ["manager","web3",  "marketing","growth", "leader",  "management", "analyst"]:
        return "Sales And Marketing"
    elif tag in ["financial",  "investment", "investor", "recruiter", "recruitment", "strategy",  "finance", "bank"]:
        return 'Management And Finance'
    else:
        return "All Others"

for doc in posts.find({}):
    category = categorize_document(doc)
    if category:
        posts.update_one({"_id": doc["_id"]}, {"$set": {"category": category}})

# UPDATE OTHER CATEGORY

posts.update_many({'category': "All Other Remote"}, {"$set": {"category": "All Others"}})
