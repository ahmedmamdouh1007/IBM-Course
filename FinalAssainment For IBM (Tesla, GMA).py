#!/usr/bin/env python
# coding: utf-8

# In[4]:


# !pip install yfinance==0.1.67
# !pip install pandas==1.3.3
# !pip install requests==2.26.0
# !mamba install bs4==4.10.0 -y
get_ipython().system('pip install plotly==5.3.1')


# In[5]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[6]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[7]:


tesla = yf.Ticker("TSLA")
tesla


# In[8]:


tesla_data = tesla.history("max")
tesla_data


# In[9]:


tesla_data.reset_index(inplace=True)


# In[10]:


tesla_data.head()


# In[14]:


# https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue.
respond = requests.get("https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue").text
# respond


# In[15]:


soup = BeautifulSoup(respond , "html")
# soup


# In[16]:


revenues = soup.find("tbody").find_all("tr")
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in revenues:
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[18]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue["Revenue"]


# In[19]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[20]:


tesla_revenue.tail()


# In[21]:


# GME Company
GameStop = yf.Ticker("GME")


# In[22]:


gme_data = GameStop.history("max")


# In[23]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[24]:


# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html
respond = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html").text


# In[25]:


soup = BeautifulSoup(respond, "html")


# In[26]:


Revenues =soup.find("tbody").find_all("tr")
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in Revenues:
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text    
    gme_revenue = gme_revenue.append({"Date":date , "Revenue":revenue},ignore_index=True)


# In[30]:


gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(',|\$',"")
gme_revenue["Revenue"]


# In[31]:


gme_revenue.tail()


# In[32]:


# Plot Tesla Stock Graph
make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[33]:


# Plot GameStop Stock Graph
make_graph(gme_data, gme_revenue, 'GameStop')

