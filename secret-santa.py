from random import shuffle
import hashlib
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

shuffle(guests)  # Shuffle guest list and pair guests up
pairs = [(f, t) for f, t in zip(guests[::2], guests[1::2])]

# Write hashes to a YAML file for potential debug
with open(settings['pairs-file'], 'wt') as f:
    yaml.dump([{'from': a['hash'], 'to': b['hash']} for (a, b) in pairs], f)
