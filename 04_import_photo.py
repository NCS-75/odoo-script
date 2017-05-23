#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import datetime
import time
import erppeek
import os
from os import listdir
import base64

from cfg_secret_configuration import odoo_configuration_user


###############################################################################
# Odoo Connection
###############################################################################
def init_openerp(url, login, password, database):
    openerp = erppeek.Client(url)
    uid = openerp.login(login, password=password, database=database)
    user = openerp.ResUsers.browse(uid)
    tz = user.tz
    return openerp, uid, tz

openerp, uid, tz = init_openerp(
    odoo_configuration_user['url'],
    odoo_configuration_user['login'],
    odoo_configuration_user['password'],
    odoo_configuration_user['database'])


###############################################################################
# Script
###############################################################################

def send_image(liste, folder_path,bool_assoc):
    print "number of objects in folder path : ", len(listdir(folder_path))
    count = 0
    for m in liste :
            file_path = folder_path+str(m.ref)+".JPG"
            if bool_assoc :
                file_path = folder_path+str(m.parent_id.ref)+".JPG"
            print file_path
            if os.path.isfile(file_path):
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    print "send picture"
                    m.image = encoded_string
                    print '   => photo enregistrée'
            else:
                print "    => pas de photo"
            count=count+1
            print count


associated_people_ids = openerp.search('res.partner', [('is_associated_people', '=', True), ('barcode_base', '!=', False)])
members_ids = openerp.search('res.partner', [('is_associated_people', '=', False), ('barcode_base', '!=', False)])

associated_poeple = openerp.ResPartner.browse([('id', 'in', associated_people_ids)])
members = openerp.ResPartner.browse([('id', 'in', members_ids)])

print ">>>>>>>> Number of members people found: ", len(members)
send_image(members, "/home/louve-erp-dev/photos/cooperateurs/", False)

print ">>>>>>>> Number of associated people found: ", len(associated_people)
send_image(associated_people, "/home/louve-erp-dev/photos/rattaches", True)
