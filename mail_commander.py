import telnetlib
import json, argparse
import sys

from communication import get_communication


def get_cli_arguments():
	"""Set up ArgumentParser object
	"""
	parser = argparse.ArgumentParser(description='SMTP over telnet wrapper')
	
	parser.add_argument(
		'-r',
		'--recipient',
		help='',
		required=True
	)
	parser.add_argument(
		'-s',
		'--subject',
		help='',
		required=True
	)
	parser.add_argument(
		'-c',
		'--content',
		help='',
		required=True
	)

	return vars(parser.parse_args())

def connect_to_server(config):
	"""Connectes to server specified in configuration file

	   @param config Content of configuration file as json
	   @returns Telnet client offering interface to specified host
	"""
	return telnetlib.Telnet(config['host'], config['port'])

def send_mail(telnet, config, recipient, subject, content):
	"""Sends mail over given telnet client

	   @param telnet Telnet client conncted to specified server
	   @param config Content of configuration file as json
	   @param recipient Recipient of mail to be written
	   @param subject Subject of mail to be written
	   @param content Content of mail to be written
	   @returns None on success, undefined on failure :-)
	"""
	# talk to him
	for e in get_communication(config, recipient, subject, content):
		to_send = e['send']
		to_read = e['read']

		if to_send:
			telnet.write(to_send + b'\r\n')
			print('[SENT] - ' + to_send.decode('utf-8'))
		if to_read:
			res = b''
			while not to_read in res:
				res = telnet.read_some()
			print('[READ] - ' + to_read.decode('utf-8'))

def main():
	"""Load config and do stuff
	"""
	# load config
	try:
		config = json.load(open('config.json', 'r'))
	except FileNotFoundError:
		print('No config found, please create one.')
		sys.exit()

	# parse args
	args = get_cli_arguments()

	telnet = connect_to_server(config)
	send_mail(telnet, config, args['recipient'], args['subject'], args['content'])

if __name__ == '__main__':
	main()