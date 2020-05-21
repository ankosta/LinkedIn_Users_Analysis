""" 1. LOGIN TO THE WEB """

# import web driver
from selenium import webdriver
# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('/Users/User/Downloads/chromedriver')
""" a window will pop up and ask for permission to control browser"""
# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/login')
# locate email form by_class_name
username = driver.find_element_by_name('session_key')
# send_keys() to simulate key strokes
username.send_keys('email@gmail.com') # here introduce your login email
# locate password form by_class_name
password = driver.find_element_by_name('session_password')
# send_keys() to simulate key strokes
password.send_keys('password') # here introduce your private password

# locate submit button by_class_id
log_in_button = driver.find_element_by_class_name('btn__primary--large')

# .click() to mimic button click
log_in_button.click()

""" 2. INDUSTRY NAMES FOR THE 1-148 IDs """

industry = range(1, 149)
id_industry_urls_l = []
for i in industry:
    url_ind = "https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&industryIncluded={}".format(i)
    driver.get(url_ind)
    id_industry = driver.find_element_by_xpath("//li[@class='artdeco-pill--blue mr1 mb1 ignore-filter-collapse control-pill flex artdeco-pill artdeco-pill--2 artdeco-pill--dismiss ember-view']/div[@class='control-pill__text max-width min-width flex']/span[@class='block max-width nowrap-ellipsis']")
    industry_name = id_industry.text
    id_industry_urls_l.append([i, url_ind, industry_name])

id_industry_urls_df = pd.DataFrame(columns = ["i", "url_ind", "industry"], data =id_industry_urls_l)

id_industry_urls_df.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\industry_name_id.csv', index = False, header=True)

""" 3. TOTAL USERS FOR EACH INDUSTRY """

"""The total_n unfortunately is a rounded value to millions! That gives a very wide spread of variation and bias to the real value.
I will try to retrive the exact amount that appears only in the search window."""
### 1. Prepare industry ids
industry = pd.read_csv('C:/Users/User/Desktop/GitHub_Projects/My Projects/industry_name_id.csv')
industry.head()
ind=industry["id_industry"]
ind=ind.drop([1], axis=0)

### 2. Scrap the industry names
total_det = []
for i in ind:
    driver.get('https://www.linkedin.com/sales/search/people?preserveScrollPosition=true&selectedFilter=I&skippedOnboarding=false&viewAllFilters=true')
    ind_xpath = "//button[@title='{}']".format(i)
    ind_button = driver.find_element_by_xpath(ind_xpath)
    ind_button.click()
    driver.implicitly_wait(3)
    total = driver.find_element_by_class_name("ph2").text
    total_det.append([i, total])

total_df = pd.DataFrame(columns = ["industry", "total"], data = total_det)
total_df.head()

total_df.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\sales_navigator_total_ind.csv', index = False, header=True)

""" 4. TOTAL NUMBER OF JOBS CHANGED AND POSTS FOR EACH INDUSTRY """
### 1. CREATE URL LIST (industry)
import pandas as pd
import numpy

industry = range(1, 149) # corresponds to ids representing possible industries
i_urls_l = [] #empty

# get urls for all combinations of regions and industries
for i in industry:
    url = "https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&industryIncluded={}".format(i)
    i_urls_l.append([i, url])
# we have list compund info, lets make a df object out of it:
i_urls_df = pd.DataFrame(columns = ["i", "url"], data = i_urls_l)
i_urls_df.head(10) # check if we obtained the desired format
# lets extract only urls
i_urls_df = i_urls_df[i_urls_df.i != 2]
urls = i_urls_df["url"]

### 2. USE URLS TO SCRAP DATA

results_l = []

for url in urls:# how to add industry and region
     driver.get(url)
     job_change_n = driver.find_element_by_xpath("//button[@id='search-spotlight-tab-RECENT_POSITION_CHANGE']/span[@class='artdeco-spotlight-tab__primary-text']").text
     post_n = driver.find_element_by_xpath("//button[@id='search-spotlight-tab-RECENTLY_POSTED_ON_LINKEDIN']/span[@class='artdeco-spotlight-tab__primary-text']").text
     results_l.append([job_change_n, post_n, url])

