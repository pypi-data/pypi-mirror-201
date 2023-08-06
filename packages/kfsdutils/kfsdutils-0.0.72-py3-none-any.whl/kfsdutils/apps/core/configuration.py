import functools


class Configuration:
    def __init__(self, **kwargs):
        self.__rawSettings = {tuple(item['setting']): item for item in kwargs.pop('settings')}
        self.__reqKeyList = ["{}:{}".format(k, v) for (k, v) in kwargs.items()]
        self.__config = self.generateConfig()

    def getFinalConfig(self):
        return self.__config

    def findSetting(self, key):
        tupleKey = tuple(key)
        return {} if tupleKey not in self.__rawSettings else self.__rawSettings[tupleKey]

    def getAllSubsetKeys(self, findKey):
        return [x for x in self.__rawSettings.keys() if self.isSubset(findKey, x)]

    def isSubset(self, tuple1, tuple2):
        set1 = set(tuple1)
        set2 = set(tuple2)
        if set2.issubset(set1):
            return True

        return False

    def sortKeysByLength(self, keys):
        return sorted(keys, key=len, reverse=False)

    def generateConfig(self):
        childKeys = self.sortKeysByLength(self.getAllSubsetKeys(self.__reqKeyList))
        masterConfig = self.findSetting(["master"])
        for childkey in childKeys:
            masterConfig.update(self.findSetting(childkey))
            masterConfig.pop('setting')
        return masterConfig

    def getConfig(self, key):
        keys = key.split(".")
        value = functools.reduce(lambda d, key: (d.get(key) if isinstance(d, dict) else None) if d else None, keys,
                                 self.__config)
        if value is None:
            raise Exception('Config key:{} not found'.format(key))
        return value

    def getConfigWithDefault(self, key, default):
        try:
            return self.getConfig(key)
        except Exception:
            return default
