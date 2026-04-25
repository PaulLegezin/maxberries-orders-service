import logging

import pythonjsonlogger.jsonlogger as jsonlogger

logger = logging.getLogger("fastapi_elk")
logger.setLevel(logging.INFO)


logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


# logstash_host = os.getenv("LOGSTASH_HOST", "logstash")

# logstash_handler = AsynchronousLogstashHandler(
#     host=logstash_host,
#     port=12201,
#     database_path=None
# )
# logger.addHandler(logstash_handler)
