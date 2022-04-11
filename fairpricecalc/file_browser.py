from datetime import date, timedelta
import time
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from os import path
from date_utils import DateUtils

import os
import getpass
import tempfile
import glob as gl
import pandas as pd
import ssl


class FileBrowser():
    

    GLOBAL_VOLUME_URL = os.environ['ru.bystrobank.apps.stockvaluation.securitiesrefurl']
    GLOBAL_VOLUME_PATH = tempfile.gettempdir() + '/stockvaluation/' + getpass.getuser() \
                                                                    + '/volume.xhtml'
    BASE_FILE_NAME = '/moex_shares_'
    BASE_FILE_URL = 'https://mfd.ru/marketdata/endofday/5/'
    BASE_FILE_PATH = tempfile.gettempdir() + '/stockvaluation/' + getpass.getuser()
    #BASE_FILE_PATH = '/var/apps/stockvaluation'
    EMPTY_FILE = -1
    EMPTY_FILE_TTL = 3600 # one hour

    DAYS_DELTA = -45


    def __init__(self, date_str):
        date_utils = DateUtils()
        self.date_range = date_utils.date_range(date_str, self.DAYS_DELTA)
        
    def get_files(self):
        ''' 
        Returns a list of files in a date range 
        and a global volume file
        '''
        return self._get_volume_file(), self._get_exchange_files()
    
    def _get_exchange_files(self):
        ''' Returns a list with files '''
        files_list = []
        for date in self.date_range:

            file = self._browse_filesystem(
                path=self._create_filesystem_path(date))

            if file == self.EMPTY_FILE: # if file is is empty, just skip
                continue

            if file != None: 
                files_list.append(file)
                continue

            # if file doesn't exist in filesystem, browse internet
            file = self._browse_internet( \
                    url=self._create_internet_path(date), \
                    save_path=self._create_filesystem_path(date, \
                    with_ext=True))
            if file == self.EMPTY_FILE:
                open(self._create_filesystem_path(date, with_ext=True).replace('csv', 'empty'), 'a').close()
                continue

            files_list.append(file)
        return files_list

    def _get_volume_file(self):
        ''' Returns a global volume file'''
        #file = self._browse_filesystem(self.GLOBAL_VOLUME_PATH)
        #if file == None:
        file = self._browse_internet(self.GLOBAL_VOLUME_URL, self.GLOBAL_VOLUME_PATH)

        if file == None:
            raise NameError('Global volume file not found')

        return file
        
    def _browse_filesystem(self, path):
        ''' Returns file searched in filesystem '''

        # Glob returns string path in list
        files=gl.glob(path)
        if files == []:
            return None # return that file not found in filesystem
        filename=files[0]
        file_is_empty = filename.find('empty') > 0
        if file_is_empty:
            if time.time()-os.path.getmtime(filename) < self.EMPTY_FILE_TTL:
                #print('skip update=',filename,time.time()-os.path.getmtime(filename))
                return self.EMPTY_FILE # return an empty file marker
            else:
                os.remove(filename)
                return None # return that file not found in filesystem
        else:
            return filename # return a valid path
        
    def _browse_internet(self, url, save_path):
        ''' Returns file searched in internet '''
        
        self._check_work_dir_exist()
        try:    
            response = urlretrieve(url, save_path)
        except HTTPError as e:
            # If file not founded in the internet,
            # creating file with extension .empty to
            # stop request to file's URL
             if e.code != 404:
                 raise e
             else:
                return self.EMPTY_FILE # file not found, return empty marker 

        except URLError as e:
             raise NameError('HTTP error: ' + e.code)

        return save_path

    def _check_work_dir_exist(self):
        if not path.isdir(self.BASE_FILE_PATH):
            os.mkdir(tempfile.gettempdir() + '/stockvaluation/')
            os.mkdir(self.BASE_FILE_PATH)
    
    def _create_filesystem_path(self, date, with_ext=False):
        ''' 
        Returns filesystem path with date,
        like this: stockvaluation/moex_shares_2019_04_12.csv
        or this for empty files: stockvaluation/moex_shares_2019_04_12.*
        '''
        date_iso = date.strftime('%Y-%m-%d')

        if with_ext:
            path = self.BASE_FILE_PATH \
                 + self.BASE_FILE_NAME \
                 + date_iso.replace('-', '_') + '.csv'
        else:
            path = self.BASE_FILE_PATH \
                 + self.BASE_FILE_NAME \
                 + date_iso.replace('-', '_') + '.*'

        return path
    
    def _create_internet_path(self, date):
        ''' 
        Returns filesystem path with date,
        like this: https://mfd.ru/marketdata/endofday/5/moex_shares_2019_04_12.csv
        '''
        date_iso = date.strftime('%Y-%m-%d')
        return self.BASE_FILE_URL \
             + self.BASE_FILE_NAME \
             + date_iso.replace('-', '_') + '.csv'
