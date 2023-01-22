import time

import pandas as pd
import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup

# file with the output
csv_file = r'data/scrapped.csv'

# list of rooms collected
rooms = []
start_time = time.time()

base_url = "https://kamernet.nl/huren/kamers-nederland"


def get_room_links(link):

    rooms_links = []

    counter = 1

    # selects all room links
    rooms_selector = ".rowSearchResultRoom div.col.s12.no-padding > div.tile-img > a"

    # loop through pages
    while True:
        current_link = f"{link}?pageno={counter}"
        # collect html
        r = requests.get(current_link)

        # print('r.text', r.text)

        soup = BeautifulSoup(r.text, "lxml")

        rooms_found = [i.get("href") for i in soup.select(rooms_selector)]

        if not rooms_found:
            print(f"no room links found at {current_link}. moving on.")
            break

        rooms_links = rooms_links + rooms_found

        counter += 1

        break
    return rooms_links[:5]


def parse_room(link):
    # collect html
    r = requests.get(link)

    room_data = BeautifulSoup(r.text, "lxml")

    # picking up the data
    image_links = room_data.select(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.pics-preview > div img"
    )
    streetCityName = room_data.select_one("#streetCityName")
    surfaceArea = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(1) > div"
    )
    price = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(2) > div.price"
    )
    unit = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(2) > div.gwe"
    )
    deliveryLevel = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(4) > div"
    )
    availability = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(5) > div"
    )
    price = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(2) > div.price"
    )
    description = room_data.select_one("div.col.s12.room-description")
    livingRoom = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(2) > div:nth-child(2) > div.text-poppins-bold"
    )
    kitchen = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(3) > div:nth-child(2) > div.text-poppins-bold"
    )
    bathroom = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(4) > div:nth-child(2) > div.text-poppins-bold"
    )
    toilet = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(5) > div:nth-child(2) > div.text-poppins-bold"
    )
    internet = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(6) > div:nth-child(2) > div.text-poppins-bold"
    )
    energy_label = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(7) > div:nth-child(2) > div.text-poppins-bold"
    )
    housemates = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(8) > div:nth-child(2) > div.text-poppins-bold"
    )
    sex = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(9) > div:nth-child(2) > div.text-poppins-bold"
    )
    pets = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(10) > div:nth-child(2) > div.text-poppins-bold"
    )
    location = room_data.select_one(
        "body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div:nth-child(9) > div.col.s12.map-address"
    )
    rooms.append(
        {
            "url": link,
            "image_links": ",".join(
                [img.get("data-src") for img in image_links]
            )
            if image_links is not None
            else "",
            "street_city_name": streetCityName.text.strip()
            if streetCityName is not None
            else "",
            "surface_area": surfaceArea.text.strip()
            if surfaceArea is not None
            else "",
            "unit": unit.text.strip() if unit is not None else "",
            "delivery_level": deliveryLevel.text.strip().split(
                "Opleverniveau: \r\n\t\t\t\t\t"
            )[-1]
            if deliveryLevel is not None
            else "",
            "availability": availability.text.strip()
            if availability is not None
            else "",
            "price": price.text.strip() if price is not None else "",
            "description": description.text.strip()
            if description is not None
            else "",
            "living_room": livingRoom.text.strip()
            if livingRoom is not None
            else "",
            "kitchen": kitchen.text.strip() if kitchen is not None else "",
            "bathroom": bathroom.text.strip() if bathroom is not None else "",
            "toilet": toilet.text.strip() if toilet is not None else "",
            "internet": internet.text.strip() if internet is not None else "",
            "energy_label": energy_label.text.strip()
            if energy_label is not None
            else "",
            "housemates": housemates.text.strip()
            if housemates is not None
            else "",
            "sex": sex.text.strip() if sex is not None else "",
            "pets": pets.text.strip() if pets is not None else "",
            "location": location.text.strip() if location is not None else "",
        }
    )

    yield


# getting links
print("getting room links..")
link_list = get_room_links(link=base_url)
print(f"{len(link_list)} links collected.")

# collecting room data
for l in link_list:
    print("")
    print(f"fetching room... >> {l} \n")
    with alive_bar(0) as bar:
        for i in parse_room(link=l):
            time.sleep(0.001)
            bar()
# creating csv file
df = pd.DataFrame(rooms)
<<<<<<< HEAD:src/scrape-kamernet.py
print('Creating csv file...')
df.to_csv (csv_file, index = None)
=======
print("creating csv file...")
df.to_csv(csv_file, index=None)
>>>>>>> 269e5396a95758121013258f22a58d698ca442a9:scrape-kamernet.py

# print('\n')
print(len(rooms), f"rooms collected. saved in {csv_file}")
