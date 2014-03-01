# specify communication to mail server
def get_communication(config, recipient, subject, content):
	return [
		{
			'send': None,
			'read': b'220'
		},
		{
			'send': b'helo ' + config['mailhost'].encode('utf-8'),
			'read': b'250'
		},
		{
			'send': b'mail from: ' + config['mailfrom'].encode('utf-8'),
			'read': b'250' # Sender OK
		},
		{
			'send': b'rcpt to: ' + recipient.encode('utf-8'),
			'read': b'250' # Recipient OK
		},
		{
			'send': b'data',
			'read': b'354'
		},
		{
			'send': b'Subject: ' + subject.encode('utf-8') + b'\r\n',
			'read': None
		},
		{
			'send': content.encode('utf-8') + b'\r\n' + b'.',
			'read': b'250' # Queued mail for delivery
		},
		{
			'send': b'quit',
			'read': b'221' # Service closing transmission channel
		}
	]