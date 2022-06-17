from omegaconf import OmegaConf

def get_config():
    """ Get hydra config file """
    return OmegaConf.load('./conf/config.yaml')

def has_numbers(string_):
    """ Check if string contains a digit character """
    return any(char.isdigit() for char in string_)

def first_number(string_):
    """ Get the first digit character of a string """
    return int(list(filter(str.isdigit, string_))[0])

def first_word(string_):
    """ Get the first word of a string """
    return string_.split()[0]

def two_first_words(string_):
    """ Get the two first words of a string """
    return ' '.join(string_.split()[:2])

