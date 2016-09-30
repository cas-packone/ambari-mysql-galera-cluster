#coding=utf-8
import os
import base64
from time import sleep
from resource_management import *

class GrantTables(Script):

    @staticmethod
    def StartGrantTables():
        print 'start mysql for skip-grant-tables mode'
        Execute('nohup mysqld_safe --skip-grant-tables &')
        return True

