import json
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import base64
from concurrent.futures import ThreadPoolExecutor
import urllib.parse as urlparse
import builtins




class WrongCredentialsError(Exception):
    """
    Exception raised for errors in case of wrong:
    : filerobot_token
    : filerobot_key

    Attributes:
        request -- input request 404
        message -- explanation of the error
    """
    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)



class FolderNotFoundError(Exception):
    """Exception raised for errors in case of wrong list folder.

        Attributes:
            request -- input request 404
            message -- explanation of the error
    """
    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)


class FileNotFoundError(Exception):
    """Exception raised for errors in case of not found file.

            Attributes:
                request -- input request 404
                message -- explanation of the error
        """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)


class UrlContentError(Exception):
    """Exception raised for errors in case of url doesn't contain Content-Lenght header

               Attributes:
                   request -- input request 400
                   message -- explanation of the error
    """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)

class FileNameExistError(Exception):
    """Exception raised for errors in case of trying to rename the file with the same name

                   Attributes:
                       request -- input request 409
                       message -- explanation of the error
        """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)

class FolderExistsError(Exception):
    """Exception raised for errors in case of trying to create folder that already exist.

                       Attributes:
                           request -- input request 403
                           message -- explanation of the error
    """

    def __int__(self, request, message):
        self.request = request
        self.message = message
        super().__init__(self.message)


class ParameterTypeError(Exception):
    """
    Exception raised for error in case of tying to parse the parameter in proper format

    """
    def __int__(self, message):
        self.message = message
        super().__init__(self.message)




