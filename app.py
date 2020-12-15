import streamlit as st
import pandas as pd
import pyodbc as pypy
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
from math import pi

from sqlalchemy import create_engine 


st.title("Scouting Tool Test")

password = st.text_input("Enter password", type="password")

if password != 'BIF1864.fodbold':
	st.error("Invalid password.")
else:

	@st.cache(allow_output_mutation=True)
	def get_data():
		con=pypy.connect(
		"Driver={SQL Server};Server=BIF-SQL02\SQLEXPRESS02;Database=Scouting_BI;Trusted_connection=yes"
		)
		
		q1 = pd.read_sql_query(
		"select *, CONCAT(playerId,', ', seasonId) AS player_season_ID, CONCAT(firstName,' ', lastName,', ',competition,', ',season,', ',radar_group) AS longID from Player_and_Averages_Info",
		con
		)
		
		player_info = pd.DataFrame(q1)

		#,columns=['playerId','season','seasonId',
		#	'competition','competitionId','radar_group','firstName','lastName',
	   # 	'height','weight','age','mins','foot','passportId','map_group', "player_season_ID","longID"])
		
		con2=pypy.connect(
		"Driver={SQL Server};Server=BIF-SQL02\SQLEXPRESS02;Database=Reporting;Trusted_connection=yes"
		)
		
		q2 = pd.read_sql_query(
		"select CONCAT(playerId,', ', seasonId) AS player_season_ID, radar_group as r_group, skill, skill2, value from Radar_All_Averages",
		con2
		)

		radar = pd.DataFrame(q2)

		q3 = pd.read_sql_query(
		"select * from radar_skill_filter",
		con2
		)

		skill_filter = pd.DataFrame(q3)

		q4 = pd.read_sql_query(
		"select * from radar_percentile_filter",
		con2
		)

		p_filter = pd.DataFrame(q4)

		#, columns=["playerId","seasonId","radar_group","skill","skill2","value","player_season_ID"])



		return player_info, radar, skill_filter, p_filter


	data_load_state = st.text('Loading...')

	players, radar, skill_filter, p_filter = get_data()

	data_load_state.text("")

	# if st.checkbox('Show raw players'):
	# 	st.subheader('Raw players')
	# 	st.write(players.head())

	# if st.checkbox('Show raw radars'):
	# 	st.subheader('Raw radars')
	# 	st.write(radar.head())

	# if st.checkbox('Show skill filter'):
	# 	st.subheader('Skill filter')
	# 	st.write(skill_filter.head())

	select_radar = st.selectbox(
		label = 'Radar',
		options = ['back','center_back','wing_back','defensive_midfielder','box_to_box_player','wing','attacking_midfielder','forward'],
		)

	# if st.checkbox('Show select_radar'):
	# 	st.subheader('Select_radar')
	# 	st.write(select_radar)

	skill_filter = skill_filter[skill_filter["Radar_Group"] == select_radar]


	# if st.checkbox('Show skill_filter'):
	# 	st.subheader('Skill_filter')
	# 	st.write(skill_filter)
	

	select_player = st.multiselect('Player', players['longID'])
	new_df = players[(players['longID'].isin(select_player))]

	plot_data = new_df.set_index('player_season_ID').join(radar.set_index('player_season_ID'))

	plot_data = plot_data[plot_data['skill'].isin(skill_filter['Skill'])]

	plot_data['index1'] = plot_data.index

	# if st.checkbox('Show plot data'):
	# 	st.subheader('Plot data')
	# 	st.write(plot_data)

	
	if len(select_player) > 0 and select_radar:
		#make empty radar plot
		fig = plt.figure(figsize = (12,6))
		ax = plt.subplot(111)

		categories = list(set(plot_data['skill2'].tolist()))
		N = len(categories)
		print(N)

		#ax1 = plt.subplot(121)
		#ax1.axis('off')
		#ax2 = plt.subplot(122, polar=True)
		for player in select_player:
			a = np.where(plot_data['longID'] == player)
			player_data = plot_data.iloc[a[0],]

			values = player_data['value'].tolist()
			values += values[:1]
			
			ticks = [n / float(N)*2* pi for n in range(N)]
			ticks += ticks[:1]
			
			plt.polar(ticks, values, marker = '.')
			plt.fill(ticks, values, alpha = 0.3)
			plt.xticks(ticks[:-1], categories)
			
			plt.yticks([0.25,0.50,0.75,1], color = "None", size=10)
			plt.ylim(0,1)
			ax.tick_params(axis="x",pad = 50)

		st.pyplot(fig)

	



	
	







#to plot images from URLS
#https://medium.com/python-in-plain-english/radar-chart-basics-with-pythons-matplotlib-ba9e002ddbcd
