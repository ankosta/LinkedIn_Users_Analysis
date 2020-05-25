This project was created for the market research purposes for Business Paradise - a LinkedIn consulting and training company. The goal is to understand the users of LinkedIn, their geographical distribution, as well as the industries they, work in. Collected data consisted of variables like: 
- total users in a given industry/ region, 
- number of users that post on LinkedIn, 
- number of users that have changed their jobs, 
that were taken as a sum of the last 90 days. It is important to acknowledge that all the numbers (except total users in a given industry) that LinkedIn provides are rounded down to millions (if in millions), thousands (if in thousands), or not at all if below thousand. For example, if you search for the total number of users in the "Information Technology and Services" industry, in the search window you will see a preview of an exactly "18,795,658 results", however in the results output it will appear as "18M+". This is a huge issue from the point of view of a data analyst, as the insights from such rounded numbers may be very biased and far from the truth. Those totals for the industries are scrapped from the search window in order to obtain the exact number. However, two remaining variables (# of users posting and # of users that have changed job) do not appear in the search window and are scrapped from the output view, where they are rounded. Those variables mostly appear in thousands, therefore the error between the real number and the rounded value will not be as big as in the example described above.

The project consists of three main parts:
1. Web scrapping using the Selenium library in Python and collecting relevant data.
2. Cleaning of the data, merging datasets, and creating derivative variables.
3. Data visualization. Creating PPT and Dashboards in Tableau Public.
