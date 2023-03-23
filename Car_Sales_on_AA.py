#!/usr/bin/env python
# coding: utf-8

# # Part 2 - Car Sales on AA
# ## by Philip Obiorah

# ### Introduction
#  "The AA believe in AA Cars as a valuable tool for people looking to buy a used car."(AA Cars 2023).  The aim of this work is to build a dataset on cars sales. The data is collected from AA website (https://www.theaa.com/cars/). Our objectives includes to : 
# - (a) collect 1000 items returned by search query of the website and save them into csv files. Data collected would include:
# 
# |     |     |
# | --- | --- |
# |Sale’s title|CO2 Emissions|
# |Location/ Distance|Transmission
# |Price|Number of seats
# |Year|Colour 
# |Mileage|Engine size
# |Fuel Type|Number of Reviews
# |Body Type|Rating 
# 
# - b)Identify any problems with the data and clean accordingly.
# - c)Calculate the total car sales based on the “year” feature 
# - d)Compare car sales on their transmission features 
# - e)What are the most popular car sales based on the “Body Type”? 
# - f)List top 10 cars having highest numbers of reviews. 
# We shall employ BeautifulSoup and Requests python libraries and also different means of data  acquisition  (scraping), cleaning, and exploration to archive our objective. 

# ### Gathering

# In[656]:


# import the required libraries
import csv
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt


# In[253]:





# In[483]:


#initialize the variables required
page_count = 1
car_urls = []
base_url = "https://www.theaa.com"
url = "https://www.theaa.com/used-cars/displaycars?fullpostcode=MK18%201EG&travel=2000&page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
car_link = ""


# Set the name of the output file
output_file = 'AAcars_data.csv'

