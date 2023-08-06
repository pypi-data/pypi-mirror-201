import pkg_resources


path = pkg_resources.resource_filename("cnd_cr", "VERSION")
__version__ = open(path).read()
