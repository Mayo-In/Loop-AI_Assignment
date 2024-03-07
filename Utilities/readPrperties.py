import configparser

config = configparser.RawConfigParser()
config.read(".\\Configurations\\config.ini")


class ReadConfig:
    @staticmethod
    def getAppURL():
        url = config.get('Common Data','url')
        return url

    @staticmethod
    def getUsername():
        username = config.get('Common Data', 'username')
        return username

    @staticmethod
    def getPassword():
        password = config.get('Common Data', 'password')
        return password
