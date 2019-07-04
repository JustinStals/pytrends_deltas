#!/usr/bin/python
__author__ = "Justin Stals"

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)

def get_deltas(keyword, show_plot=False):

	kw_list = [keyword]
	pytrends.build_payload(kw_list, cat=0, timeframe='all', geo='', gprop='')
	interest_over_time = pytrends.interest_over_time()

	current = int(interest_over_time[keyword].tail(1).values[0])

	deltas = {}

	for month_range in [3, 6]:
		tminus = float(interest_over_time[keyword].tail(month_range).values[0])
		if tminus != 0:
			deltas[str(month_range)+ 'm'] = float("{:.2f}".format(current / tminus * 100 / 1))
		else:
			deltas[str(month_range)+ 'm'] = None

	for year_range in [1, 3, 5]:
		tminus = float(interest_over_time[keyword].tail(year_range*12).values[0])
		if tminus != 0:
			deltas[str(year_range)+ 'y'] = float("{:.2f}".format(current / tminus * 100 / 1))
		else:
			deltas[str(year_range)+ 'y'] = None

	suggestions = pytrends.suggestions(keyword)

	if show_plot:
		for suggestion in suggestions:
			print(suggestion['title'], suggestion['type'])
		if show_plot:
			interest_over_time.plot()
			plt.show()

	return deltas