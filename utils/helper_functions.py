from omegaconf import OmegaConf
import pandas as pd
from pathlib import Path

def get_config():
    """ Get hydra config file """
    return OmegaConf.load('./conf/config.yaml')

def get_df_from_db(folder_path: str, file_name: str) -> pd.DataFrame:
    """ Get database as a dataframe """
    db_file_path = Path(folder_path) / file_name
    return pd.read_pickle(db_file_path)

def has_numbers(string_: str) -> bool:
    """ Check if string contains a digit character """
    return any(char.isdigit() for char in string_)

def first_number(string_: str) -> int:
    """ Get the first digit character of a string """
    return int(list(filter(str.isdigit, string_))[0])

def first_word(string_: str) -> str:
    """ Get the first word of a string """
    return string_.split()[0]

def two_first_words(string_: str) -> str:
    """ Get the two first words of a string """
    return ' '.join(string_.split()[:2])

