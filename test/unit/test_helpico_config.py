import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from helpico_config import HelpicoConfig


@pytest.fixture
def helpico_conf(**kwargs):
    defaults = {
        'rpcuser': 'helpicorpc',
        'rpcpassword': 'Helpicodsf4TR73627fuao3y7ts78o',
        'rpcport': 11000,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    helpico_config = helpico_conf()
    creds = HelpicoConfig.get_rpc_creds(helpico_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'helpicorpc'
    assert creds.get('password') == 'Helpicodsf4TR73627fuao3y7ts78o'
    assert creds.get('port') == 11000

    helpico_config = helpico_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = HelpicoConfig.get_rpc_creds(helpico_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'helpicorpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', helpico_conf(), re.M)
    creds = HelpicoConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'helpicorpc'
    assert creds.get('password') == 'Helpicodsf4TR73627fuao3y7ts78o'
    assert creds.get('port') == 12000


# ensure helpico network (mainnet, testnet) matches that specified in config
# requires running helpicod on whatever port specified...
#
# This is more of a helpicod/jsonrpc test than a config test...
