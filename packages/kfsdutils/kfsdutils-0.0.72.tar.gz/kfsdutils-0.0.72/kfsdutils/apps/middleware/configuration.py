from django.conf import settings
from kfsdutils.apps.core.utils import DictUtils
from kfsdutils.apps.core.configuration import Configuration

import os


class KubefacetsConfigMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.__config = self.genConfig()

    def __call__(self, request):
        request.config = self.__config
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def getEnv(self, envKey):
        return os.getenv(envKey)

    def constructDimensionsFromEnv(self, dimensionKeys):
        return {key: self.getEnv(key) for key in dimensionKeys}

    def genLocalConfig(self, dimensionKeys, config):
        dimensions = self.constructDimensionsFromEnv(dimensionKeys)
        return Configuration(settings=config, **dimensions)

    def deriveConfig(self):
        kubefacetsSettings = settings.KUBEFACETS
        isLocalConfig = DictUtils.getValueFromKeyPath("config.is_local_config", kubefacetsSettings)
        lookupDimensions = DictUtils.getValueFromKeyPath("config.lookup_dimension_keys", kubefacetsSettings)
        if isLocalConfig:
            localConfig = DictUtils.getValueFromKeyPath("config.local", kubefacetsSettings)
            return self.genLocalConfig(lookupDimensions, localConfig)
        return None

    def genConfig(self):
        return self.deriveConfig()