results_df = pd.DataFrame(columns = ["job_change_n", "post_n", "url"], data = results_l)

len(i_urls_df)
len(results_df)
dataset = pd.merge(i_urls_df,
                    results_df,
                    on = "url")
len(dataset)

dataset.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\sales_totals_round.csv', index = False, header=True)

""" 5. TOTAL NUMBER OF USERS, JOBS CHANGED AND POSTS FOR EACH INDUSTRY AND EACH REGION """
### 1. CREATE URL LIST (industry&region)

# url for region: 'Europe' & industry: 'Accounting'
# https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&geoIncluded=100506914&industryIncluded=47&logHistory=true&page=1&rsLogId=278332905&searchSessionId=g2UdNAVqTJuuGAJmVQ5O7A%3D%3D&selectedFilter=GE
# we can see geoIncluded=100506914 & industryIncluded=47
# there are range of industries from 1 to 148, except of 2, to which there is no industry assigned to
# geo numbers are difficult to guess, I will collect it manualy

industry = range(1, 149) #fill with industries
region = ["103537801", "91000003", "91000004", "102393603",  "91000005", "91000006", "91000007", "100506914", "91000008", "91000009", "102221843", "91000010", "104514572"] #fill with regions
i_r_urls_l = [] #empty

for i in industry:
    url_i = '&industryIncluded={}'.format(i)
    for r in region:
        url = 'https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&geoIncluded='.format(r) + url_i
        i_r_urls_l.append([i, r, url])
# we have list compund info, lets make a df object out of it:
i_r_urls_df = pd.DataFrame(columns = ["i", "r", "url"], data = i_r_urls_l)
i_r_urls_df.head(3) # check if we obtained the desired format
# lets extract only urls
i_r_urls_df = i_r_urls_df[i_r_urls_df.i != 2]
urls = i_r_urls_df["url"]

### 2. USE THE URLS LIST TO SCRAP DATA

results_l = []

for url in urls:# how to add industry and region
     driver.get(url)
     driver.implicitly_wait(4)
     total_n = driver.find_element_by_xpath("//button[@id='search-spotlight-tab-ALL']/span[@class='artdeco-spotlight-tab__primary-text']").text
     job_change_n = driver.find_element_by_xpath("//button[@id='search-spotlight-tab-RECENT_POSITION_CHANGE']/span[@class='artdeco-spotlight-tab__primary-text']").text
     post_n = driver.find_element_by_xpath("//button[@id='search-spotlight-tab-RECENTLY_POSTED_ON_LINKEDIN']/span[@class='artdeco-spotlight-tab__primary-text']").text
     results_l.append([total_n, job_change_n, post_n, url])

results_df = pd.DataFrame(columns = ["total_n", "job_change_n", "post_n", "url"], data = results_l)

### 4. MERGE OBTAINED URLS AND SAVE AS CSV
len(i_r_urls_df)
len(results_df)
dataset = pd.merge(i_r_urls_df,
                    results_df,
                    on = "url")
len(dataset)

# save resulting data to csv file
data_complete.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\sales_navigator_stats_all.csv', index = False, header=True)

# At the end it is important to log of from the Sales Navigator
# locate log off button by_class_id
log_off_button = driver.find_element_by_class_name('btn__primary--large')

# .click() to mimic button click
log_off_button.click()

""" 6. CLEANING OF OBTAINED DATASETS """

### 1. TOTALS ONLY BY INDUSTRY:
total_ind_det = pd.read_csv("C:/Users/User/Desktop/GitHub_Projects/My Projects/sales_navigator_total_ind.csv")
total_ind_det.head()
total_job_post = pd.read_csv("C:/Users/User/Desktop/GitHub_Projects/My Projects/sales_totals_round.csv")
total_job_post.head()
# To id industry names with ids:
industry_name_id = pd.read_csv("C:/Users/User/Desktop/GitHub_Projects/My Projects/industry_name_id.csv")
industry_name_id.head()
### 2. MERGE TOTALS BY INDUSTRY
del industry_name_id['url_ind']
industry_name_id = industry_name_id[industry_name_id.i != 2]
industry_dict = dict(zip(industry_name_id.i, industry_name_id.industry))
len(industry_name_id)
len(total_job_post)
total_job_post = total_job_post.replace({"i": industry_dict})
total_job_post.rename(columns={'i':'industry'}, inplace=True)
total_job_post.head()
len(total_ind_det)
totals = pd.merge(total_job_post,
                    total_ind_det,
                    on = "industry")