class Filerobot:
    """
    The filerobot class provides all the functionality of the filerobot and all of it's APIs.
    The idea of the filerobot class is to be used in every scrips filerobot related providing the functionality
    of the filerobot in an easier way.

    filerobot class accepts
    - filerobot_token
    - filerobot_key

    filerobot class methods:
    > Files:
        - List files
        - Get file details
        - Upload file URLs
        - Upload file multipart
        - Pool upload
        - Rename file
        - Move file
        - Delete file

    > Folders:
        - Create folder
        - Get folder details
        - List & search folders
        - Rename folder
        - Move folder
        - Delete folder

    > Metadata:
        - Get metadata fields
        - Get metadata field value
    """
    path_ = ''
    limit_ = 1000
    offset_ = 0
    order_ = 'updated_at,asc'
    order_options_ = ['updated_at,asc',
                      'updated_at,desc',
                      'created_at,asc',
                      'created_at,desc', ]
    recursive_ = 0
    pool = None
    verbose = False

    def __init__(self, filerobot_token=None, filerobot_key=None):
        """
        CREDENTIALS
        :param filerobot_token: Token, provided by Scaleflex
        :param filerobot_key:   Key, provided by Scaleflex
        """
        if filerobot_token is not None:
            self.filerobot_token = filerobot_token
        if filerobot_key is not None:
            self.filerobot_key = filerobot_key
        self.status_code_auth = None

    def verbose_print(self, *args) -> None:
        """
        :param args: Accepts string args
        :return:     If verbose is True prints all strings in new line.
        """
        if self.verbose is True:
            builtins.print(*args, sep="\n")

    def get_credentials_from_file(self, file_path):
        """
        The method accepts json file path in format
        {
         "filerobot_token": <filerobot_token>,
         "filerobot_key": <filerobot_key>
        }
        :param file_path:  str => path
        :return: str
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except:
            raise FileNotFoundError("Can't open the credentials file. Wrong format or missing file")

        filerobot_token = data.get('filerobot_token')
        filerobot_key = data.get('filerobot_key')
        if filerobot_token is not None and filerobot_key is not None:
            self.filerobot_token = filerobot_token
            self.filerobot_key = filerobot_key
        else:
            raise ValueError('Filerobot token and/or filerobot key are missing!')

        return "OK"


    def generate_json_file_with_credentials(self, json_file_path:str):
        """
        This method generates file with credentials in format

        :param json_file_path:  str=> file_name
        :return:
        """
        # Data to be written
        dictionary = {
            "filerobot_token": self.filerobot_token,
            "filerobot_key": self.filerobot_key
        }

        # Serializing json
        json_object = json.dumps(dictionary, indent=4)

        # Writing to sample.json
        with open(json_file_path, "w") as outfile:
            outfile.write(json_object)




    def check_and_set_filerobot_credentials(self) -> str:
        """
        Check if filerobot credentials is correct:
        If filerobot credentials are right set status_code to 200 and
        :return: 'Credentials: OK' string

        else raise WrongCredentialsError
        """
        self.verbose_print("="*100,
                           'Check and set filerobot method!',
                           '-' * 100,
                           f'filerobot token: {self.filerobot_token}',
                           f'filerobot key: {self.filerobot_key}',
                           '-' * 100)

        self.verbose_print('Concat url for checking filerobot token and key.')
        # make request
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        headers = self.get_header()
        url_check = f'https://api.filerobot.com/{self.filerobot_token}/v4/meta/model/fields'
        self.verbose_print(f'URL for check credentials => {url_check}')
        response = session.get(url_check, headers=headers)

        if response.status_code != 200:
            self.verbose_print(f'Wrong filerobot key or token => response status code {response.status_code}',
                               f'Message => {response.text}',
                               "="*100)
            error_message = 'Wrong filerobot key or token'
            self.status_code_auth = response.status_code
            raise WrongCredentialsError(error_message)
        else:
            self.verbose_print(f'filerobot token and key => OK => status code {response.status_code}',
                               f'Response => {response.text}',
                               "="*100)
            self.status_code_auth = response.status_code
            return 'Credentials: OK'

    def get_header(self) -> dict:
        """
        The method creates the header using filerobot_key
        :return: dict in format
        {
            'X-filerobot-Key': {{ filerobot_key }},
            'Content-Type': 'application/json',
        }
        """
        headers = {
            'X-filerobot-Key': self.filerobot_key,
            'Content-Type': 'application/json',
        }
        self.verbose_print('-'*100,
                           f'Get header method',
                           f'Header => {headers}',
                           '-'*100)
        return headers

    def get_multipart_header(self) -> dict:
        """
        The method creates the header using filerobot_key
        :return: dict in format
        {
            'X-filerobot-Key': {{ filerobot_key }},
        }
        """
        headers = {
            'X-filerobot-Key': self.filerobot_key,
        }
        self.verbose_print('-'*100,
                           'Get multipart headers',
                           f'Headers => {headers}',
                           '-'*100,)
        return headers

    @staticmethod
    def validate_int(value: int) -> bool:
        """

        :param value:   value expect integer
        :return:        Bool
        """
        try:
            int(value)
            return True
        except (Exception,):
            return False


    def validate_order(self, order: str) -> bool:
        """
        Staticmethod for validation order parameter
        :param order: expect string and check if the sting is in order_options_ list form constants.py
        :return:
        """
        if order in self.order_options_:
            return True
        else:
            return False

    def validate_values(self,
                        path: str = None,
                        limit: int = None,
                        offset: int = None,
                        order: str = None,
                        recursive: int = None) -> tuple:
        """
        Validate values
        :param path:      str => File path
        :param limit:     int => if is None -> get value form constants.py
        :param offset:    int => if is None -> get value from constants.py
        :param order:     str => if is None -> get value from constants.py
                          Possible values:
                                        updated_at,asc ;
                                        updated_at,desc ;
                                        created_at,asc ;
                                        created_at,desc
        :param recursive: int => if is None -> get value from constants.py
        :return:
        """

        self.verbose_print('-'*100,
                           'Validate values => INPUT:',
                           f'path: {path}',
                           f"limit: {limit}",
                           f"offset: {offset}",
                           f"order: {order}",
                           f"recursive: {recursive}")
        # Validate limit
        if limit is None:
            limit = self.limit_
        res = self.validate_int(limit)
        if not res:
            raise ParameterTypeError("Wrong parameter type for limit => required integer!")
        # Validate offset
        if offset is None:
            offset = self.offset_
        res = self.validate_int(offset)
        if not res:
            raise ParameterTypeError("Wrong parameter type for offset => required integer!")
        # Validate recursive
        if recursive is None:
            recursive = self.recursive_
        res = self.validate_int(recursive)
        if not res:
            raise ParameterTypeError("Wrong parameter type for recursive => required integer!")
        # Validate order
        if order is None:
            order = self.order_
        res = self.validate_order(order)
        if not res:
            message = ', '.join(self.order_options_)
            raise ParameterTypeError(f"Wrong parameter type or value => Valid options: {message}")
        # Validate path
        if path is None:
            path = self.path_

        self.verbose_print('-' * 100,
                           'Validate values => OUTPUT:',
                           f'path: {path}',
                           f"limit: {limit}",
                           f"offset: {offset}",
                           f"order: {order}",
                           f"recursive: {recursive}")

        return path, str(limit), str(offset), str(order), str(recursive)

    # FILES
    def inspect_file(self, uuid: str) -> dict:
        """
        Inspect file method make request and get details about asset with provided uuid
        :param uuid:   str
        :return:       dict
        """
        self.verbose_print('='*100,
                           'Start inspect_file method')
        headers = self.get_header()
        req_url = f'https://api.filerobot.com/{self.filerobot_token}/v4/files/{uuid}'
        response = requests.get(req_url,
                                headers=headers)
        self.verbose_print(f'Request url => {req_url}',
                           f'Response status code = > {response.status_code}',
                           "="*100)
        if response.status_code == 404:
            raise FileNotFoundError(f'File with uuid: {uuid} not found!')

        return response.json()

    def list_files(self, path: str = None,
                   limit: int = None,
                   offset: int = None,
                   order: str = None,
                   recursive: int = None) -> dict:
        """
        List_file method make list
        :param path:          folder path or folder name
        :param limit:         int      => Default value if not provided -> limit variable in constants.py
        :param offset:        int      => Default value if not provided -> offset variable in constants.py
        :param order:         str      => Default value if not provided -> order variable in constants.py
                                          Possible options  'updated_at,asc',
                                                            'updated_at,desc',
                                                            'created_at,asc',
                                                            'created_at,desc',
        :param recursive:    int       => Default value if not provided -> recursive variable in constants.py
        :return:            dict       => Response
        """
        self.verbose_print('=' * 100,
                           'Start list_file method')
        path, limit, offset, order, recursive = self.validate_values(path,
                                                                     limit,
                                                                     offset,
                                                                     order,
                                                                     recursive)
        headers = self.get_header()
        url_req = f'https://api.filerobot.com/{self.filerobot_token}' \
                  f'/v4/files?folder=/{path}&recursive={recursive}&limit={limit}&offset={offset}&order={order}'
        response = requests.get(url_req, headers=headers)
        if response.status_code == 404:
            raise FolderNotFoundError(f"Folder {path} not found!")
        self.verbose_print(f'Request url => {url_req}',
                           f'Response status => {response.status_code}',
                           '='*100)
        return response.json()

    def upload_file_multipart(self, file_path: str,
                              upload_filerobot_folder: str = None,
                              name_file: str = None,
                              metadata: dict = None,
                              pool_upload=False) -> dict:
        """
        upload_file_multipart method uploads multipart file
        :param file_path:                   str  => local file path
        :param upload_filerobot_folder:     str  => the name or path of folder in filerobot where to upload file
                                                    Optional => Default root filerobot folder
        :param name_file:                   str  => the name of the file in filerobot
                                                    Optional => Default name is the name of the local file
        :param metadata:                    dict => dict with metadata in proper format depends on metadata structure
                                                    Optional => Default value is empty dict
        :param pool_upload                  bool => If the method is calling from pool method  or not (Default=False)
        :return:                            dict => Response
        """
        self.verbose_print('Start multipart upload!', '-'*100, f'File to upload: {file_path}', '-'*100)
        if upload_filerobot_folder is None:
            upload_filerobot_folder = ''

        files = {}
        if type(file_path) != list:
            file_path = [file_path]

        counter_ = 1
        for file_path in file_path:
            if file_path:
                try:
                    curr_file = open(file_path, 'rb')
                except:
                    if pool_upload:
                        return {'file_path': file_path,
                        'Error': 'File not found!',
                        }
                    raise FileNotFoundError(f'Wrong file path => "{file_path}"')
                file_name = os.path.basename(file_path)

                # file_name = file_name.split('.')[0]

                files[f'{file_name}'] = curr_file
                if metadata is not None:
                    curr_meta_json = json.dumps(metadata).encode('utf-8')
                    files[f'{file_name}'] = curr_file
                    files[f'meta[{file_name}]'] = (None, curr_meta_json)

                counter_ += 1

        headers = self.get_multipart_header()
        url_upload = f"https://api.filerobot.com/{self.filerobot_token}/v4/upload?folder=/{upload_filerobot_folder}"
        self.verbose_print(f'Request url : {url_upload}')
        response = requests.post(url_upload, files=files, headers=headers)
        if response.status_code == 200 and name_file is not None:
            res = json.loads(response.text)
            uuid = res['file']['uuid']
            res_ = 0
            counter = 0
            while True:
                if res_ == 200 or counter > 3:
                    break
                res_ = self.rename_file(uuid, name_file)
                counter += 1

            self.verbose_print(f'Successfully uploaded => UUID {uuid} with name {name_file}',
                               '='*100)
        else:
            return {'file_path': file_path,
                    'Error': 'The requested file not uploaded!',
                    'response': response.json()}

        return response.json()

    def upload_url(self, url_: str,
                   upload_filerobot_folder: str = None,
                   name_file: str = None,
                   metadata: dict = None,
                   pool_upload=False) -> dict:
        """
        upload_url method uploads asset from URLs
        :param url_:                      str  =>  Asset url
        :param upload_filerobot_folder:   str  =>  the name or path of folder in filerobot where to upload file
                                                   Optional => Default root filerobot folder.
        :param name_file:                 str  =>  the name of the file in filerobot
                                                   Optional => Default name is the name of the local file
        :param metadata:                  str  =>  dict with metadata in proper format depends on metadata structure
                                                   Optional => Default value is empty dict
        :param pool_upload                  bool => If the method is calling from pool method  or not (Default=False)
        :return:                          dict =>  Response
        """
        self.verbose_print('Start URL upload!', '-' * 100, f'File to upload: {url_}', '-' * 100)
        up_ = {}
        if upload_filerobot_folder is None:
            upload_filerobot_folder = ''
        if name_file is None:
            file = {'url': url_}
        else:
            file = {'url': url_, 'name': name_file}

        if metadata is not None:
            file['meta'] = metadata

        if upload_filerobot_folder is None:
            upload_filerobot_folder = ''

        headers = self.get_header()
        res = [file]
        up_['files_urls'] = res
        req_url = f"https://api.filerobot.com/{self.filerobot_token}/v4/upload?folder=/{upload_filerobot_folder}"
        response = requests.post(req_url, json=up_, headers=headers)
        self.verbose_print(f'Requested url => {req_url}',
                           f'Response status code => {response.status_code}',
                           '='*100)
        if response.status_code == 400:
            if pool_upload:
                return {'url': url_,
                        'Error': 'The requested url is not valid and return status code 400',
                        'response': response.json()}
            raise UrlContentError(f'Wrong Url = "{req_url}" => Requested URL doesn not contain Content-Lenght header')
        return response.json()

    def rename_file(self, uuid: str, name_file: str) -> int:
        """
        rename_file method accepts target file uuid and rename it with provided name
        :param uuid:          str => target file uuid
        :param name_file:     str => new name of the file
        :return:              int => Status code
        """
        self.verbose_print("Rename method",
                           f"uuid: {uuid} file change name =>'{name_file}'",
                           "-"*100)
        d = {'name': name_file}
        headers = {
            'X-filerobot-Key': self.filerobot_key,
            'Content-Type': 'application/json',

        }
        response = requests.patch(
            f"https://api.filerobot.com/{self.filerobot_token}/v4/files/{uuid}",
            json=d, headers=headers)
        if response.status_code == 409:
            raise FileNameExistError(f'The name "{name_file}" already exists!')

        return response.status_code

    # TODO Need to be discussed with Simeon
    def upload_base_64(self, file_path: str = None,
                       upload_filerobot_folder: str = None,
                       name_file: str = None, ):
        if name_file is None:
            name_file = ''
        if upload_filerobot_folder is None:
            upload_filerobot_folder = ''

        if file_path is not None:
            with open(file_path, "rb") as file:
                encoded_string = base64.b64encode(file.read())

            f = {"postactions": "decode_base64", 'data': encoded_string, "name": name_file}

            headers = {
                'X-filerobot-Key': self.filerobot_key,
                # 'Content-Type': 'application/json',

            }
            response = requests.post(
                f"https://api.filerobot.com/{self.filerobot_token}/v4/upload?folder=/{upload_filerobot_folder}",
                files=f, headers=headers)
            return response.status_code

    def delete_file(self, uuid: str) -> dict:
        """
        delete_file method is method that delete file with provided uuid
        :param uuid:  str  => uuid of file
        :return:      dict => Response
        """
        self.verbose_print('='*100,
                           'Start delete file method',
                           f'Delete file with uuid => {uuid}',
                           '-'*100)
        headers = self.get_header()
        response = requests.delete(f'https://api.filerobot.com/{self.filerobot_token}/v4/files/{uuid}', headers=headers)
        if response.status_code == 404:
            raise FileNotFoundError(f'Wrong file uuid => {uuid}')
        return response.json()

    def download_file(self, uuid: str, path: str) -> str:
        """
        download_file method downloads file with uuid in provided local path
        :param uuid:   str  => uuid of file
        :param path:   str  => local path where to store downloaded asset
        :return:       str => Successful message
        """
        headers = self.get_header()
        response = requests.get(f'https://api.filerobot.com/{self.filerobot_token}/v4/get/{uuid}/download',
                                headers=headers)

        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
        return f'Download file {path} with uuid: {uuid} successful!'

    def move_file(self, file_uuid: str, destination_folder_uuid: str) -> dict:
        """
        move_file method move file to folder
        :param file_uuid:                 str  => uuid of file (The file which want to move)
        :param destination_folder_uuid:   str  => uuid of the folder where want to move the file
        :return:                          dict => Response
        """
        self.verbose_print('='*100,
                           f'Start method move_file!',
                           f"file_uuid {file_uuid} => destination_folder => {destination_folder_uuid}",
                           "-"*100)
        headers = self.get_header()
        response = requests.put(
            f'https://api.filerobot.com/{self.filerobot_token}/v4/files/{file_uuid}/folders/{destination_folder_uuid}',
            headers=headers)
        if response.status_code == 404:
            raise FileNotFoundError('ROUTE_NOT_FOUND, Please check file uuid or destination folder uuid!')
        return response.json()

    # Folders
    def list_folder(self,
                    path: str = None,
                    limit: int = None,
                    offset: int = None,
                    order: str = None,
                    recursive: int = None) -> dict:
        """
        list_folder method get list of all files and folders
        :param path:          str
        :param limit:         int      => Default value if not provided -> limit variable in constants.py
        :param offset:        int      => Default value if not provided -> offset variable in constants.py
        :param order:         str      => Default value if not provided -> order variable in constants.py
                                          Possible options  'updated_at,asc',
                                                            'updated_at,desc',
                                                            'created_at,asc',
                                                            'created_at,desc',
        :param recursive:    int       => Default value if not provided -> recursive variable in constants.py
        :return:             dict      => Response
        """
        self.verbose_print('='*100,
                           'Start list_folder method => ',)
        path, limit, offset, order, recursive = self.validate_values(path, limit, offset, order, recursive)
        headers = self.get_header()

        response = requests.get(
            f'https://api.filerobot.com/{self.filerobot_token}/v4/folders?folder=/{path}&recursive={str(recursive)}'
            f'&limit={str(limit)}&offset={str(offset)}&order={order}',
            headers=headers,
        )
        if response.status_code == 404:
            raise FolderNotFoundError(f'The specified directory "{path}" does not exist.')

        return response.json()

    def create_folder(self, path: str) -> dict:
        """
        create_folder method creates folder
        :param path:    str  => folder name or path
        :return:        dict => Response
        """
        self.verbose_print('='*100,
                           'Start create_folder method',
                           f'Create folder: "{path}"')
        headers = self.get_header()
        json_data = {
            'name': path,
        }

        response = requests.post(f'https://api.filerobot.com/{self.filerobot_token}/v4/folders',
                                 headers=headers,
                                 json=json_data)
        if response.status_code == 403:
            raise FolderExistsError(f'Folder ="{path}" already exists. '
                                    f'If you do not see it it might indicate that you do not have the '
                                    f'necessary permissions')
        return response.json()

    # TODO Need to be discussed with Simeon
    def get_sass_key(self):
        headers = {
            'X-filerobot-Key': self.filerobot_key,
            'Content-Type': 'application/json',
        }

        response = requests.get(f'https://api.filerobot.com/{self.filerobot_token}'
                                f'/v4/key/{{security_template_identifier}}',
                                headers=headers)
        return response.json()

    # pool methods
    def add_to_pool(self, *args) -> str:
        """
        add_to_pool method accepts dict or list of dicts
        :param args:  dict or list of dicts => Accepting dict format:
                                            {'file_path': {{ file_path }}, # url or multipart
                                             'file_name': {{ name file in filerobot }},
                                             'upload_folder':{{ name folder in filerobot }},
                                             'metadata': {} # dict with proper format according to metadata structure
                                             }
        :return:                        str => Success message
        """
        if self.pool is None:
            self.pool = list(args)
        else:
            self.pool.extend(list(args))

        return "Successfully added!"

    def start_pool_upload(self) -> list[dict]:
        """
        start_pool_upload method starts threading pool upload
        :return:   list[dicts] => list with all responses after uploading the pool
        """
        self.verbose_print("="*100,
                           "Start start_pool_upload method",
                           '-'*100)
        # self.upload_pool(self.pool[0])
        executor = ThreadPoolExecutor()
        result = executor.map(self.upload_pool, self.pool)
        finals = []
        for value in result:
            finals.append(value)

        print('>'*100)
        # Sort result
        final_res = sorted(finals, key=lambda k: ("Error" not in k, k.get("Error", None)))
        return final_res

    def upload_pool(self, file: dict) -> dict:
        """
        upload_pool method is threading upload method. All files in pool start uploading in paralel
        :param file:                dict =>  {'file_path': {{ file_path }}, # url or multipart
                                             'file_name': {{ name file in filerobot }},
                                             'upload_folder':{{ name folder in filerobot }},
                                             'metadata': {} # dict with proper format according to metadata structure
                                             }
        :return:                   dict => Response
        """
        # Get data
        file_ = file.get('file_path')

        name_ = file.get('file_name')
        upload_folder_ = file.get('upload_folder')

        # Validate data
        is_url_ = urlparse.urlparse(file_).scheme != ""
        is_file_ = os.path.isfile(file_)

        metadata = file.get('metadata')
        res = {
            'file': file_,
            'Error': 'The path is not url or multipart file!'
        }
        if is_url_:
            print(f'Start uploading url file => {file_}')
            res = self.upload_url(file_,
                                  upload_filerobot_folder=upload_folder_,
                                  name_file=name_,
                                  metadata=metadata,
                                  pool_upload=True)
            print(f'Response => {file_} =>> completed')
        elif is_file_:
            print(f'Start uploading multipart file => {file_}')
            res = self.upload_file_multipart(file_, upload_filerobot_folder=upload_folder_,
                                             name_file=name_,
                                             metadata=metadata,
                                             pool_upload=True)
            print(f'Response => {file_} =>> completed')
        return res

    def get_metadata_field(self) -> list:
        """
        get_metadata_field method gets metadata structure
        :return:   list => List with all fields from the response
        """
        self.verbose_print("="*100,
                           "Start get_metadata_field",
                           "-"*100)
        headers = self.get_header()
        response = requests.get(f'https://api.filerobot.com/{self.filerobot_token}/v4/meta/model/fields',
                                headers=headers)
        res_data = json.loads(response.text)
        fields = res_data.get('fields')
        if fields is None:
            # TODO return error
            print('Error in filerobot request metadada structure fields')
        else:
            return fields

    def get_metadata_field_values(self, uuid: str) -> list:
        """
        get_metadata_field_values method get information for specific field uuid
        :param uuid:    str => field uuid (Get fields uuid from get_metadata_field method)
        :return:       list => list of dicts with details
        """
        self.verbose_print("="*100,
                           "Start get_metadata_field_values",
                           "-"*100)
        headers = self.get_header()
        response = requests.get(
            f'https://api.filerobot.com/{self.filerobot_token}/v4/meta/model/fields/{uuid}/options',
            headers=headers,
        )
        res_data = json.loads(response.text)
        fields_values = res_data.get('options')
        return fields_values

    def inspect_folder(self, uuid: str) -> dict:
        """
        inspect_folder method accsepts uuid of folder and return details about this folder
        :param uuid:   str  => uuid of the folder
        :return:       dict => Response
        """
        self.verbose_print("="*100,
                           f"Start inspect_folder method for uuid => {uuid}")
        headers = self.get_header()
        response = requests.get(
            f'https://api.filerobot.com/{self.filerobot_token}/v4/folders/{uuid}',
            headers=headers)
        if response.status_code == 404:
            raise FolderNotFoundError(f'Folder is not found! => uuid: {uuid}')
        return response.json()

    def move_folder(self, folder_uuid: str, dest_folder_uuid: str) -> dict:
        """
        move_folder method accsepts target and destination folder uuid and move target folder in to destination folder
        :param folder_uuid:         str  => target folder uuid
        :param dest_folder_uuid:    str  => destination folder uuid
        :return:                    dict => Response
        """
        self.verbose_print('='*100,
                           'Start move_folder method',
                           f'folder_uuid: {folder_uuid} to destination folder_uuid=> {dest_folder_uuid}')
        headers = self.get_header()
        response = requests.put(
            f'https://api.filerobot.com/{self.filerobot_token}/v4/folders/{folder_uuid}/folders/{dest_folder_uuid}',
            headers=headers,
        )
        if response.status_code == 404:
            raise FolderNotFoundError(f'Path not found. Folder uuid or destination folder is not correct')
        return response.json()

    def rename_folder(self, uuid_folder: str, new_name: str) -> dict:
        """
        rename_folder method accepts target folder uuid and name. Rename the target folder with the new name
        :param uuid_folder:   str  => targer folder uuid
        :param new_name:      str  => new name of the folder
        :return:              dict => Response
        """
        self.verbose_print('='*100,
                           'Start rename_folder method',
                           f'Rename folder with uuid : {uuid_folder} => New name = {new_name}')
        headers = self.get_header()
        json_data = {
            'name': new_name
        }
        # json_data = json.dumps(json_data, cls=SetEncoder)

        response = requests.patch(f'https://api.filerobot.com/{self.filerobot_token}/v4/folders/{uuid_folder}',
                                  headers=headers,
                                  json=json_data)
        if response.status_code == 400:
            raise FolderExistsError(f'Folder with name "{new_name}" already exists.')
        elif response.status_code == 404:
            raise FolderNotFoundError(f"Folder uuid {uuid_folder} is wrong!")
        return response.json()

    def delete_folder(self, uuid_folder: str) -> dict:
        """
        delete_folder method accepts uuid of the folder and delete it
        :param uuid_folder:   str  => Target folder uuid
        :return:              dict => Response
        """
        self.verbose_print('='*100,
                           "Start delete_folder method",
                           f'Delete folder with uuid {uuid_folder}')
        headers = self.get_header()
        response = requests.delete(f'https://api.filerobot.com/{self.filerobot_token}/v4/folders/{uuid_folder}',
                                   headers=headers)

        if response.status_code == 404:
            raise FolderNotFoundError(f"Wrong folder uuid => {uuid_folder}")
        return response.json()
