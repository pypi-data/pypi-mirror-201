# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import mlflow


class PyfuncModel(mlflow.pyfunc.PythonModel):
    def __init__(self, my_model):
        self._model = my_model