### 4. CLEAN TOTALS BY INDUSTRY
#if totals[totals[col].str.contains(pat = '\d\.\d+', regex = True)]:
tot_cols = ["job_change_n", "post_n"]

for col in tot_cols:
    i = 0
    for y in totals[col]:
        if "." in y:
            print(y)
            y = y.replace("K", "00").replace("M","00000").replace(".","").replace("+","")
            totals[col][i] = y
            print(totals[col][i])
        else:
            print(y)
            y = y.replace("K", "000").replace("M","000000").replace("+","")
            totals[col][i] = y
            print(totals[col][i])
        i += 1

totals["total"] = totals["total"].str.replace(" results","").str.replace(",","")

pd.to_numeric(totals["total"])
pd.to_numeric(totals["job_change_n"])
pd.to_numeric(totals["post_n"])

totals.sort_values(by=['job_change_n'], inplace=True)

totals.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\1_sales_navigator_totals.csv', index = False, header=True)

### 5. TOTALS BY INDUSTRY AND REGIONS:
stats = pd.read_csv("C:/Users/User/Desktop/GitHub_Projects/My Projects/sales_navigator_stats_all.csv")
stats.head()
# To id industry names with ids:
industry_name_id = pd.read_csv("C:/Users/User/Desktop/GitHub_Projects/My Projects/industry_name_id.csv")
industry_name_id.head()
# To id region names with ids:
region_dic = {103537801:"Africa", 91000003:"APAC", 91000004:"APJ", 102393603:"Asia", 91000005:"Benelux", 91000006:"DACH", 91000007:"EMEA", 100506914:"Europe", 91000008:"MENA", 91000009:"Nordics", 102221843:"North America", 91000010:"Oceania", 104514572:"South America"}

# CONCATE TOTALS BY INDUSTRY AND REGION
del industry_name_id['url_ind']
industry_name_id = industry_name_id[industry_name_id.i != 2] # as #2 does not represents any industry
industry_dict = dict(zip(industry_name_id.i, industry_name_id.industry))

stats = stats.replace({"r": region_dic})
stats.rename(columns={'r':'region'}, inplace=True)
stat_cols = ["total_n", "job_change_n", "post_n"] #"job_change_n", "post_n"

stats.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\2_sales_navigator_concate_raw.csv', index = False, header=True) # save it before the cleaning for verification purposes
stats.reset_index(drop=True, inplace=True)

for col in stat_cols:
    i = 0
    for y in stats[col]:
        if "." in y:
            y = y.replace("K", "00").replace("M","00000").replace(".","").replace("+","")
            stats[col][i] = y
        else:
            y = y.replace("K", "000").replace("M","000000").replace("+","").replace(",","")
            stats[col][i] = y
        i += 1

len(stats)
stats = stats.replace({"i": industry_dict})
len(stats)
stats.head()

pd.to_numeric(stats["total_n"])
pd.to_numeric(stats["job_change_n"])
pd.to_numeric(stats["post_n"])

stats.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\2_sales_navigator_stats_i_r.csv', index = False, header=True)

regions = ["APAC", "APJ", "Benelux", "DACH", "EMEA", "MENA", "Nordics"]
continents = ["Asia", "Europe", "South America", "North America", "Oceania", "Africa"]
stats_continent = stats.copy()

for r in regions:
    stats_continent = stats_continent[stats_continent.region != r]

stats_continent["region"].value_counts()

stats_continent.to_csv (r'C:\Users\User\Desktop\GitHub_Projects\My Projects\2_sales_navigator_stats_continent.csv', index = False, header=True)
