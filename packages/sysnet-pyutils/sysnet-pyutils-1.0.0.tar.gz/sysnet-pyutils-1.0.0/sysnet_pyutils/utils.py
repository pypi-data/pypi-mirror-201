import logging
import os
import secrets
import sys
import traceback
import uuid
from datetime import datetime, timedelta
# from pathlib import Path
from urllib.parse import quote

import dateutil.parser
import pytz
import yaml

from ident import generate_pid, check_pid, correct_pid, generate_id12

TZ = os.getenv('TZ', 'Europe/Prague')
DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s in %(module)s: %(message)s')
LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%d.%m.%Y %H:%M:%S')


class ConfigError(Exception):
    pass


class Singleton(type):
    """
    Třída Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigFlag(object, metaclass=Singleton):
    def __init__(self):
        self.started = True
        self.config = False
        logging.info('ConfigFlag constructor')


CF = ConfigFlag()


class Config(object, metaclass=Singleton):
    """
    Třída Config: správa konfigurace
    """

    def __init__(self, config_path=None, config_dict=None):
        if not CF.config:
            self.loaded = False
            if config_path in [None, '']:
                config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf', 'config.yml')
            self.config_path = config_path
            # Path(self.config_path).mkdir(parents=True, exist_ok=True)
            if config_dict is None:
                logging.warning('Input configuration is empty')
                self.config = {}
            self.config_input = config_dict
            self.init()
            CF.config = True
            logging.info('Config initialized')
        else:
            logging.info('Config is already initialized')

    def init(self):
        if os.path.isfile(self.config_path):
            with open(self.config_path, "r") as yamlfile:
                out = yaml.load(yamlfile, Loader=yaml.FullLoader)
            if bool(out):
                self.config = out
                self.loaded = True
                logging.info('Configuration loaded')
                return self
            self.loaded = False
        self.config = self.config_input
        self.store()
        self.loaded = True
        return self

    def store(self):
        with open(self.config_path, 'w') as yamlfile:
            yaml.dump(self.config, yamlfile)
        logging.info('Configuration stored')
        return True

    def delete_file(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
            return True
        else:
            logging.error('Configuration file does not exist')
            return False

    def replace(self, config_dict):
        self.delete_file()
        self.config = config_dict
        self.store()


def url_safe(url):
    """
    Upraví URL, aby beobsahovalo nepovolené znaky

    :param url: Vstupní URL
    :return: Upravené URL
    """
    return quote(url, safe='/:?=&')


def who_am_i():
    """
    Vrátí název funkce

    :return: název funkce, odkud je voláno
    """
    stack = traceback.extract_stack()
    file_name, code_line, func_name, text = stack[-2]
    return func_name


def unique_list(input_list):
    """
    Vyřadí opakující se položky ze seznamu

    :param input_list:   Vstupní seznam
    :return: Unikátní seznam
    """
    if not isinstance(input_list, list):
        return input_list
    out = []
    for x in input_list:
        if x not in out:
            out.append(x)
    return out


def api_keys_init(agenda='main', amount=4):
    """
    Vygeneruje klíče pro API

    :param agenda: Název agendy, pro kterou se klíče generují
    :param amount: Počet vygenerovaných klíčů
    :return: seznam vygenerovaných klíčů
    """
    out = []
    for i in range(amount):
        out.append(api_key_next('{} {}'.format(agenda, i + 1)))
    return out


def uuid_next(uuid_type=1):
    """
    Vygeneruje UUID

    :param uuid_type: Lze použít pouze typ 1 nebo 4
    :return: uuid
    """
    if uuid_type == 1:
        out = uuid.uuid1()
    else:
        out = uuid.uuid4()
    return out


def pid_next():
    """
    Vygeneruje korektní PID

    :return:    PID
    """
    return generate_pid()


def pid_check(pid):
    """
    Zkontroluje korektnost PID

    :param pid: Vstupní PID
    :return: True/False
    """
    return check_pid(pid)


def pid_correct(pid):
    """
    Opraví PID

    :param pid: Vstupní PID
    :return: Opravený PID
    """
    return correct_pid(pid)


def id12_next(three_char_prefix=None):
    """
    Vygeneruje korektní 12místný alfanumerický identifikátor s pevným prefixem

    :param three_char_prefix:   Tříznakový prefix identifikátoru
    :return:    12místný alfanumerický identifikátor
    """
    return generate_id12(three_char_prefix=three_char_prefix)


def api_key_next(name, length=16):
    """
    Vygeneruje slovník API key {<API Key>: <name>}

    :param name:    Název API klíče
    :param length:  Dělka API klíče
    :return:    Slovník {<API Key>: <name>}
    """
    out = {api_key_generate(length=length): name}
    return out


def api_key_generate(length: int):
    """
    vygeneruje API klíč

    :param length: Dělka API klíče
    :return: API Key
    """
    return secrets.token_urlsafe(length)


def iso_to_local_datetime(isodate):
    """
    ISO string datum do lokálního datetime

    :param isodate: Textové datum v ISO
    :return: lokální datetime
    """
    if isodate is None:
        return None
    local_tz = pytz.timezone(TZ)
    ts = dateutil.parser.parse(isodate)
    out = ts.astimezone(local_tz)
    return out


def convert_hex_to_int(id_hex):
    """
    KOnvertuje hex string na int

    :param id_hex:  Hexadecimální string
    :return: int
    """
    id_int = int(id_hex, base=16)
    return id_int


def increment_date(date_str=None, days=1):
    """
    Inkrementuje datum v textovém formátu ISO o daný počet dní

    :param date_str:    ISO datum v textovém formátu ISO
    :param days:        počet dní
    :return:        ISO datum v textovém formátu ISO
    """
    if date_str is None:
        return None
    if days is None:
        return date_str
    d = datetime.strptime(date_str, '%Y-%m-%d')
    out = d + timedelta(days=days)
    return out.date().isoformat()


def today():
    """
    Vrací ISO 8601 datum dnešního dne

    :return:    ISO 8601 datum dnešního dne
    """
    out = datetime.now()
    return out.date().isoformat()


def tomorrow():
    """
    Vrací ISO 8601 datum zítřejšího dne

    :return:    ISO 8601 datum
    """
    return increment_date(date_str=today(), days=1)


def cs_bool(value=None):
    """
    Vrátí českou textovou hodnotu 'ano'/'ne' pokud je bool(value) True/False

    :param value:  Obecný objekt
    :return:    'ano' or 'ne'
    """
    out = 'ne'
    if bool(value):
        out = 'ano'
    return out


def cron_to_dict(cron):
    """
    Konvertuje cron text do do slovníku

    :param cron: cron text (například '35 21 * * *')
    :return:    dict of cron
    """
    cron_list = cron.split(' ')
    if len(cron_list) != 5:
        return None
    out = {
        'minute': cron_list[0],
        'hour': cron_list[1],
        'day': cron_list[2],
        'month': cron_list[3],
        'day_of_week': cron_list[4]
    }
    return out


class Log(object, metaclass=Singleton):
    """
    Singleton pro logování v celé aplikaci, kde je použit
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler(sys.stdout)
        if DEBUG:
            self.logger.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
            handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        handler.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.propagate = False
        self.logger.info('LOG created')

    def set_ext_logger(self, ext_logger):
        """
        Nastaví externí logger (například z Djanga nebo Flask)

        :param ext_logger: Esterní logger
        :return:
        """
        if ext_logger is not None:
            self.logger = ext_logger
