import pkg_resources


path = pkg_resources.resource_filename("cr_obj_naming", "VERSION")
__version__ = open(path).read()
