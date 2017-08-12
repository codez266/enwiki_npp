import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import pdb

review_usersset = 'quarry-20824-users-doing-page-reviews-run196795.tsv'
col = 'log_user'
df = pd.read_csv(review_usersset, delimiter='\t')
# get total years to iterate on
years = df['year'].unique()
review_users = np.array([])
avg_reviews = np.array([])
for y in years:
    df_tmp = df[df['year'] == y]
    # Get unique months in the year
    months = df_tmp['month'].unique()
    for m in months:
        reviewers_per_month = df_tmp[df['month'] == m][col].count()
        # Add per month review users to the array
        review_users = np.append(review_users, reviewers_per_month)
        # Add per month average reviews to the array
        avg_reviews = np.append(avg_reviews, df_tmp[df['month'] == m]['reviews_performed'].mean())

# Generate year-months for x-axis
months = pd.date_range('2015-11', periods=review_users.shape[0], freq='1m')
f = open('reviewers_parser.wiki','w')
for i, m in enumerate(months):
    f.write('|-\n|{:%Y-%m}\n|{}\n|{}\n'.format(m, review_users[i], avg_reviews[i]))
f.close()
multiple_bars = plt.figure()

plt.plot(months, review_users, label="users doing review")
plt.plot(months, avg_reviews, label="mean review per user that month")
plt.ylabel('Average editors reviewing / Mean reviews')
plt.xlabel('Months')
plt.legend()
xfmt = mdates.DateFormatter('%d-%m-%y')
plt.axvline('2016-11', color='b', linestyle='dashed', linewidth=2, label="NPP right implementation")
plt.text('2016-11', plt.gca().get_ylim()[1]+5,'NPP user right implementation', ha='center', va='center')
plt.show()
