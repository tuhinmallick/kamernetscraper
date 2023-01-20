import time
from bs4 import BeautifulSoup
import requests
from alive_progress import alive_bar
import pandas as pd

# file with the output
csv_file = r'data/scrapped.csv'

# list of rooms collected
rooms = []
start_time = time.time()

base_url = 'https://kamernet.nl/huren/kamers-nederland'


def get_room_links(link):
  
  rooms_links = []
  
  counter = 1
  
  # selects all room links
  rooms_selector = '.rowSearchResultRoom div.col.s12.no-padding > div.tile-img > a'
    
  # loop through pages
  while True:
    current_link = f'{link}?pageno={counter}'
    # collect html
    r = requests.get(current_link)
    
    # print('r.text', r.text)
    
    soup = BeautifulSoup(r.text, 'lxml')

    rooms_found = [i.get('href') for i in soup.select(rooms_selector)]
        
    if len(rooms_found) == 0:
      print(f'no room links found at {current_link}. moving on.')
      break
    
    rooms_links = rooms_links + rooms_found
    
    counter += 1
    
    break
  return rooms_links[:5]


def parse_room(link):
    # collect html
    r = requests.get(link) 

    room_data = BeautifulSoup(r.text, 'lxml')
    
    # picking up the data
    image_links = room_data.select(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.pics-preview > div img'
    )
    streetCityName = room_data.select_one(
      '#streetCityName'
    )
    surfaceArea = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(1) > div'
    )
    price = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(2) > div.price'
    )
    unit = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(2) > div.gwe'
    )
    deliveryLevel = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(4) > div'
    )
    availability = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(5) > div'
    )
    price = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.top-block-wrapper > div.col.s12.m6.l6.titles-wrapper.position-relative > div:nth-child(3) > div:nth-child(2) > div.price'
    )
    description = room_data.select_one(
      'div.col.s12.room-description'
    )
    livingRoom = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(2) > div:nth-child(2) > div.text-poppins-bold'
    )
    kitchen = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(3) > div:nth-child(2) > div.text-poppins-bold'
    )
    bathroom = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(4) > div:nth-child(2) > div.text-poppins-bold'
    )
    toilet = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(5) > div:nth-child(2) > div.text-poppins-bold'
    )
    internet = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(6) > div:nth-child(2) > div.text-poppins-bold'
    )
    energy_label = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(7) > div:nth-child(2) > div.text-poppins-bold'
    )
    housemates = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(8) > div:nth-child(2) > div.text-poppins-bold'
    )
    sex = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(9) > div:nth-child(2) > div.text-poppins-bold'
    )
    pets = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div.col.s12.m12.l8.offset-l2.no-padding.room-details-info > div > div:nth-child(10) > div:nth-child(2) > div.text-poppins-bold'
    )   
    location = room_data.select_one(
      'body > main > div:nth-child(1) > div:nth-child(11) > div:nth-child(10) > div:nth-child(9) > div.col.s12.map-address'
    )
    rooms.append({
      'url': link,
      'image_links': ','.join([img.get('data-src') for img in image_links]) if not image_links == None else '',
      'street_city_name': streetCityName.text.strip() if not streetCityName == None else '',
      'surface_area': surfaceArea.text.strip() if not surfaceArea == None else '',
      'unit': unit.text.strip() if not unit == None else '',
      'delivery_level': deliveryLevel.text.strip().split('Opleverniveau: \r\n\t\t\t\t\t')[-1] if not deliveryLevel == None else '',
      'availability': availability.text.strip() if not availability == None else '',
      'price': price.text.strip() if not price == None else '',
      'description': description.text.strip() if not description == None else '',
      'living_room': livingRoom.text.strip() if not livingRoom == None else '',
      'kitchen': kitchen.text.strip() if not kitchen == None else '',
      'bathroom': bathroom.text.strip() if not bathroom == None else '',
      'toilet': toilet.text.strip() if not toilet == None else '',
      'internet': internet.text.strip() if not internet == None else '',
      'energy_label': energy_label.text.strip() if not energy_label == None else '',
      'housemates': housemates.text.strip() if not housemates == None else '',
      'sex': sex.text.strip() if not sex == None else '',
      'pets': pets.text.strip() if not pets == None else '',
      'location': location.text.strip() if not location == None else '',
    })
    
    yield
  
# getting links
print('getting room links..')
link_list = get_room_links(link=base_url)
print(f'{len(link_list)} links collected.')

      
# collecting room data
for l in link_list:
  print('')
  print(f'fetching room... >> {l} \n')
  with alive_bar(0) as bar:
    for i in parse_room(link=l):
      time.sleep(.001)
      bar()
# creating csv file
df = pd.DataFrame(rooms)
print('Creating csv file...')
df.to_csv (csv_file, index = None)

    
# print('\n')
print(len(rooms), f'rooms collected. saved in {csv_file}')
