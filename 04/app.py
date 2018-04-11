from flask import (
    Flask,
    g,
    make_response,
    request,
    jsonify,

)
from datetime import datetime
import sqlite3, itertools

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False



DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return 'Hello!'

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
        real_offset = (int(page)-1)*int(per_page)

    if country_name_query_string is not None and real_offset is None and page is None:
        db = get_db()
        data = db.execute("""SELECT city FROM city
                     JOIN country USING (country_id)
                     WHERE country.country = ?
                     ORDER BY city COLLATE NOCASE ASC
                    """, (country_name_query_string, )).fetchall()
        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json)

    if country_name_query_string is not None and real_offset is not None and page is not None:
        query = '''
        SELECT city FROM city 
        JOIN country USING (country_id)
        WHERE country.country =?
        ORDER BY city COLLATE NOCASE ASC
        LIMIT ? OFFSET ? 
        '''
        args = (country_name_query_string, per_page, real_offset, )
        db = get_db()
        data = db.execute(query, args).fetchall()
        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json)


    if per_page is not None and real_offset is not None:
        query = 'SELECT city FROM city ORDER BY city COLLATE NOCASE ASC LIMIT ? OFFSET ? '
        args = (per_page, real_offset)
        db = get_db()
        data = db.execute(query, args).fetchall()

        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json) 

    elif per_page is not None and real_offset is None:
        query = 'SELECT city FROM city ORDER BY city COLLATE NOCASE ASC LIMIT ? '
        args = (per_page,)
        db = get_db()
        data = db.execute(query, args).fetchall()

        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json) 

    else:

        query = 'SELECT city FROM city ORDER BY city COLLATE NOCASE ASC' 
        args = ()

        db = get_db()
        data = db.execute(query, args).fetchall()

        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json) 

def post_city():
    jsondata = request.get_json()

    date = datetime.utcnow()

    country_id = jsondata['country_id']
    city_name = jsondata['city_name']

    db = get_db()
    country_keys = db.execute('SELECT country_id FROM country').fetchall()
    db.commit()
    keys_country = []
    for i in country_keys:
        keys_country.extend(list(i))

    if country_id in keys_country:
        db = get_db()
        db.execute(
            'INSERT INTO city (country_id, city, last_update) VALUES (?, ?, ?)',
            (country_id, city_name, date)
        )
        db.commit()

        query = '''
                SELECT city_id FROM city 
                WHERE city.city =?
                '''
        args = (city_name,)
        db = get_db()
        data = db.execute(query, args).fetchone()
        r = '{}'.format(data[0])

        jsondata = {"country_id":country_id, "city_name":city_name, "city_id":r}
        return make_response(jsonify(jsondata), 200)
    else:
        error_msg = {"error": "Invalid country_id"}
        return make_response(jsonify(error_msg), 400)

@app.route('/lang_roles')
def lang_list():

    query = '''
    SELECT name, COUNT(*) from language
    join film using (language_id)
    JOIN film_actor using (film_id) 
    GROUP by name
   
    '''
    args = ()
    db = get_db()
    data = db.execute(query, args).fetchall()
    data_json = []
    for i in data:
        data_json.extend(list(i))


    data_json = dict(itertools.zip_longest(*[iter(data_json)] * 2, fillvalue=""))

    return jsonify(data_json)

if __name__ == '__main__':
    app.run(debug=True)
