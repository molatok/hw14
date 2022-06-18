import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    
    def __del__(self):
        self.cur.close()
        self.con.close()


def film_by_title(title):
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT *
        from netflix
        where title like '%{title}%'
        order by release_year desc """)
    result = db_connect.cur.fetchone()
    return {'title': result[2],
            'country': result[5],
            'release_year': result[7],
            'genre': result[1],
            'description': result[12]}


def film_by_release(years_start, years_end):
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, release_year from netflix where release_year between {years_start} and {years_end} limit 100""")
    result = db_connect.cur.fetchall()
    all_films = []
    for film in result:
        all_films.append({'title': film[0],
                          'release_year': film[1]})
    return result


def film_by_rating(rating):
    db_connect = DbConnect('netflix.db')
    rating_parametrs = {
        'children': "'G'",
        'family': "'G', 'PG', 'PG-13'",
        'adult': "'R', 'NC-17'"
    }
    if rating not in rating_parametrs:
        return "Выбран несуществующий параметр"
    query = f'select title, rating, description from netflix where rating in ({rating_parametrs[rating]})'
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    all_films = []
    for film in result:
        all_films.append({'title': film[0],
                          'rating': film[1],
                          'description': film[2]})
    return result


def film_by_genre(genre):
    db_connect = DbConnect('netflix.db')
    query = (
        f'''select title, description from netflix where listed_in like '%{genre}%' order by release_year desc limit 10;''')
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    all_films = []
    for film in result:
        all_films.append({'title': film[0],
                          'description': film[1]})
    return result


def cast_partners(name1, name2):
    db_connect = DbConnect('netflix.db')
    query = (f'''select `cast` from netflix where `cast` like '%{name1}%' and `cast` like '%{name2}%';''')
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    name_list = []
    for name in result:
        name_list.extend(name[0].split(', '))
    final_list = []
    counter = Counter(name_list)
    for actor, count in counter.items():
        if actor not in [name1, name2] and count > 2:
            final_list.append(actor)
    return final_list


def custom_search(input_type, release_year, genre):
    db_connect = DbConnect('netflix.db')
    query = (
        f'''select title, description from netflix where type = '{input_type}' and release_year = {release_year} and listed_in like '%{genre}%';''')
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({'title': movie[0],
                            'description': movie[1]}
                           )
    
    return result_list


print(custom_search('TV Show', 2020, 'Drama'))
