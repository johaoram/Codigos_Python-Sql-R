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


## ingreso api
api = mygeotab.API(username='usuario@empresa.com',password='xxxxx',database='transportempo')
api.authenticate()


# In[50]:


# se agrega +5 horas, porque la hora del servidor es GMT -5
inicio = "2023-01-01 05:00:00"
final = "2023-08-01 05:00:00"


# In[51]:


viajes = api.get("Trip",
                        search = {
                            'fromDate':inicio, 'toDate':final})


# In[52]:


viajes = pd.DataFrame(viajes)
viajes = viajes[["start", "device", "driver"]]


# In[56]:


viajes['mes'] = viajes['start'].dt.month


# In[58]:


## función para extraer los diccionarios
def key_func(x,key):
    try:
        return(x[key])
    except:
        return(x)


# In[59]:


viajes.driver = viajes.driver.apply(lambda x:key_func(x,"id"))


# In[60]:


viajes.device = viajes.device.apply(lambda x:key_func(x,"id"))


# In[61]:


viajes


# In[82]:


dias = viajes.groupby(["driver","mes"])["start"].apply(lambda x: x.dt.date.nunique()).reset_index()


# In[96]:


conductores = api.get("User")
conductores = pd.DataFrame(conductores)


# In[97]:


conductores = conductores[["employeeNo", "firstName", "lastName", "name", "isDriver","id"]]


# In[98]:


conductores = conductores[conductores["isDriver"]==True]


# In[101]:


dias_trabajados = dias.merge(conductores, left_on="driver",right_on="id", how="left")


# In[102]:


dias_trabajados[["name","employeeNo","start","mes"]]


# In[83]:


dias.to_excel("C:\Users\jramos\OneDrive - Renting Colombia S.A\Escritorio")


# In[ ]:




