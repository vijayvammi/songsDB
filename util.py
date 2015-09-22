import re

def get_config(config_params):
    '''
    Reads the credentials file to extract application specific configuration
    parameters. 
    config_params is a list of params you seek
    returns a dictionary of the parameters you asked if they exist in 
    credentials
    Raises exception if one of the config_params is not found
    '''
    lines = open('credentials').readlines()
    return_params = {}
    for line in lines:
        if line.startswith('#'):
            continue
        if line.strip() == '':
            continue    
        data = re.compile('\s+').split(line.strip())
        if data[0] in config_params:
            return_params[data[0]] = data[1]
    if set(config_params) != set(return_params.keys()):
        # we did not find a key in the credentials. WARN!!!
        raise ValueError('I dont have some config params you asked for!!')        
    return return_params        