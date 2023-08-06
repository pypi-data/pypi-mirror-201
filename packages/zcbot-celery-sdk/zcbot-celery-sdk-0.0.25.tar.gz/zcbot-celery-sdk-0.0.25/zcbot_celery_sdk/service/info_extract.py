from typing import Dict

from .base import BaseService
from ..model.callback import Callback
from ..model.param import InfoPredictParam


class BrandNameModelExtractService(BaseService):

    def info_extract(self, task_params: InfoPredictParam = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='info_extract.bnm', task_params=task_params.dict(), callback=callback,
                                        **kwargs)
