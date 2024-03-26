from fastapi import Request
from logs.apilogger import logger

async def log_middleware(request: Request, call_next):
    log_dict= {
        "url": request.url.path,
        "method": request.method,
    }
    logger.info(log_dict)

    response = await call_next(request)

    log_dict["response_code"] = response.status_code

    logger.info(log_dict)

    return response

