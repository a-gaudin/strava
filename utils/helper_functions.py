from omegaconf import OmegaConf

def get_config():
    """ Get hydra config file """
    return OmegaConf.load('./conf/config.yaml')