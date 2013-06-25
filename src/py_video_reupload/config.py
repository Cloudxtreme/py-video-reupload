import sys
import os
import json

class pantheraConfig:
    """ Panthera Desktop Framework Configuration module """

    Config = dict()
    configTime = None # config last modification time
    app = None

    def __init__(self, file, create=False):
        self.file = os.path.expanduser(file)
        #self.app = app
        self.Config = dict()
        
        # allow or disallow creation of missing files or directories
        if create == True:
            # create directory if does not exists
            if not os.path.isdir(os.path.dirname(self.file)):
                os.mkdir(os.path.dirname(self.file))
                
            # create file if does not exists yet
            if not os.path.isfile(self.file):
                f = open(self.file, "w")
                f.write("")
                f.close()
        
        f = open(self.file, "r")
        self.Config = json.loads(f.read())
        f.close()

    def __str__(self):
        return str(self.Config)
        
    def __dict__(self):
        return self.Config

    def setKey(self, Option, Value):
        """ Set configuration key """

        self.Config[Option] = str(Value)
        return True


    def removeKey(self, Option):
        try:
            return self.Config.pop(Option)
        except KeyError:
            return False


    def getKey(self, Key, default=None):
        """ Returns configuration variable value

            Args:
              Key - variable name

            Returns:
              False - when value of variable is "false" or "False" or just False
              string value - value of variable
        """

        try:
            cfg = self.Config[Key]

            # returning int values instead of strings
            try:
                cfg = int(cfg)
            except ValueError:
                pass

            if str(cfg).lower() == "false":
                return False
            else:
                return cfg

        except KeyError:
            # if we specified default value, let it be saved to configuration file too
            if default != None:
                self.setKey(Key, default)
                self.save()
                return default

            return None


    def save(self):
        """ Save configuration to file """

        try:
            f = open(os.path.expanduser(self.file), "w")
            f.write(json.dumps(self.Config, sort_keys=True, indent=4, separators=(',', ': ')))
            f.close()
        except Exception:
            return False
            
        return True
