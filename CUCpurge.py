#/usr/bin/python
# coding: utf-8
import requests
from requests.auth import HTTPBasicAuth
import config as cfg
import time
import argparse
from xml.dom.minidom import parse,parseString

def get_messages(daysretency, force, simulate):
	print("Connexion")
	print cfg.CUCIP
	resp = requests.get('https://'+cfg.CUCIP+'/vmrest/mailbox/folders/inbox/messages', auth=HTTPBasicAuth(cfg.USERID, cfg.PASSWORD), verify=False)
	#print(resp)
	#print(resp.text)
	olderthaninmillisecs = daysretency*24*3600000
	now = time.time()*1000

	dom = parseString(resp.text.encode('utf8'))
	listmessages = dom.getElementsByTagName("Messages")[0]
	print listmessages.nodeName
	print listmessages.childNodes.length
	for message in listmessages.childNodes:
		for attribute in message.childNodes:
			if (attribute.nodeName == "MsgId"):
				msgid = attribute.childNodes[0].nodeValue
			if (attribute.nodeName == "Subject"):
				subject = attribute.childNodes[0].nodeValue
			if (attribute.nodeName == "Read"):
				read = attribute.childNodes[0].nodeValue
			if (attribute.nodeName == "ArrivalTime"):
				arrivaltime = attribute.childNodes[0].nodeValue
		if ((now-int(arrivaltime)) > olderthaninmillisecs):
			if (force or read=="true"):
				print subject
				print "suppression de "+msgid
				if (not simulate):
					delete_message(msgid)

def delete_message(id):
	resp = requests.delete('https://'+cfg.CUCIP+'/vmrest/messages/'+id, auth=HTTPBasicAuth(cfg.USERID, cfg.PASSWORD), verify=False)
	print (resp)
		#print str(read)+" "+str(arrivaltime)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-force", help="efface les messages non-lus egalement",
		action="store_true")
	parser.add_argument("-days", help="efface les messages plus vieux que le nombre de jours precises", type=int)
	parser.add_argument("-simulate", help="simule et affiche la liste des messages qui seront supprimés",
		action="store_true")
	args = parser.parse_args()
	if args.force:
	    force = True
	else:
		force = False
	if args.simulate:
	    simulate = True
	else:
		simulate = False
	if args.days:
		daysretency = args.days
	else:
		daysretency = 60
	get_messages(daysretency, force, simulate)