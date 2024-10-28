import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from mangum import Mangum
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.database import initialise_database
from app.routers import oven, machines
from app.utils.http_messages import HTTPMessages
from app.websocket import manager as WebSocketManager

app = FastAPI()
handler = Mangum(app)

origins: list[str] = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:4200",
]


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> None:
    """
    WebSocket endpoint for the application.

    Args:
        websocket (WebSocket): The WebSocket connection.
        client_id (str): The client identifier.

    """

    await WebSocketManager.connect(websocket, client_id)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        WebSocketManager.disconnect(client_id)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Exception handler for RequestValidationError.

    Args:
        request (Request): The request that caused the exception.
        exc (RequestValidationError): The RequestValidationError instance.

    Returns:
        JSONResponse: The JSON response containing the error details.

    """

    return JSONResponse(
        status_code=422,
        content=dict(
            success=False,
            msg=HTTPMessages.VALIDATION_ERROR,
            data=[],
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Exception handler for HTTPException.

    Args:
        request (Request): The request that caused the exception.
        exc (HTTPException): The HTTPException instance.

    Returns:
        JSONResponse: The JSON response containing the error details.

    """

    message: str = exc.detail.msg.value

    return JSONResponse(
        status_code=exc.status_code,
        content=dict(
            success=False,
            msg=message,
            data=[],
        ),
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """
    Exception handler for IntegrityError.

    Args:
        request (Request): The request that caused the exception.
        exc (IntegrityError): The IntegrityError instance.

    Returns:
        JSONResponse: The JSON response containing the error details.

    """

    return JSONResponse(
        status_code=400,
        content=dict(
            success=False,
            msg=HTTPMessages.DATA_INTEGRITY_ERROR,
            data=[],
        ),
    )


@app.exception_handler(NoResultFound)
async def no_result_found_handler(request: Request, exc: NoResultFound) -> JSONResponse:
    """
    Exception handler for NoResultFound.

    Args:
        request (Request): The request that caused the exception.
        exc (NoResultFound): The NoResultFound instance.

    Returns:
        JSONResponse: The JSON response containing the error details.

    """

    resource_type: str = "Resource"

    if "oven" in request.url.path:
        resource_type = "Oven"
    elif "mould" in request.url.path:
        resource_type = "Mould"

    message: str = f"{resource_type} not found."

    return JSONResponse(
        status_code=404,
        content=dict(
            success=False,
            msg=message,
            data=[],
        ),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Exception handler for general exceptions.

    Args:
        request (Request): The request that caused the exception.
        exc (Exception): The exception instance.

    Returns:
        JSONResponse: The JSON response containing the error details.

    """

    return JSONResponse(
        status_code=500,
        content=dict(
            success=False,
            msg=f"{exc}",
            # msg=HTTPMessages.INTERNAL_SERVER_ERROR,
            data=[],
        ),
    )


app.include_router(oven.router)
app.include_router(machines.router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """
    Root endpoint that redirects to the /docs endpoint.

    Returns:
        RedirectResponse: The redirect response.

    """

    return RedirectResponse(url="/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
initialise_database()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
