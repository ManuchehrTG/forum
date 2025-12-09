import logging
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, WARNING

logger = getLogger("root")
logger.setLevel(INFO)

handler = StreamHandler()

formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

getLogger("apscheduler").setLevel(WARNING)
getLogger("uvicorn").disabled = True
getLogger("uvicorn.access").disabled = True
getLogger("uvicorn.error").disabled = True
