import json
import csv

csv_files = ["ad.csv", "category.csv", "location.csv", "user.csv"]
json_files = ["ads.json", "categories.json", "locations.json", "users.json"]
fields = [
    # {
    #         "name": row['name'],
    #         "author": int(row['author_id']),
    #         "price": int(row['price']),
    #         "description": row['description'],
    #         'is_published': True if row['is_published'] == 'TRUE' else False,
    #         "image": row['image'],
    #         "category": int(row['category_id']),
    # },
    # {
    #     "name": row['name'],
    # },
    # {
    #     "name": row["name"],
    #     "lat": row["lat"],
    #     "lng": row["lng"],
    # },
    # {
    #     "first_name": row["first_name"],
    #     "last_name": row["last_name"],
    #     "username": row["username"],
    #     "password": row["password"],
    #     "role": row["role"],
    #     "age": int(row["age"]),
    #     "location": int(row["location_id"]),
    # }
]

ads_list = []

with open(csv_files[2]) as f:
    csv = csv.DictReader(f)
    for row in csv:
        fields = {
            "name": row["name"],
            "latitude": row["lat"],
            "longitude": row["lng"]
        }
        ad = {
            "model": "ads.location",
            "pk": int(row['id']),
            "fields": fields
        }

        ads_list.append(ad)

with open(json_files[2], "w") as f:
    json.dump(ads_list, f, ensure_ascii=False, indent=2)
