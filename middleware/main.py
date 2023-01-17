# Source: https://github.com/tiangolo/fastapi/issues/1788
# Source: https://stackoverflow.com/questions/70610266/proxy-an-external-website-using-python-fast-api-not-supporting-query-params # noqa
import os

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import StreamingResponse

MLFLOW_HOST = os.getenv('MLFLOW_HOST')
MLFLOW_PORT = os.getenv('MLFLOW_PORT')
MLFLOW_API_ACCESS_TOKEN = os.getenv('MLFLOW_API_ACCESS_TOKEN')

client = httpx.AsyncClient(
    base_url="http://{}:{}/".format(MLFLOW_HOST, MLFLOW_PORT)
)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def _forward_request(request: Request):
    url = httpx.URL(
        path=request.url.path,
        query=request.url.query.encode("utf-8")
    )
    rp_req = client.build_request(
        request.method,
        url,
        headers=request.headers.raw,
        content=await request.body()
    )
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )


@app.api_route("/api/{path:path}",
               methods=["GET", "HEAD", "POST", "PUT", "DELETE",
                        "CONNECT", "OPTIONS", "TRACE", "PATCH"])
async def reverse_proxy_auth(request: Request,
                             token: str = Depends(oauth2_scheme)):
    if token == MLFLOW_API_ACCESS_TOKEN:
        return await _forward_request(request)
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")


@app.api_route("/{path:path}",
               methods=["GET", "HEAD", "POST", "PUT", "DELETE",
                        "CONNECT", "OPTIONS", "TRACE", "PATCH"])
async def reverse_proxy(request: Request):
    return await _forward_request(request)
