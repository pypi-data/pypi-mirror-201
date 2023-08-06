from fastapi_myhelper.pydantic.meta import ConfigMeta
from sqlmodel.main import SQLModelMetaclass


class SQLModelMetaConfig(ConfigMeta, SQLModelMetaclass):
    pass

