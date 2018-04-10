from flask import (
    Flask,
    request,
    make_response,
    jsonify,

)
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, LargeBinary, Numeric, \
    SmallInteger, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy import create_engine
from datetime import datetime
import json, uuid

engine = create_engine('postgres://nrhrgkdolvosii:8fd7b44ae8d287dd52f01762c1b91290572540c46967aafd749e4a636e2d29a5@ec2-54-246-84-200.eu-west-1.compute.amazonaws.com:5432/d8g9osslceaoai')

# engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
metadata = Base.metadata

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False




class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    country_id = Column(ForeignKey('country.country_id', ondelete='NO ACTION', onupdate='CASCADE'), nullable=False,
                        index=True)
    last_update = Column(DateTime, nullable=False)

    country = relationship('Country', backref='city')


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(SmallInteger, primary_key=True)
    country = Column(String(50), nullable=False)
    last_update = Column(DateTime)

    # city = relationship('City')




# def new_alchemy_encoder():
#     _visited_objs = []
#
#     class AlchemyEncoder(json.JSONEncoder):
#         def default(self, obj):
#             if isinstance(obj.__class__, DeclarativeMeta):
#                 # don't re-visit self
#                 if obj in _visited_objs:
#                     return None
#                 _visited_objs.append(obj)
#
#                 # an SQLAlchemy class
#                 fields = {}
#                 for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                     fields[field] = obj.__getattribute__(field)
#                 # a json-encodable dict
#                 return fields
#
#             return json.JSONEncoder.default(self, obj)
#
#     return AlchemyEncoder
#

@app.route('/')
def home():
    return 'Hello'


@app.route('/cities', methods=['GET', 'POST'])
def city_list():
    country_name_query_string = request.args.get('country_name')
    per_page = request.args.get('per_page')
    page = request.args.get('page')
    real_offset = None

    if request.method == 'POST':
            return post_city()

    if per_page is not None and per_page.isnumeric():
        int(per_page)

    if page is not None and page.isnumeric():
        int(page)
        real_offset = (int(page) - 1) * int(per_page)

    if country_name_query_string is not None and real_offset is None and page is None:
        all_cities = session.query(City.city)
        cities_filter = all_cities.filter(City.country.has(country=country_name_query_string))
        data_json = []
        for i in cities_filter:
            data_json.extend(list(i))
        return jsonify(data_json)

    elif country_name_query_string is not None and real_offset is not None and page is not None:
        all_cities = session.query(City.city)
        cities_filter = all_cities.filter(City.country.has(country=country_name_query_string)).limit(per_page).offset(
            real_offset)
        data_json = []
        for i in cities_filter:
            data_json.extend(list(i))
        return jsonify(data_json)

    else:
        all_cities = session.query(City.city)
        data_json = []
        for i in all_cities:
            data_json.extend(list(i))
        return jsonify(data_json)

def post_city():
    jsondata = request.get_json()

    date = datetime.utcnow()
    unique_id = str(uuid.uuid4())

    country_id = jsondata['country_id']
    city_name = jsondata['city_name']

    country_keys = session.query(Country.country_id)

    keys_country = []
    for i in country_keys:
        keys_country.extend(list(i))

    if country_id in keys_country:
        all_cities = session.query(City)
        new_entry = City(
            city_id = 0,
            country_id = country_id,
            city = city_name,
            last_update = date
        )
        session.add(new_entry)
        session.commit()
        jsondata = {"country_id":country_id, "city_name":city_name, "city_id":unique_id}
        return make_response(jsonify(jsondata), 200)
    else:
        error_msg = {"error": "Invalid country_id"}
        return make_response(jsonify(error_msg), 400)

if __name__ == '__main__':
    app.run(debug=True)