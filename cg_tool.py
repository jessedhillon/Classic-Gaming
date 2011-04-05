#!/usr/bin/env python
import os
import sys
import re

from os.path import dirname, basename, walk, isfile, isdir

from getopt import getopt
from glob import glob

import classic_gaming
from gamefaqs import GameFAQSRomIdentifier
from tools import slugify

def help_task(args):
    print "some help text"

def define_task(args):
    if len(args) < 3:
        print "usage for define"
        return

    classic_gaming.insert_system(args[0], args[1], args[2])

def list_task(args):
    if len(args) < 1:
        print "usage for list"
        return

    if args[0] == "systems":
        systems = classic_gaming.fetch_systems()
        for s in systems:
            print "%s(%s): %s" % (s['name'], s['slug'], s['path'])

    if args[0] == "roms":
        roms = classic_gaming.fetch_roms()
        for r in roms:
            print "%s (%s)" % (r['title'], r['year'])

def import_task(args):
    if len(args) < 2:
        print "usage for import"
        return

    slug = args[0]
    path = args[1]

    system = classic_gaming.get_system_by_slug(slug)
    roms = []

    def visit(arg, dirname, names):
        for name in names:
            if isfile(name):
                roms.append(name)
            if isdir(name):
                walk(name, visit)

    for p in glob(path):
        if isfile(p):
            roms.append(p)
        if isdir(p):
            walk(p, visit, None)

    def save(image, dest):
        f = open(dest, 'wb')
        f.write(image.read())

    for f in roms:
        rom = {}

        i = GameFAQSRomIdentifier(system['slug'], basename(f).split('.')[0])
        rom['publisher'] = i.get_publisher()
        rom['year'] = i.get_year()
        rom['description'] = i.get_description() 

        image_path = dirname(f) + '/images'
        try:
            os.mkdir(image_path)
        except Exception:
            pass

        ext, tmp = i.get_thumbnail()
        rom['thumbnail'] = "%s/%s-cover.%s" % (image_path, slugify(basename(f)), ext)
        save(tmp, rom['thumbnail'])

        ext, tmp = i.get_image()
        rom['image'] = "%s/%s-image.%s" % (image_path, slugify(basename(f)), ext)
        save(tmp, rom['image'])

        classic_gaming.insert_rom(system['slug'], i.get_title(), f, **rom)
        print "imported", i.get_title()

# roms = map(lambda x: basename(x), glob(rom_glob))
# print "Found roms", rom_glob, roms
# 
# query_base = "http://www.gamefaqs.com/search/index.html?"
# url_base = "http://www.gamefaqs.com"
# 
# for filename in roms:
#     print filename
#     i = GameFAQSRomIdentifier(system, filename.split('.')[0])
#     print i.get_title()
#     print i.get_publisher()
#     print i.get_year()
#     print i.get_description()
# 
#     ext, tmp = i.get_thumbnail()
#     cover_path = covers + slug(filename) + "-cover." + ext
#     cover = open(cover_path, 'wb')
#     cover.write(tmp.read())
# 
#     cover.close()
#     tmp.close()
#     print cover_path
# 
#     ext, tmp = i.get_image()
#     image_path = covers + slug(filename) + "-image." + ext
#     image = open(image_path, 'wb')
#     image.write(tmp.read())
#     print image_path
# 
#     image.close()
#     tmp.close()

def do_command(args):
    commands = {
        'help': help_task,
        'define': define_task,
        'list': list_task,
        'import': import_task,
    }

    command = None
    if len(sys.argv) > 1:
        command = args[1]
    else:
        command = 'help'

    classic_gaming.initialize()
    commands[command](args[2:])

if __name__ == '__main__':
    do_command(sys.argv)

# optlist, args = getopt(sys.argv[1:], 's:g:c:')
# optlist = dict(optlist)
# 
# system = optlist['-s']
# rom_glob = optlist['-g']
# covers = optlist['-c']
# 
# roms = map(lambda x: basename(x), glob(rom_glob))
# print "Found roms", rom_glob, roms
# 
# query_base = "http://www.gamefaqs.com/search/index.html?"
# url_base = "http://www.gamefaqs.com"
# 
# for filename in roms:
#     print filename
#     i = GameFAQSRomIdentifier(system, filename.split('.')[0])
#     print i.get_title()
#     print i.get_publisher()
#     print i.get_year()
#     print i.get_description()
# 
#     ext, tmp = i.get_thumbnail()
#     cover_path = covers + slug(filename) + "-cover." + ext
#     cover = open(cover_path, 'wb')
#     cover.write(tmp.read())
# 
#     cover.close()
#     tmp.close()
#     print cover_path
# 
#     ext, tmp = i.get_image()
#     image_path = covers + slug(filename) + "-image." + ext
#     image = open(image_path, 'wb')
#     image.write(tmp.read())
#     print image_path
# 
#     image.close()
#     tmp.close()
