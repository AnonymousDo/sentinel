import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from helpicod import HelpicoDaemon
from helpico_config import HelpicoConfig


def test_helpicod():
    config_text = HelpicoConfig.slurp_config_file(config.helpico_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000073747eac038cbc757165dd9950b6dc47018c4113c6d7c213a2928605db5'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = HelpicoConfig.get_rpc_creds(config_text, network)
    helpicod = HelpicoDaemon(**creds)
    assert helpicod.rpc_command is not None

    assert hasattr(helpicod, 'rpc_connection')

    # Helpico testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = helpicod.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert helpicod.rpc_command('getblockhash', 0) == genesis_hash
