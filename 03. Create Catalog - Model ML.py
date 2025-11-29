# Databricks notebook source
# MAGIC %sql
# MAGIC -- Qui suis-je ?
# MAGIC SELECT current_user();
# MAGIC
# MAGIC -- Quel catalog/schema actifs ?
# MAGIC SELECT current_catalog(), current_schema();

# COMMAND ----------

# MAGIC %sql
# MAGIC -- (admin) créer un schema pour les modèles
# MAGIC CREATE SCHEMA IF NOT EXISTS dbx_retail_dev_cc.mlops;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- donner l’accès au catalog
# MAGIC GRANT USE CATALOG ON CATALOG dbx_retail_dev_cc TO `account users`;  -- ou à ton user / groupe
# MAGIC
# MAGIC -- donner l’accès et le droit de créer dans le schema
# MAGIC GRANT USE SCHEMA, CREATE ON SCHEMA dbx_retail_dev_cc.mlops TO `account users`; 
# MAGIC -- (tu peux remplacer `account users` par ton email AAD ou un groupe)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- donner l’accès au catalog
# MAGIC GRANT USE CATALOG ON CATALOG dbx_retail_dev_cc TO `account users`;  -- ou à ton user / groupe
# MAGIC
# MAGIC -- donner l’accès et le droit de créer dans le schema
# MAGIC GRANT USE SCHEMA, CREATE ON SCHEMA dbx_retail_dev_cc.mlops TO `account users`; 
# MAGIC -- (tu peux remplacer `account users` par ton email AAD ou un groupe)