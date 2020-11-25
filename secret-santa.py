from jinja2 import Template
import smtplib
import hashlib
import random
import yaml

SETTINGS_LOCATION = 'settings.yml'

# Read settings file
with open(SETTINGS_LOCATION, 'rt') as f:
    settings = yaml.load(f, Loader=yaml.FullLoader)

# Read guest list
with open('guests.yml', 'rt') as f:
    guests = yaml.load(f, Loader=yaml.FullLoader)

for guest in guests:  # Create hashes for each guest
    guest['hash'] = hashlib.sha1(guest['email'].encode()).hexdigest()

random.shuffle(guests)  # Shuffle guest list and pair guests up
pairs = [(f, t) for f, t in zip(guests[::2], guests[1::2])]

# Write hashes to a YAML file for future debug
with open(settings['pairs-file'], 'wt') as f:
    yaml.dump([{'from': a['hash'], 'to': b['hash']} for (a, b) in pairs], f)

# Create connection to SMTP Server
server = smtplib.SMTP_SSL(settings['server'], 465)
server.login(settings['username'], settings['password'])

# Load body template from settings file
template = Template(settings['body'])

# Loop through pairs and send emails
for from_guest, to_guest in pairs:
    first = from_guest['name'].split(' ')[0]
    body = template.render(first=first,
                           name=to_guest['name'],
                           address=to_guest['address'])
    message = 'Subject: {}\n\n{}'.format(settings['subject'], body)
    server.sendmail('santa@mg.dea.gl', from_guest['email'], message)

server.quit()
