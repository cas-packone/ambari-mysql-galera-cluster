import os
import base64
from time import sleep
from resource_management import *

file_object = open("/root/.mysql_secret")
try:
    file_content = file_object.read()
    array = file_content.split(':')
    size = len(array)
    print array[size-1]
finally:
    file_object.close()