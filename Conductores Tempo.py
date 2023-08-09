#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime as dt
from datetime import time
from datetime import timedelta
import pandas as pd
import numpy as np
import mygeotab


# In[2]:


api = mygeotab.API(username='usuario@rentingcolombia.com',password='xxxxx',database='transportempo')
api.authenticate()


# In[5]:


conductores = api.get("User")
conductores = pd.DataFrame(conductores)
conductores = conductores.loc[:,["employeeNo", "firstName", "lastName", "name", "isDriver","id"]]
conductores = conductores[(conductores["isDriver"]==True) & (conductores["id"]!="UnknownDriverId")]


# In[7]:


conductores.to_excel(r"C:\Users\jramos\OneDrive - Renting Colombia S.A\Escritorio\conductores.xlsx",index=False)

