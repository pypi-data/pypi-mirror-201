from ..shared.helpers import updateEnvironmentVariablesFromJsonConfig,getPathRelativeToSkynamoDataFolder
from typing import List

def sendEmailUsingGmailCredentialsWithFilesAttached(subject: str, body: str, recipients: List[str], files: list) -> None:
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase
	from email import encoders
	from email.mime.application import MIMEApplication

	## get sender and sender password from environment variables
	import os
	if 'SKYNAMO_GMAIL_SENDER' not in os.environ:
		updateEnvironmentVariablesFromJsonConfig()
	sender=os.environ.get('SKYNAMO_GMAIL_SENDER')
	senderPassword=os.environ.get('SKYNAMO_GMAIL_PASSWORD')
	if sender is None or senderPassword is None:
		raise Exception('SKYNAMO_GMAIL_SENDER and SKYNAMO_GMAIL_PASSWORD environment variables must be set to send emails using Gmail credentials.')
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ','.join(recipients)
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))

	for file in files:
		if 'output/' != file[:7]:
			file = 'output/'+file
		with open(getPathRelativeToSkynamoDataFolder(file), "rb") as fil:
			part = MIMEApplication(
				fil.read(),
				Name=file.split('/')[-1]
			)
		# After the file is closed
		part['Content-Disposition'] = 'attachment; filename="%s"' % file.split('/')[-1]
		msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(sender, senderPassword)
	text = msg.as_string()
	server.sendmail(sender, recipients, text)
	server.quit()