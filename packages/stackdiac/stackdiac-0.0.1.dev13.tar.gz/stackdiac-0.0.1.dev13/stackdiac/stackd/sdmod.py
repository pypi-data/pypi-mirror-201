# stackd instance


from stackdiac.api import app as api_app
from .stackd import Stackd
sd = Stackd()

@api_app.get("/sd")
async def get_sd() -> Stackd:
    s = Stackd()
    s.configure()
    return s

import logging

logger = logging.getLogger(__name__)

