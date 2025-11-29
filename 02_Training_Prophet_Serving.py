# Databricks notebook source
# MAGIC %md
# MAGIC # 📙 02 - Training & Serving (Prophet + MLflow)
# MAGIC Entraîne un modèle de prévision hebdomadaire par produit et enregistre via **MLflow**. Active ensuite **Model Serving** via l'UI Databricks.

# COMMAND ----------

# MAGIC %pip install prophet mlflow cloudpickle

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

import mlflow, mlflow.pyfunc
from prophet import Prophet
import pandas as pd
import cloudpickle, tempfile

# COMMAND ----------

jdbc_url = "jdbc:sqlserver://server-retail-dev.database.windows.net:1433;database=db-retail-dev;encrypt=true;trustServerCertificate=false"
connection_props = {
  "user": dbutils.secrets.get("kv-retail", "SQL-USER"),     
  "password": dbutils.secrets.get("kv-retail", "SQL-PASSWORD"),
  "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

df = (spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "dbo.vw_WeeklySalesByProduct").options(**connection_props).load())
display(df)

pdf = df.toPandas()
pdf = pdf.rename(columns={"WeekStart":"ds", "SalesAmount":"y"})
top_pid = pdf['ProductID'].value_counts().idxmax()
pdf_focus = pdf[pdf['ProductID']==top_pid].sort_values("ds")
display(pdf)

# COMMAND ----------

import mlflow
from mlflow.models import infer_signature
import pandas as pd
import tempfile, cloudpickle
from prophet import Prophet

mlflow.set_registry_uri("databricks-uc")
registered_name = "dbx_retail_dev_cc.mlops.retail_weekly_prophet"

# Données d'entraînement déjà prêtes dans pdf_focus[['ds','y']]
model = Prophet(interval_width=0.8)
model.fit(pdf_focus[['ds','y']])

# Exemple d'entrée/sortie pour la signature
example_input  = pd.DataFrame([{"horizon": 6}])
_example_future = model.make_future_dataframe(periods=6, freq='W')
_example_fc = model.predict(_example_future.tail(6))[["ds","yhat","yhat_lower","yhat_upper"]]
signature = infer_signature(example_input, _example_fc)

class ProphetWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        with open(context.artifacts["model_path"], "rb") as f:
            self.model = cloudpickle.load(f)

    # ✅ type hints ajoutés
    def predict(self, context, model_input: pd.DataFrame) -> pd.DataFrame:
        horizon = int(model_input.iloc[0].get('horizon', 6))
        future = self.model.make_future_dataframe(periods=horizon, freq='W')
        fc = self.model.predict(future.tail(horizon))
        return fc[['ds','yhat','yhat_lower','yhat_upper']]

tmp = tempfile.mkdtemp()
model_path = f"{tmp}/prophet.pkl"
with open(model_path, "wb") as f:
    cloudpickle.dump(model, f)

with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",                 # OK de garder (warning cosmétique)
        python_model=ProphetWrapper(),
        artifacts={"model_path": model_path},
        registered_model_name=registered_name, # <catalog>.<schema>.<name>
        signature=signature,                   # ✅ ajoute la signature
        input_example=example_input            # (optionnel mais utile)
    )

print("✅ Modèle enregistré dans UC ; prêt pour le Serving.")


# COMMAND ----------

import mlflow.pyfunc
model = mlflow.pyfunc.load_model("models:/dbx_retail_dev_cc.mlops.retail_weekly_prophet/1")
model.predict({"horizon": [8]})
