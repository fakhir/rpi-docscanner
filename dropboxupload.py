#!/usr/bin/env python
#
# Upload any file to a Dropbox account. You'll first need to go to the following page
# and setup an Dropbox app (with App folder option):
# https://www.dropbox.com/developers/apps
#
# Then paste the app key and secret obtained from the above page to within this script
# below.
#

# Include the Dropbox SDK
import sys
import os
import json
import math
import dropbox

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'INSERT_APP_KEY'
APP_SECRET = 'INSERT_APP_SECRET'

CONFIG_FILE = '.dropboxupload'

def first_run():
    """Sets up authentication with Dropbox and returns the access code and user ID."""
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()
    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)
    return (access_token, user_id)

def file_upload(access_token, filename):
    """Uploads a file to dropbox from the current directory."""
    client = dropbox.client.DropboxClient(access_token)
    f = open(filename, 'rb')
    return client.put_file(os.path.basename(filename), f)

def file_download(access_token, filename):
    """Downloads a file from dropbox into the current directory."""
    client = dropbox.client.DropboxClient(access_token)

    f, metadata = client.get_file_and_metadata(filename)
    out = open(filename, 'wb')
    out.write(f.read())
    out.close()
    print metadata

def config_create(data):
    """Creates a config file containing data specified in the 'data' dictionary."""
    f = open(os.path.join(os.path.expanduser('~'), CONFIG_FILE), 'w')
    json.dump(data, f, sort_keys=True, indent=4)
    f.close()

def config_read():
    """Reads a config file and returns its data as a dictionary."""
    try:
        f = open(os.path.join(os.path.expanduser('~'), CONFIG_FILE), 'r')
        data = json.load(f)
        f.close()
    except:
        data = None
    return data

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print 'Syntax: %s <file-to-upload>' % sys.argv[0]
        sys.exit(1)
    try:
        conf = config_read()
        if not conf:
            access_token, user_id = first_run()
            conf = { 'access_token': access_token }
            config_create(conf)
        if len(sys.argv) == 2:
            response = file_upload(conf['access_token'], sys.argv[1])
            if response is not None:
                print 'Successfully uploaded: %s' % (response['path'])
            else:
                raise Exception('Error in upload operation')
    except Exception, e:
        print 'Failed to upload file (%s)' % str(e)
        sys.exit(1)
