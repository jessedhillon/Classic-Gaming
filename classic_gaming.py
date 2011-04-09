import os

import mysql.connector as mysql
from xml.etree import ElementTree

State = {}
Views = {}

config = None

def initialize(path='config.xml'):
    conn = connect()
    curs = conn.cursor()
    curs.execute("""
create table if not exists
    system(
        slug varchar(20),
        name varchar(50),
        path varchar(255),
        primary key(slug)
    )
""")
    curs.execute("""
create table if not exists
    rom(
        id int not null auto_increment,
        system varchar(20),
        title varchar(50),
        path varchar(255),
        thumbnail varchar(255),
        image varchar(255),
        publisher varchar(50),
        year int,
        description text,
        primary key(id)
    )
""")
    conn.close()

def connect():
    return mysql.connect(database='classic_gaming', user='root', password='')

def insert_system(slug, name, path):
    query = "insert into system(slug, name, path) values(%s, %s, %s)"

    conn = connect()
    curs = conn.cursor()
    curs.execute(query, (slug, name, path))
    conn.close()

def get_rom_by(**kwargs):
    query = "select id, system, title, path, thumbnail, image, publisher, year, description from rom where %s = %s"

    params = []

    if 'path' in kwargs:
        params.append('path')
        params.append(kwargs['path']) 

    conn = connect()
    curs = conn.cursor()
    curs.execute(query, params)
    result = curs.fetchone()
    conn.close()

    if not result:
        return None

    return {
        'id': rom[0],
        'system': rom[1],
        'title': rom[2],
        'path': rom[3],
        'thumbnail': rom[4],
        'image': rom[5],
        'publisher': rom[6],
        'year': rom[7],
        'description': rom[8],
    }

def insert_rom(system, title, path, thumbnail='', image='', publisher='', year='', description=''):
    query = "insert into rom(system, title, path, thumbnail, image, publisher, year, description) values (%s, %s, %s, %s, %s, %s, %s, %s)"

    conn = connect()
    curs = conn.cursor()

    if not get_rom_by(path=path):
        curs.execute(query, (system, title, path, thumbnail, image, publisher, year, description))
    conn.close()

def get_system_by_slug(slug):
    query = "select slug, name, path from system where slug = %s"

    conn = connect()
    curs = conn.cursor()
    curs.execute(query, (slug,))
    result = curs.fetchone()
    conn.close()

    if not result:
        raise Exception("None or multiple results for slug = %s" % slug)

    return {
        'slug': result[0],
        'name': result[1], 
        'path': result[2]
    }

def fetch_systems(order_by='name', direction='asc'):
    query = "select slug, name, path from system order by %s"

    systems = []

    conn = connect()
    curs = conn.cursor()
    curs.execute(query, ("%s %s" % (order_by, direction)))

    for r in curs:
        systems.append({
            'slug': r[0],
            'name': r[1],
            'path': r[2]
        })
    conn.close()

    return systems

def fetch_roms():
    query = "select * from rom order by title asc"

    roms = []

    conn = connect()
    curs = conn.cursor()
    curs.execute(query)

    for r in curs:
        roms.append({
            'id': r[0],
            'system': r[1],
            'title': r[2],
            'path': r[3],
            'thumbnail': r[4],
            'image': r[5],
            'publisher': r[6],
            'year': r[7],
            'description': r[8],
        })
    conn.close()

    return roms

def get_rom_list():
    global config

    roms = []
    for slug, system in config.iteritems():
        if 'roms' in system:
            for rom in system['roms']:
                roms.append({'name': rom['name'],
                             'path': rom['path'],
                             'thumbnailPath': rom.get('thumbnailPath', ''),
                             'publisher': rom.get('publisher', ''),
                             'year': rom.get('year', ''),
                             'description': rom.get('description', ''),
                             'system': slug})

    return roms

def launch_rom(system, rom_path):
    cmd = system['path'].replace("{rom_path}", "'%s'" % rom_path)
    os.system(cmd)
