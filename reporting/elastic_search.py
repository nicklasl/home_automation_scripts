import logging
import config
from datetime import datetime
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)
ELASTIC_SEARCH_NODE_URI = config.key("ELASTIC_SEARCH_URI")
es = Elasticsearch([ELASTIC_SEARCH_NODE_URI])


def log(pulses, k_w_h, verbose=False):
    timestamp = datetime.now()
    data = {'pulses': pulses, 'kwh': k_w_h, 'timestamp' : timestamp}
    if verbose:
        logger.debug("indexing:".format(data))

    es.index(index="electricity", doc_type="zapdos", body=data, timestamp=timestamp)

def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)