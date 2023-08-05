# we can not import model classes here because that would create a circular
# comparison which would not work in python2
# do not import all models into this module because that uses a lot of memory and stack frames
# if you need the ability to import all models from one package, import them with
# from aphos_openapi.models import ModelA, ModelB