# Set up the CSV writer
csv_file = open(output_file, 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write the header row
csv_writer.writerow(['sales_title', 'url', 'location'])

# loop using range of no. required
for page_count in range(1, 51):
    
    try:
        # Send a request to the server
        response = requests.get(url + str(page_count), headers=headers)
        
        
        
        time.sleep(5)
    except requests.HTTPError as err: 
        print(err)    
        
    except requests.ConnectionError as cerr:
        print(cerr)  
        
        
    else:
        print(response.status_code,":" ,end="")
        print(page_count, ":Receiving..",url + str(page_count))
        
   
    # Let's use BeautifulSoup to parse the response content
    soup = BeautifulSoup(response.content, "html.parser")
    # use soup object to extract html elements in the div with class : vl-item clearfix
    car_listings_page = soup.find_all("div", {"class": "vl-item clearfix"})
    
    #for each car in the car_listing page
    for car in car_listings_page:
        car_link = base_url + car.find("h3", {"class": "vl-title"}).find("a", {"class":"black-link"}).get("href").strip()
        sales_title = car.find("h3", {"class": "vl-title"}).get('title').strip()
        location = car.find("div", {"class":"vl-location"}).contents[1].text.strip()
        #car_urls.append(car_link)
        # Write the data to the CSV file (save sales_tilte, url, and location )
        csv_writer.writerow([sales_title.strip(), car_link,location])

            
# Close the CSV file
csv_file.close()        


# Data containing sales_tilte, url, and location from the url (https://www.theaa.com/used-cars/displaycars?fullpostcode=MK18%201EG&travel=2000&page=50 )sample save is saved as `AAcars_data.csv` 

# In[484]:


# Load data from CSV file
df = pd.read_csv('AAcars_data.csv', names=['sales_title', 'url','location'], header=None, skiprows=1, sep=',')

df


# In[490]:


#We create a list of car_urls, sales_title, and location
car_urls= list(df['url'])
sales_title = list(df['sales_title'])
location = list(df['location'])


# In[497]:


# Set the name of the output file
aa_output_file = 'AAcars_data_complete.csv'

# Set up the CSV writer
aa_csv_file = open(aa_output_file, 'w', newline='')
aa_csv_writer = csv.writer(aa_csv_file)

# Write the header row
aa_csv_writer.writerow(['Make', 'Model', 'Title', 'Price', 'Mileage', 'Year', 'Transmission', 'Fuel Type', 'Reviews', 'Rating', 'CO2 Emission', 'Engine Size', 'Color', 'Doors', 'Body Type', 'Distance'])


# In[498]:


#count no of cars
count = 0
for url, sale_title, loc in zip(car_urls,sales_title, location):
    try:
        # Send a request to the server
        response = requests.get(url, headers=headers)
        time.sleep(1)
    except requests.HTTPError as err: 
        print(err)    

    except requests.ConnectionError as cerr:
        print(cerr)  


    else:
        print(response.status_code,": ", end="")
        count = count + 1
        print(count, ":", url)               


        # Let's use BeautifulSoup to parse the response content
        soup = BeautifulSoup(response.content, "html.parser")

        car_page = soup.find_all("div", {"class": "top-content clearfix"})
        #loop throught the car page
        for vehicle in car_page:
            
            try:
                title = sale_title.strip()
            except IndexError:
                title = None
            try:
                make = vehicle.find("div", {"class":"vehicle-name clearfix"}).contents[1].contents[1].contents[0].text.strip()
            except IndexError:
                make = None
            try:
                model = vehicle.find("div", {"class":"vehicle-name clearfix"}).contents[1].contents[1].contents[1].text.strip()
            except IndexError:
                model = None
            try:
                price = vehicle.find("strong", {"class":"total-price"}).text.strip()
            except IndexError:
                price = None
            try:
                mileage = vehicle.find("ul", {"class":"vd-specs-list"}).contents[1].contents[3].contents[3].text.strip()
            except IndexError:
                mileage = None
            try:
                transmission = vehicle.find("ul", {"class":"vd-specs-list"}).contents[7].contents[3].contents[1].text.strip()
            except IndexError:
                transmission = None
            try:
                year = vehicle.find("ul", {"class":"vd-specs-list"}).contents[3].contents[3].contents[3].text.strip()
            except IndexError:
                year = None
            try:
                fuel_type = vehicle.find("ul", {"class":"vd-specs-list"}).contents[5].contents[3].contents[1].text.strip()
            except IndexError:
                fuel_type = None
            try:
                reviews = vehicle.find("div", {"class":"vehicle-name clearfix"}).contents[3].contents[1].contents[3].contents[1].get("content").strip()
            except IndexError:
                reviews = None
            try:
                rating = vehicle.find("div", {"class":"vehicle-name clearfix"}).contents[3].contents[1].contents[3].contents[5].get("content")
            except IndexError:
                rating = None
            try:
                co2_emission = vehicle.find("ul", {"class":"vd-specs-list"}).contents[16].contents[3].contents[3].text.strip()
            except IndexError:
                co2_emission = None
            try:
                engine_size = vehicle.find("ul", {"class":"vd-specs-list"}).contents[14].contents[3].contents[1].text.strip()
            except IndexError:
                engine_size = None
            try:
                color = vehicle.find("ul", {"class":"vd-specs-list"}).contents[10].contents[3].contents[1].text.strip()
            except IndexError:
                color = None
            try:
                doors = vehicle.find("ul", {"class":"vd-specs-list"}).contents[12].contents[3].contents[1].text.strip()
            except IndexError:
                doors = None
            try:
                body_type = vehicle.find("ul", {"class":"vd-specs-list"}).contents[8].contents[3].contents[1].text.strip()
            except IndexError:
                body_type = None
            try:
                distance = loc
            except IndexError:
                distance = None
        #write values to CSV        
        aa_csv_writer.writerow([make, model, title, price, mileage, year, transmission, fuel_type, reviews, rating, co2_emission, engine_size, color, doors, body_type, distance]) 
        print("Car Make: {}\nModel: {}\nTitle: {}\nPrice: {}\nMileage: {}\nYear: {}\nTransmission: {}\nFuel Type: {}\nReviews: {}\nRating: {}\nCO2 Emission: {}\nEngine Size: {}\nColor: {}\nDoors: {}\nBody Type: {}\nDistance: {}\n".format(make, model, title, price, mileage, year, transmission, fuel_type, reviews, rating, co2_emission, engine_size, color, doors, body_type, distance))



# ### Accessing Data
# `AAcars_data_complete.csv`

# In[612]:


# Load data from CSV file
aa_cars_df = pd.read_csv('AAcars_data_complete.csv',names=['make', 'model', 'title', 'price', 'mileage', 'year', 'transmission', 'fuel_type', 'reviews', 'rating', 'co2_emission', 'engine_size', 'color', 'doors', 'body_type', 'distance'], header=None, skiprows=1, sep=',')


# In[613]:


#view the loaded complete  AAcars_data_complete.csv
aa_cars_df.head()


# In[614]:


# view the no of rows and column
aa_cars_df.shape


# The scrapped AA CARs dataset comprise of 973 rows and 16 columns. We intended to scrap about 1000 rows however,the website had some car pages inactive as some of the cars where already sold at the point of scrapping. 

# In[615]:


#View datatypes
aa_cars_df.dtypes


# In[616]:


# Lets check for Quality and Tidyness
aa_cars_df.info()


# In[617]:


# Let check for NaN
aa_cars_df.isna().sum()


# In[618]:


# Let us check for null values
aa_cars_df.isnull().sum()


# In[619]:


#Let us check for duplicate rows
aa_cars_df.duplicated().sum()


# In[620]:


#Descriptive statistics for numeric values
aa_cars_df.describe()


# #### (b) Issues/Problems with data
#  - Incorrect datatype for price
#  - Incorrect datatype for mileage
#  - NaN present in `ratings` and `reveiws`, `co2_emission`, `engine_size`
#  - 'Semi auto' and 'Semiauto' values in the 'transmission' column
#  
#      

# ### Data Cleaning

# In[621]:


#Let us make a copy of the orignal dataset.
aa_cars_clean_df = aa_cars_df.copy()


# In[622]:


#View the dataframe
aa_cars_clean_df


# ### Incorrect datatype for price

# ##### Define
# - Replace `£` in price with " "  using `str.replace()` function
# - Convert the "price" column to integer using astype() function

# ##### Code

# In[623]:


#Replace `£` in price with " "  using `str.replace()` function
#Convert the "price" column to integer using astype() function
aa_cars_clean_df['price'] = aa_cars_clean_df['price'].str.replace('£', '').str.replace(',', '').astype(int)


# ##### Test

# In[624]:


# Confirm that  "price" column is converted to to integer
aa_cars_clean_df['price'].dtype


# ### Incorrect datatype for mileage

# ##### Define
# - Replace `,` in mileage with empty string
# - Convert `mileage` to int

# ##### Code

# In[625]:


# Replace `,` in mileage with empty string
aa_cars_clean_df['mileage']= aa_cars_clean_df['mileage'].str.replace(',','')
# Convert `mileage` to int
aa_cars_clean_df['mileage']= aa_cars_clean_df['mileage'].astype(int)


# ##### Test

# In[626]:


# Confirm that `mileage` is converted to int
aa_cars_clean_df['mileage'].dtype


# ### NaN present in `ratings` and `reveiws`, `co2_emission`, `engine_size`

# ##### Define

# - Drop columns not required in the analysis
# - Remove NaN using dropna() method

# ##### Code

# In[627]:


# Fill NaN values with the mean of the column
aa_cars_clean_df = aa_cars_clean_df.drop(['co2_emission','engine_size'], axis=1)


# In[633]:


#Remove NaN using dropna() method
aa_cars_clean_df= aa_cars_clean_df.dropna()


# ##### Test
# - Test that  NaN  is not present in `ratings` and `reveiws`,  We would ignore NaN in `co2_emission`, `engine_size` as we would not utilize them in our analysis

# In[632]:


# Test that  NaN  is not present in `ratings` and `reveiws`,  
aa_cars_clean_df.isna().sum()   


# ### 'Semi auto' and 'Semiauto' values in the 'transmission' column

# ##### Define
# - Combine 'Semi auto' and 'Semiauto' values in the 'transmission' column

# ##### Code

# In[695]:


# combine 'Semi auto' and 'Semiauto' values in the 'transmission' column
aa_cars_clean_df['transmission'] = aa_cars_clean_df['transmission'].replace(['Semi auto', 'Semiauto'], 'Semi-auto')


# ##### Test

# In[706]:


# Test combination of  'Semi auto' and 'Semiauto' values in the 'transmission' column
aa_cars_clean_df['transmission'].unique()


# In[697]:


#view the dataframe info after cleaning
aa_cars_clean_df.info()


# ### Data Storage
# After the data cleaning process it is necessary that we store our clean datasdet into a new csv file

# In[698]:


# save dataframe to `aa_cars_data_clean.csv`
aa_cars_clean_df.to_csv('aa_cars_data_clean.csv', index=False)


# ### Data Analysis
# 
# We shall attempt the the folowing:
# 
# - c)Calculate the total car sales based on the “year” feature 
# - d)Compare car sales on their transmission features 
# - e)Determine the most popular car sales based on the “Body Type”? 
# - (f)List top 10 cars having highest numbers of reviews. (5 marks)

# In[699]:


# load the 'aa_cars_data_clean.csv' into `aa_cars_master_df`
aa_cars_master_df = pd.read_csv('aa_cars_data_clean.csv')
aa_cars_master_df.sample(20)


# ### The total car sales based on the “year” feature

# In[700]:


#The total car sales based on the “year” feature
year_title_sale = aa_cars_master_df.groupby('year')['title'].count()
year_title_sale


# In[701]:


#plot graph of no of titles  
year_title_sale.plot(kind="bar")
plt.title('No for Sale by Year')
plt.xlabel('Year of Car Model')
plt.ylabel('No of Cars')
plt.show()


# The figure above shows the number of cars for sale by year of manufacture. 2021 car models has the heighest number of  123 cars. There is very few cars manufactured between 2001 to 2003 for sale. 

# ### Compare car sales on their transmission features

# In[702]:


# group the cars based on their transmission type
grouped_cars= aa_cars_master_df.groupby('transmission')


# In[703]:


# count the number of cars with manual and automatic transmission
num_cars = grouped_cars['transmission'].count()
num_cars


# In[704]:


# plot the results using a bar plot
fig, ax = plt.subplots()
ax.bar(num_cars.index, num_cars.values)
ax.set_xlabel('Transmission')
ax.set_ylabel('Number of Cars')
ax.set_title('Car Sales by Transmission Type')
plt.show()


# There are more manual transmission cars for sale than automatic transmission. 352 Automatic transmission cars, 
#  518 Manual transmission cars ,  38 Semi-auto  , Other 1
# 

# ### The most popular car sales based on the “Body Type”
# 

# In[707]:


# group the cars based on their body type
grouped_body_type = aa_cars_master_df.groupby('body_type')


# In[736]:


# count the number of cars based on body type
body_type_num = grouped_body_type['body_type'].count()
body_type_num = body_type_num.sort_values(ascending=False)
body_type_num


# In[737]:


# plot the data
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(body_type_num.index, body_type_num.values)
ax.set_xlabel('Body Type')
ax.set_ylabel('Count')
ax.set_title('Car Body Type Distribution')
plt.xticks(rotation=90)
plt.show()


# As shown in the graph, there are over 490 automobiles of the Hatchback body type, making it the most prevalent body type in the dataset. With over 190 vehicles, SUVs are the second most popular body style. With over 30 automobiles apiece, Estate, MPV, and Panel van are further popular body variants.
# 
# On the other hand, a small percentage of the automobiles in the sample have some very uncommon body forms. For instance, there is just one of each type of station waggon, cabriolet, window van, and temperature-controlled vehicle.
# 

# ### List top 10 cars having highest numbers of reviews

# In[725]:


grouped_reviews = aa_cars_master_df.groupby('make')['reviews'].sum()
# group the dataframe by country and sum the suicides_no column
#country_suicides = suicide_master_df.groupby('country')['suicides_no'].sum()
grouped_reviews


# In[738]:


#group and slice the top ten [:10]
top_ten_cars = grouped_reviews.sort_values(ascending=False)[:10]


# In[729]:


#top ten cars
top_ten_cars


# In[732]:



# plot the top 10 cars
plt.figure(figsize=(10, 6))
plt.bar(top_ten_cars.index, top_ten_cars.values)
plt.title('Top 10 Cars by Number of Reviews')
plt.xlabel('Car Make')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=45, ha='right')
plt.show()


# From the visual above , Ford has the most reviews (23,425), followed by Toyota (17,546) and Vauxhall (12,485). In terms of the number of reviews, these three automobile brands much outnumber the others.
# 
# Nissan, Kia, Volkswagen, Renault, Hyundai, Citroen, and Peugeot have got less reviews, with Nissan receiving the fourth-most (3,289) and Peugeot receiving the tenth-most (1,420).
# 
# This points to the popularity of certain automobile brands based on the amount of reviews from the dataset

# In[ ]:




