import base64
import pickle
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel

import numpy as np
from minio import Minio
from exodusutils.model_store import load_stuff_from_minio
from exodusutils.enums import TimeUnit

class TimeGroupInfo(BaseModel):
    """
    The ID for the model we trained for a time group value, along with the minimum target value in the time group value's dataframe, and the last date in the dataframe.

    Could contain an actual `LGBMRegressor` model.
    """

    model_id: str
    last_date: datetime
    min_target: Optional[float] = None
    model: Optional[Any] = None

    def load(self, minio: Minio):
        self.model = load_stuff_from_minio(self.model_id, minio)
        return self

    def get_last_date_for_prediction(self, time_unit: TimeUnit) -> np.datetime64:
        return np.datetime64(time_unit.format_datetime(self.last_date))

    def to_downloadable(self, minio: Minio) -> Dict[str, Any]:
        stuff = self.load(minio).dict(exclude={"model_id"})

        # FIXME dumping with pickle and then encoding with base64 is too much work.
        #       Use a better mechanism when time permits.
        stuff["model"] = base64.b64encode(pickle.dumps(stuff["model"]))

        return stuff

    class Config:
        arbitrary_types_allowed = True
