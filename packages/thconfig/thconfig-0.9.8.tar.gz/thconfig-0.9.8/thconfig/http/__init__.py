from .http_config import HTTPConfig
from .couch_config import CouchConfig

try:
    from .etcd_config import EtcdConfig
except Exception as e:
    print(f'Error: {e}')
