from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,

)
from datetime import datetime
import sqlite3, itertools, json, uuid

app = Flask(__name__)


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
                     WHERE country.country = ?""", (country_name_query_string, )).fetchall()
        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json)

    if country_name_query_string is not None and real_offset is not None and page is not None:
        query = '''
        SELECT city FROM city 
        JOIN country USING (country_id)
        WHERE country.country =?
        LIMIT ? OFFSET ?
        '''
        args = (country_name_query_string, per_page, real_offset, )
        db = get_db()
        data = db.execute(query, args).fetchall()
        # data = db.execute("""SELECT city FROM city 
        #              JOIN country USING (country_id)
        #              WHERE country.country = ?""", (country_name_query_string, )).fetchall()
        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json)


    if per_page is not None and real_offset is not None:
        query = 'SELECT city FROM city LIMIT ? OFFSET ?'
        args = (per_page, real_offset)
        db = get_db()
        data = db.execute(query, args).fetchall()

        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json) 

    elif per_page is not None and real_offset is None:
        query = 'SELECT city FROM city LIMIT ?'
        args = (per_page,)
        db = get_db()
        data = db.execute(query, args).fetchall()

        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json) 

    else:
        query = 'SELECT city FROM city'
        args = ()

        db = get_db()
        data = db.execute(query, args).fetchall()

        data_json = []
        for i in data:
            data_json.extend(list(i))

        return jsonify(data_json) 

    # if country_name_query_string is not None :
    #     db = get_db()
    #     data = db.execute('''
    #     SELECT city, country FROM city 
    #     JOIN country ON city.country_id = country.country_id
    #     ''').fetchall()
    #     data_json = []
    #     for i in data:
    #         data_json.extend(list(i))

    #     data_json = dict(itertools.zip_longest(*[iter(data_json)] * 2, fillvalue=""))
        
    #     result_json = []
    #     for keys, values in data_json.items():
    #         if values == country_name_query_string:
    #             result_json.append(keys)

    #     return jsonify(sorted(result_json))

def post_city():
    jsondata = request.get_json()
    date = datetime.utcnow()
    unique_id = str(uuid.uuid4())

    country_id = jsondata['country_id']
    city_name = jsondata['city_name']
    db = get_db()
    db.execute(
        'INSERT INTO city (city_id, country_id, city, last_update) VALUES (?, ?, ?, ?)',
        (unique_id, country_id, city_name, date)
    )
    db.commit()

    keys = ("country_id", "city_name", "city_id")
    query = '''
    SELECT city, city_id, country_id FROM city 
    WHERE city_id = ?
    '''
    args = (unique_id, )
    db = get_db()
    data = db.execute(query, args).fetchall()
    # data_json = []
    # for i in data:
    #     data_json.extend(list(i))
    json.dumps(data)

    return data


@app.route('/lang')
def lang_list():
    query = '''
    SELECT name FROM language 
    '''
    args = ()
    db = get_db()
    data = db.execute(query, args).fetchall()
    # data = db.execute("""SELECT city FROM city 
    #              JOIN country USING (country_id)
    #              WHERE country.country = ?""", (country_name_query_string, )).fetchall()
    data_json = []
    for i in data:
        data_json.extend(list(i))

    return jsonify(data_json)


if __name__ == '__main__':
    app.run(debug=True)
