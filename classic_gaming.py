import os
from xml.etree import ElementTree

config = None

def initialize(path='config.xml'):
    global config
    config = parse_config(os.getcwd() + '/' + path)    
    print "results of config> " + str(config)

def get_system_list():
    global config

    systems = []
    for slug, system in config.items():
        systems.append({'slug': slug, 'name': system['name']})

    return systems

def get_rom_list():
    global config

    roms = []
    for slug, system in config.items():
        if 'roms' in system:
            for rom in system['roms']:
                print "rom> " + str(rom)
                roms.append({'name': rom['name'],
                             'path': rom['path'],
                             'thumbnailPath': rom.get('thumbnailPath', ''),
                             'publisher': rom.get('publisher', ''),
                             'year': rom.get('year', ''),
                             'system': slug})

    return roms

def launch_rom(system, romPath):
    global config
    os.system('%s %s' % (config[system]['emulatorPath'], romPath))

def parse_config(path):
    tree = ElementTree.parse(path) 
    root = tree.getroot()

    systems = {}

    for s in root.find('systems').getchildren():
        if s.tag != 'system':
            continue

        slug = s.attrib['slug']
        name = s.find('name').text
        emulatorPath = s.find('emulatorPath').text
        emulatorName = s.find('emulatorName').text

        systems[slug] = {'name': name,
                         'emulatorPath': emulatorPath,
                         'emulatorName': emulatorName}

    for r in root.find('roms').getchildren():
        if r.tag != 'rom':
            continue

        rom = {}                
        system = r.attrib['system']

        rom['name'] = r.find('name').text
        rom['path'] = r.find('path').text

        for prop in ['thumbnailPath', 'publisher', 'year']:
            el = r.find(prop)

            if el != None:
                rom[prop] = el.text
            
        systems[system].setdefault('roms', []).append(rom)

    return systems
