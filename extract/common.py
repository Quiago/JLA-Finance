import yaml

__config = None


def config():
    """sumary_line
    A function that return the config file for the css selectors while scraping

    Return: config.yaml file
    """
    
    global __config
    if not __config:
        with open('../extract/config.yaml', mode='r') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)


    return __config
