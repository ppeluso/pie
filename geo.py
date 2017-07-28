import requests
import geojson
from geojson import Point, Feature
import sqlite3
class GoogleLocation(object):

    def __init__(self, location_search):
        self.search = location_search.replace(" ","+")
        self.response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + self.search)
        self.json = self.response.json()
    def lat_long(self):
        return self.json["results"][0]['geometry']['location']
class ReviewGeoJSON():
    def __init__(self, title, lat, lng, score):
        self.lat = lat
        self.lng = lng
        self.title = title
        self.score = score
        self.title = self.title + "\n Score: " + str(self.score)
    @property
    def __geo_interface__(self):
        return Feature(geometry=Point((self.lng, self.lat), title=self.title))
class Review(GoogleLocation):
    def __init__(self, parlor_name, parlor_info, score):
        GoogleLocation.__init__(self,parlor_info)
        self.parlor_name = parlor_name
        self.score = score
        tmp = self.lat_long()
        self.lat = tmp['lat']
        self.lng = tmp['lng']
    def to_sql(self):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        #c.execute('DROP TABLE IF EXISTS reviews')
        c.execute('''CREATE TABLE IF NOT EXISTS reviews
             (name text, lat real, lng real, score real)''')
        dat = (self.parlor_name, self.lat, self.lng, self.score)
        c.execute('INSERT INTO reviews VALUES (?,?,?,?)', dat)
        conn.commit()
        conn.close()
if  __name__ == '__main__':
    loc = Review('Prince Street Pizza', "Prince St Pizza NY", 8.2)
    loc.to_sql()
