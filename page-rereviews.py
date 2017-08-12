import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import pdb

"""
Following SQL query was used on Quarry to get the dataset:

use enwiki_p;
SELECT EXTRACT(YEAR FROM DATE_FORMAT(log_timestamp,'%Y%m%d%H%i%s')) AS `year`,
       EXTRACT(MONTH FROM DATE_FORMAT(log_timestamp,'%Y%m%d%H%i%s')) AS `month`,
	   	log_title, log_page, log_timestamp FROM logging_logindex WHERE log_type='pagetriage-curation'
        AND log_timestamp between 20151001000000 and 20170731000000
		ORDER BY `year` ASC, `month` ASC;

"""

page_rereviewsset = 'quarry-20777-re-reviews-of-new-pages-run196734.tsv'
df = pd.read_csv(page_rereviewsset, delimiter='\t')
# get total years to iterate on
years = df['year'].unique()
page_rereviews = np.array([])
avg_reviews = np.array([])
# aggregate the data for each month
for y in years:
    df_tmp = df[df['year'] == y]
    # Get unique months in the year
    months = df_tmp['month'].unique()
    for m in months:
        page_rereviews = np.append(page_rereviews, 0)
        reviews_per_month = df_tmp[df['month'] == m]
        prev_id = 0
        for index, row in reviews_per_month.iterrows():
            page_id = row['log_page']
            # If continuous review entries of a page exist, likely from the same
            # session, here we're looking at a new page id so add it
            if prev_id != page_id:
                page_rereviews[-1] = page_rereviews[-1] + 1
            prev_id = page_id

# Generate year-months for x-axis
months = pd.date_range('2015-11', periods=page_rereviews.shape[0], freq='1m')
# For storing the aggregate data in wikitable format
f = open('page_rereviews.wiki','w')
for i, m in enumerate(months):
    f.write('|-\n|{:%Y-%m}\n|{}\n'.format(m, page_rereviews[i]))
f.close()
plt.figure()

plt.plot(months, page_rereviews, label="users doing review", c='orange')
plt.ylabel('Re-reviews per month')
plt.xlabel('Months')
plt.legend()
xfmt = mdates.DateFormatter('%d-%m-%y')
plt.axvline('2016-11', color='b', linestyle='dashed', linewidth=2, label="NPP right implementation")
plt.text('2016-11', plt.gca().get_ylim()[1]+10,'NPP user right implementation', ha='center', va='center')
plt.show()
