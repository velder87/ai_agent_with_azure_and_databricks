# Databricks notebook source
dbutils.secrets.listScopes()
dbutils.secrets.get(scope="kv-ai-agent-0001", key="openai-key")
print("✅ Secret récupéré avec succès (non affiché pour sécurité)")

# COMMAND ----------

jdbc_url = "jdbc:sqlserver://server-ai-0001.database.windows.net:1433;database=db_retail;encrypt=true;trustServerCertificate=false"
connection_props = {
  "user": dbutils.secrets.get("kv-ai-agent-0001", "SQLUSER"),     
  "password": dbutils.secrets.get("kv-ai-agent-0001", "SQLPASSWORD"),
  "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

df = (spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "dbo.vw_WeeklySalesByProduct").options(**connection_props).load())
display(df)