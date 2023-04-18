#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading Dataset

# In[2]:


df = pd.read_csv('hotel_bookings 2.csv')


# # Exploratory Data Analysis and Cleaning

# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


df.shape


# In[6]:


df.columns


# In[7]:


df.info()


# In[8]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[9]:


df.info()


# In[10]:


df.describe(include = 'object')


# In[13]:


for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[14]:


df.isnull().sum()


# In[15]:


df.drop(['company', 'agent'], axis = 1, inplace = True)
df.dropna(inplace = True)


# In[16]:


df.isnull().sum()


# In[18]:


df.describe()


# In[19]:


df['adr'].plot(kind = 'box')


# In[20]:


df = df[df['adr']<5000]


# In[22]:


df.describe()


# # Data Analysis and Visualizations

# In[28]:


canceled_perc = df['is_canceled'].value_counts(normalize = True)
print(canceled_perc)


# In[39]:


plt.figure(figsize = (5,4))
plt.title('Reservation Status Count', fontsize = 20)
plt.bar(['Not canceled', 'Canceled'], df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.8)
plt.show()


# In[47]:


plt.figure(figsize = (8,4))
ax1 = sns.countplot(x = 'hotel', hue = 'is_canceled', data = df, palette = 'Blues')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor = (1,1))
plt.title('Reservation Status in Different Hotels', size = 20)
plt.xlabel('Hotel')
plt.ylabel('Number of Reservations')
plt.legend(['Not canceled', 'Canceled'], fontsize = 15)
plt.show()


# In[33]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[34]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[35]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[55]:


plt.figure(figsize = (20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 35)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# In[53]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'Blues')
plt.title('Reservation Status per Month', size = 30)
plt.xlabel('Month', fontsize = 20)
plt.ylabel('Number of Reservations', fontsize = 20)
plt.legend(['Not canceled', 'Canceled'], fontsize = 20)
plt.show()


# In[61]:


plt.figure(figsize = (15,8))
plt.title('ADR per Month', fontsize = 30)
sns.barplot('month', 'adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# In[62]:


canceled_data = df[df['is_canceled'] == 1]
top_10_country = canceled_data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)
plt.show()


# In[63]:


df['market_segment'].value_counts()


# In[64]:


df['market_segment'].value_counts(normalize = True)


# In[65]:


canceled_data['market_segment'].value_counts(normalize = True)


# In[69]:


canceled_df_adr = canceled_data.groupby('reservation_status_date')[['adr']].mean()
canceled_df_adr.reset_index(inplace = True)
canceled_df_adr.sort_values('reservation_status_date', inplace = True)

not_canceled_data = df[df['is_canceled'] == 0]
not_canceled_df_adr = not_canceled_data.groupby('reservation_status_date')[['adr']].mean()
not_canceled_df_adr.reset_index(inplace = True)
not_canceled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize =(20,6))
plt.title('Average Daily Rate', fontsize = 30)
plt.plot(not_canceled_df_adr['reservation_status_date'], not_canceled_df_adr['adr'], label = 'not canceled')
plt.plot(canceled_df_adr['reservation_status_date'], canceled_df_adr['adr'], label = 'canceled')
plt.legend()
plt.show()

