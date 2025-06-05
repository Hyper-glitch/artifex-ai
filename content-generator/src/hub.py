"""Utility instances and factories for build, deployment & analysis"""

from ttk import (
    SourceRepository,
    TritonDeployer,
    TritonManager,
    TritonRepository,
)

from settings import settings

source = SourceRepository(
    url=settings.SOURCE_REPOSITORY_URL,
    access_key_id=settings.SOURCE_REPOSITORY_ACCESS_KEY_ID,
    secret_access_key=settings.SOURCE_REPOSITORY_SECRET_ACCESS_KEY,
    bucket=settings.SOURCE_REPOSITORY_BUCKET,
    prefix=settings.SOURCE_REPOSITORY_PREFIX,
)

repository = TritonRepository(
    url=settings.TRITON_REPOSITORY_URL,
    access_key_id=settings.TRITON_REPOSITORY_ACCESS_KEY_ID,
    secret_access_key=settings.TRITON_REPOSITORY_SECRET_ACCESS_KEY,
    bucket=settings.TRITON_REPOSITORY_BUCKET,
    prefix=settings.TRITON_REPOSITORY_PREFIX,
)

manager = TritonManager(url=settings.TRITON_CLIENT_URL)

deployer = TritonDeployer(
    repository=repository,
    manager=manager,
    reload_policy=settings.TRITON_REPOSITORY_RELOAD_POLICY,
)
