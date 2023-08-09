#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import numpy as np

# URL del servicio web
url = 'https://www.worldfleetlog.com/WebFleetStationServices/ManagedServices.asmx'

# Datos de la solicitud SOAP

SOAPEnvelope = '''
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <LoginInfo xmlns="http://tempuri.org/">
      <Username>usuario</Username>
      <Password>xxxxx</Password>
      <Company>Renting colombia</Company>
    </LoginInfo>
  </soap:Header>
  <soap:Body>
    <GetNextTripsRecords xmlns="http://tempuri.org/">
      <LastRecordID>0</LastRecordID>
      <MaxRecords>10</MaxRecords>
      <DeviceID></DeviceID>
      <StartDate>2023-07-01</StartDate>
    </GetNextTripsRecords>
  </soap:Body>
</soap:Envelope> '''

options = { 
'Content-Type': 'text/xml; charset=utf-8'
}

# Reemplazar los valores reales en el cuerpo SOAP
#SOAPEnvelope = SOAPEnvelope.replace('your_username', 'wsviajes')
#SOAPEnvelope = SOAPEnvelope.replace('your_password', 'Wsrc2024*')
#SOAPEnvelope = SOAPEnvelope.replace('your_company', 'Renting colombia')
#SOAPEnvelope = SOAPEnvelope.replace('dateTime', '2023-07-01 11:59:59')
#SOAPEnvelope = SOAPEnvelope.replace('string', '20585562')

# Realizar la solicitud POST
response = requests.post(url, data=SOAPEnvelope, headers=options)

# Verificar el código de respuesta
if response.status_code == 200:
    # Imprimir la respuesta
    print(response.content)
else:
    print('Error en la solicitud:', response.status_code)


# In[2]:


contenido = response.content


# In[3]:


from bs4 import BeautifulSoup
soup = BeautifulSoup(contenido, 'html.parser')


# In[4]:


xml_content = soup.find('getnexttripsrecordsresult').text


# In[5]:


df = pd.read_xml(xml_content)


# In[6]:


df


# In[7]:


df['NN'].value_counts()


# In[ ]:




