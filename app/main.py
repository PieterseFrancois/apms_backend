import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from mangum import Mangum
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.database import initialise_database
from app.routers import oven
from app.schemas import Response
from app.utils.http_messages import HTTPMessages

app = FastAPI()
handler = Mangum(app)

origins: list[str] = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:4200",
]


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
        content=Response(
            success=False,
            msg=HTTPMessages.VALIDATION_ERROR,
            data=[],
        ).model_dump(),
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
        content=Response(
            success=False,
            msg=message,
            data=[],
        ).model_dump(),
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
        content=Response(
            success=False,
            msg=HTTPMessages.DATA_INTEGRITY_ERROR,
            data=[],
        ).model_dump(),
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
        content=Response(
            success=False,
            msg=message,
            data=[],
        ).model_dump(),
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
        content=Response(
            success=False,
            msg=HTTPMessages.INTERNAL_SERVER_ERROR,
            data=[],
        ).model_dump(),
    )


app.include_router(oven.router)


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
    uvicorn.run(app, host="127.0.0.1", port=8000)
