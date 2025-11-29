# ai_agent_with_azure_and_databricks

  ### 1. Create a ressource group in Azure 
        Region : WEST US 2

  ### 2. Add ressource Azure SQL 
        SQL and Windows Authentication
        user : sql_admin
        pass : XXXXXXXXXXXXX
  
      - Create Database : instnwnd (Azure SQL Database).sql
      - Run script : store_proc_and_views.sql
      - Test script in cloud or in Azure studio : 
            - SELECT * FROM vw_TopProducts_8w 

  ### 3. Add Key Vault pour permettre à SQL Server de communiquer avec Databricks

  ### 4. Add Databricks and test if we get access to SQL SERVER

  ### 5. Add OpenAI Services From Azure 
        Services : Azure OpenAI
        Modele : gpt-4o-mini
        Quota : check quota before deployment

        In deployment section, we'll get Endpoint URL : https://ai-openai-0001.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview
        and Key : Dhlpq4dttd0TSZ6i7uXJIXE7i376cPfwE9ySnjUKVuv9hYVNyKlU

  ### 6. Test OpenAI API with Postman

        {
         "messages": [
              {
                  "role": "user",
                  "content": "Le point le plus profond de la mer?"
              }
         ],
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 800,
        "stop": null
      }




