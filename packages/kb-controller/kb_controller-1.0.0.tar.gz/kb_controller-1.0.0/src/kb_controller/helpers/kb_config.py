import os
# from pathlib import Path
import configparser

script_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()

def save():
    with open('kbc-config.ini', 'w') as configfile:
        print("Gemmer konfigurationsfilen...")
        config.write(configfile)


# Intialize configuration values

try:
    with open('kbc-config.ini') as cfgFile:
        config.read_file(cfgFile)
except IOError:
    print()
    print('----------------------------------------------------------------')
    print("Ingen konfigurationsfil fundet - opretter en ny")
    defaultConfig = configparser.ConfigParser()
    with open(script_path + '/kbc-default-config.ini') as defaultCfgFile:
        defaultConfig.read_file(defaultCfgFile)
        config['GENERAL'] = defaultConfig['GENERAL']
        config['EMULATOR'] = defaultConfig['EMULATOR']
        config['MICROBIT'] = defaultConfig['MICROBIT']
        config['LOCALHOST'] = defaultConfig['LOCALHOST']
        config['PRODUCTION'] = defaultConfig['PRODUCTION']

    save()
    print("Afslutter programmet - tjek kbc-config.ini filen og start igen !")
    print('----------------------------------------------------------------')
    exit()

api_user='API_User'
pwd='Password'

def set_api_user(user, p):
    global api_user, pwd
    api_user = user
    pwd = p

is_production = config['GENERAL'].getboolean('is_production')
is_emulator = config['GENERAL'].getboolean('is_emulator')
poll_interval_in_seconds = config['GENERAL'].getint('polling_interval')
EMULATOR = config['EMULATOR']
MICROBIT = config['MICROBIT']
LOCALHOST = config['LOCALHOST']
PRODUCTION = config['PRODUCTION']

def get_tty_value(key):
    return EMULATOR[key] if is_emulator else MICROBIT[key]

def get_host_value(key):
    return LOCALHOST[key] if not is_production else PRODUCTION[key]

tty_name = get_tty_value('tty_name')
tty_rate = int(get_tty_value('tty_rate'))
tty_timeout = int(get_tty_value('tty_timeout'))
kbc_host = get_host_value('host')

print(f'  is_production        = {is_production}')
print(f'  is_emulator          = {is_emulator}')
print(f'  tty_name             = {tty_name}')
print(f'  tty_rate             = {tty_rate}')
print(f'  tty_timeout          = {tty_timeout}')
print(f'  kbc_host             = {kbc_host}')
print(f'  polling_interval (s) = {poll_interval_in_seconds}')