"""

Upload a file to O365 sharepoint using Python.

Got code from here:

https://github.com/vgrem/Office365-REST-Python-Client/issues/40

"""

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.utilities.request_options import RequestOptions
from office365.sharepoint.file_creation_information import FileCreationInformation
import requests
import os
from os.path import basename

def upload_binary_file(file_path, base_url, folder_url, ctx_auth):
    """Attempt to upload a binary file to SharePoint"""

    file_name = basename(file_path)
    files_url ="{0}/_api/web/GetFolderByServerRelativeUrl('{1}')/Files/add(url='{2}', overwrite=true)"
    full_url = files_url.format(base_url, folder_url, file_name)

    options = RequestOptions(base_url)
    context = ClientContext(base_url, ctx_auth)
    context.request_form_digest()

    options.set_header('Accept', 'application/json; odata=verbose')
    options.set_header('Content-Type', 'application/octet-stream')
    options.set_header('Content-Length', str(os.path.getsize(file_path)))
    options.set_header('X-RequestDigest', context.contextWebInformation.form_digest_value)
    options.method = 'POST'

    with open(file_path, 'rb') as outfile:

        # instead of executing the query directly, we'll try to go around
        # and set the json data explicitly

        context.authenticate_request(options)
        
        data = requests.post(url=full_url, data=outfile, headers=options.headers, auth=options.auth)

        if data.status_code != 200:
            print("upload_binary_file error code: "+str(data.status_code))
            
def checkin_file(file_path, base_url, folder_url, ctx_auth):
    """Attempt to upload a binary file to SharePoint"""

    file_name = basename(file_path)
    files_url ="{0}/_api/web/GetFileByServerRelativeUrl('{1}/{2}')/CheckIn(comment='Comment',checkintype=0)"
    full_url = files_url.format(base_url, folder_url, file_name)

    options = RequestOptions(base_url)
    context = ClientContext(base_url, ctx_auth)
    context.request_form_digest()

    options.set_header('X-RequestDigest', context.contextWebInformation.form_digest_value)
    options.method = 'POST'

    context.authenticate_request(options)
        
    data = requests.post(url=full_url, headers=options.headers, auth=options.auth)

    if data.status_code != 200:
        print("checkin_file error code: "+str(data.status_code))
        
def upload_one_file(base_url,folder_url,file_name,user_name,pwd):
    ctx_auth = AuthenticationContext(url=base_url)
    if not ctx_auth.acquire_token_for_user(username=user_name, password=pwd):
        print(ctx_auth.get_last_error())
        exit()

    upload_binary_file(file_name, base_url, folder_url, ctx_auth)

    checkin_file(file_name, base_url, folder_url, ctx_auth)
        
if __name__ == '__main__':

    base_url = "https://mysite.sharepoint.com/sites/mypath/"
    folder_url = "/sites/mypath/Test"
    file_name = "C:\\temp\\out.txt"
    user_name = 'myuser@mysite.com'
    pwd = 'MyPassword'
    
    upload_one_file(base_url,folder_url,file_name,user_name,pwd)