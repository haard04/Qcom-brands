from urllib.parse import urlparse


categories = [
    {"name":"Cold%20Drinks%20and%20Juices", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Atta%2C%20Rice%20and%20Dal", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Ice%20Creams%20and%20Frozen%20Desserts", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Chips%20and%20Namkeens", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Chocolates", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Noodles%2C%20Pasta%2C%20Vermicelli", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Frozen%20Food", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Sweets", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Paan%20Corner", "taxonomy_type":"Speciality%20taxonomy%203"},
    {"name":"Bath%20and%20Body", "taxonomy_type":"Supermarket"},
    {"name":"Hair%20Care", "taxonomy_type":"Supermarket"},
    {"name":"Skincare", "taxonomy_type":"Supermarket"},
    {"name":"Makeup", "taxonomy_type":"Supermarket"},
    {"name":"Oral%20Care", "taxonomy_type":"Supermarket"},
    {"name":"Grooming", "taxonomy_type":"Supermarket"},
    {"name":"Baby%20Care", "taxonomy_type":"Supermarket"},
    {"name":"Fragrances", "taxonomy_type":"Supermarket"},
    {"name":"Proteins%20and%20Supplements", "taxonomy_type":"Supermarket"},
    {"name":"Feminine%20Hygiene", "taxonomy_type":"Supermarket"},
    {"name":"Sexual%20Wellness", "taxonomy_type":"Supermarket"},
    {"name":"Health%20and%20Pharma", "taxonomy_type":"Supermarket"},
    {"name":"Fresh%20Vegetables", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Fresh%20Fruits", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Dairy%2C%20Bread%20and%20Eggs", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Cereals%20and%20Breakfast", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Oils%20and%20Ghee", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Masalas", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Dry%20Fruits%20and%20Seeds%20Mix", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Biscuits%20and%20Cakes", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Tea%2C%20Coffee%20and%20Milk%20drinks", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Sauces%20and%20Spreads", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Meat%20and%20Seafood", "taxonomy_type":"Speciality%20taxonomy%201"},
    {"name":"Home%20and%20Furnishing", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Kitchen%20and%20Dining", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Cleaning%20Essentials", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Clothing", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Mobiles%20and%20Electronics", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Appliances", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Books%20and%20Stationery", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Jewellery%20and%20Accessories", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Puja", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Toys%20and%20Games", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Sports%20and%20Fitness", "taxonomy_type":"Health%20and%20Wellness%20Stores"},
    {"name":"Pet%20Supplies", "taxonomy_type":"Health%20and%20Wellness%20Stores"}
]
store_ids = [
    {"id":1402796, "location":"Ahmedabad"},
    {"id":1396282, "location":"Mumbai"},
    {"id":1402948, "location":"Bengaluru"},
    {"id":1062419, "location":"Delhi"},
    {"id":1381355, "location":"Hyderabad"},
    {"id":1380621, "location":"Kolkata"},
    {"id":1399697, "location":"Chennai"},
    {"id":1397626, "location":"Pune"}
    
]
category_name = "Atta%2C%20Rice%20and%20Dal"
store_id = "1374258"
offset = 1
taxonomy_type = ""
def get_taxonomy_type(category_name):
    for category in categories:
        if category["name"] == category_name:
            return category["taxonomy_type"]
    return None 
def swiggy_api(category_name,store_id,offset):
    taxonomy_type = get_taxonomy_type(category_name)
    filter = f""
    return f"https://www.swiggy.com/api/instamart/category-listing?categoryName={category_name}&storeId={store_id}&offset={offset}&filterName=&taxonomyType={taxonomy_type}"


def extract_slug_from_url(url):
    parts = urlparse(url).path.strip("/").split("/")
    try:
        b_index = parts.index("b")
        return parts[b_index + 1]
    except ValueError:
        return None
    


