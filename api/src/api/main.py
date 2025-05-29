"""Tmp app for running in the docker compose."""

import asyncio

import uvicorn
import uvloop
from logger import logger, set_up_logger
from settings import settings

from api.app import app


async def main() -> None:
    """Main entry point for the application setup and execution."""
    set_up_logger()
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            host=settings.APP_HOST,
            port=settings.APP_PORT,
            reload=settings.DEBUG,
        )
    )
    logger.info(f"Server is running on {settings.APP_HOST}:{settings.APP_PORT}")
    try:
        await server.serve()
    except Exception as exc:
        logger.exception(f"An error occurred while running the server: {exc}")


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main(), debug=settings.DEBUG)
