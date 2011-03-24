import os
import mc
from xml.etree import ElementTree

State = {}
Views = {}

config = None
windows = {}

def initialize(path='config.xml'):
    global config
    config = parse_config(os.getcwd() + '/' + path)    

    windows['main'] = mc.GetWindow(14000)
    windows['action'] = mc.GetWindow(14401)

def get_system_list():
    global config

    systems = []
    for slug, system in config.items():
        systems.append({'slug': slug, 'name': system['name'], 'emulatorPath': system['emulatorPath']})

    return systems

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

def launch_rom(system, romPath):
    print "launching rom"
    global config
    print "got config"
    os.system("%s '%s'" % (config[system]['emulatorPath'], romPath))

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

        for prop in ['thumbnailPath', 'publisher', 'year', 'description']:
            el = r.find(prop)

            if el != None:
                rom[prop] = el.text
            
        systems[system].setdefault('roms', []).append(rom)

    return systems

def get_window(name):
    return windows[name]

def unload():
    Views = {}
    State = {}
    windows = {}
    config = None

# class MainView(object):
#     @staticmethod
#     def get_instance():
#         global Views
#         if 'main' not in Views:
#             Views['main'] = MainView()
#         return Views['main']
# 
#     def __init__(self):
#         initialize('config.xml')
#         self.window = mc.GetWindow(14000) # get_window('main')
#         self.item_list = self.window.GetList(14055)
# 
#         items = mc.ListItems()
#         for rom in get_rom_list():
#           item = mc.ListItem(mc.ListItem.MEDIA_UNKNOWN)
#           item.SetLabel(rom['name'])
#           item.SetPath(rom['path'])
#           item.SetThumbnail(rom['thumbnailPath'])
#           item.SetProperty('description', rom['description'])
#           item.SetProperty('system', rom['system'])
#           item.SetProperty('publisher', rom['publisher'])
#           item.SetProperty('year', rom['year'])
#           items.append(item)
# 
#         self.item_list.SetItems(items)
# 
#     def on_list_item_click(self):
#         items = self.item_list.GetItems()
#         index = self.item_list.GetFocusedItem()
# 
#         item = items[index]
#         State['current_item'] = item
# 
#         action = ActionView.get_instance()
#         # launch_rom(item.GetProperty('system'), item.GetPath())
# 
# class ActionView(object):
#     @staticmethod
#     def get_instance():
#         global Views
#         if 'action' not in Views:
#             Views['action'] = ActionView()
#         return Views['action']
# 
#     def __init__(self):
#         mc.ActivateWindow(14401)
# 
#         self.item = State['current_item']
#         self.window = mc.GetWindow(14401) # get_window('action')
#         self.item_list = self.window.GetList(5000)
# 
#         items = mc.ListItems()
#         items.append(self.item)
#         self.item_list.SetItems(items)
# 
#         system = config[self.item.GetProperty('system')]
#         self.window.GetLabel(14101).SetLabel(self.item.GetProperty('publisher'))
#         self.window.GetLabel(14102).SetLabel('[COLOR grey]' + self.item.GetProperty('year') + '[/COLOR]')
#         self.window.GetLabel(14104).SetLabel(self.item.GetProperty('description'))
#         self.window.GetLabel(6013).SetLabel(system['name'])
#         self.window.GetLabel(6742).SetLabel('[COLOR grey]Path: ' + self.item.GetPath() + '[/COLOR]')
# 
#     def launch_rom(self):
#         items = self.item_list.GetItems()
#         index = self.item_list.GetFocusedItem()
# 
#         print self.item.GetPath()
#         item = items[index]
#         launch_rom(item.GetProperty('system'), item.GetPath())
