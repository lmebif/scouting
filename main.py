import streamlit as st
import pymssql as pypy
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from sqlalchemy import create_engine

if __name__ == '__main__':
    st.set_page_config(initial_sidebar_state="expanded",
        layout="centered",
        page_title="BIF Scouting",
        page_icon="https://brondby.com/files/design/images/2016/logo.png")

    page_bg_img = '''
<style>
body {
background-image: url("https://raw.githubusercontent.com/lmebif/scouting/main/bif-fans_meinert.jpg");
background-size: cover;
}
</style>
'''
    #inverted blue https://raw.githubusercontent.com/lmebif/scouting/main/image.png
    #blue https://raw.githubusercontent.com/lmebif/scouting/main/bif-scoutin_bgimg_2.jpg
    #grey box blue https://raw.githubusercontent.com/lmebif/scouting/main/bif-scoutin_bgimg_1.jpg
    #grey box all the way through https://raw.githubusercontent.com/lmebif/scouting/main/bif-scoutin_bg-img.jpg
    #very white https://raw.githubusercontent.com/lmebif/scouting/main/bif-fans_meinert.jpg
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title("BIF Scouting")

    def get_player_dropdown():
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_BI')
        q = pd.read_sql_query(
            "select * from streamlit_player_search",
            conn
            )
        player_dropdown = pd.DataFrame(q)
        return player_dropdown

    @st.cache(allow_output_mutation=True)
    def get_player_data(player_season_ID):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_BI')
        s1 = "'"
        q = "select * from Player_and_Averages_Info where player_season_ID="
        query = q + s1 + player_season_ID[0] + s1
        q1 = pd.read_sql_query(
        query,
        conn
        )
        
        player_info = pd.DataFrame(q1)
        return player_info

    @st.cache(allow_output_mutation=True)
    def get_player_career_data(player_ID):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_BI')

        s1 = "'"
        q = "select * from streamlit_player_career where playerId="
        query = q + s1 + player_ID + s1
        q1 = pd.read_sql_query(
        query,
        conn
        )
        
        player_career_info = (pd.DataFrame(q1)).sort_values(by=['startDate'],ascending=False)
        return player_career_info

    def get_player_contract(player_ID):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_Raw')

        s1 = "'"
        q = "SELECT max([contractExpiry]) as contractExpiry FROM [Scouting_Raw].[dbo].[Wyscout_Player_Contract_Info] where playerId ="
        query = q + s1 + player_ID + s1
        q1 = pd.read_sql_query(
        query,
        conn
        )
        
        #player_career_info = (pd.DataFrame(q1)).sort_values(by=['startDate'],ascending=False)
        contract_info = pd.DataFrame(q1)
        return contract_info

    def construct_abbreviator():
        skills = ['air_duels_won_P90',
            'att_air_duels_won_P90',
            'box_actions_P90',
            'crosses_P90',
            'def_air_duels_won_P90',
            'flat_center_passes_P90',
            'headers_P90',
            'mid_air_duels_won_P90',
            'opp_third_actions_P90',
            'opp_third_involvment',
            'passes_into_last_third_P90',
            'percentage_air_duels',
            'percentage_defensive_duels',
            'percentage_offensive_duels',
            'percentage_offensive_duels_opp_half',
            'percentage_passes_to_last_third',
            'percentage_passing',
            'pos_adj_clearances_P90',
            'pos_adj_interceptions_P90',
            'pos_adj_looseballs_P90',
            'pos_adj_tackles_P90',
            'pos_adj_xg_P90',
            'progressive_passes_P90',
            'ratio_through_balls',
            'shots_P90',
            'succ_box_passes_P90',
            'through_balls_P90',
            'xa_P90',
            'xa_sec_P90',
            'xa_ter_P90',
            'xb_P90',
            'xg_P90',
            'xg_shot']
            
        abb = ['Air Duels Won',
            'Off. Air Duels Won',
            'Box Actions',
            'Crosses',
            'Def. Air Duels Won',
            'Flat Center Passes',
            'xG from Headers',
            'Mid Air Duels Won',
            'Opp. Third Actions',
            'Opp. Third Involvement',
            'Passes (in)to Last Third',
            'Air Duels Won %',
            'Def. Duels Won %',
            'Off. Duels Won %',
            'Off. Duels Won in Opp. Half %',
            'Passes to Last Third %',
            'Passing %',
            'Clearances (PA)',
            'Interceptions (PA)',
            'Looseballs (PA)',
            'Tackles (PA)',
            'xG (PA)',
            'Progressive Passes',
            'Ratio Through Balls',
            'Shots',
            'Succ. Box Passes',
            'Through Balls',
            'xA',
            'xA Secondary',
            'xA Tertiary',
            'xB',
            'xG',
            'xG per Shot']

        skill_d = dict(zip(skills,abb))

        return skill_d

    skill_dict = construct_abbreviator()

    def get_abbreviation(skill,skill_d = skill_dict):
        return skill_d[skill]

    def construct_sorter():
        skills = [
        'percentage_defensive_duels',
        'def_air_duels_won_P90',
        'air_duels_won_P90',
        'mid_air_duels_won_P90',
        'percentage_air_duels',
        'percentage_offensive_duels',
        'percentage_offensive_duels_opp_half',
        'att_air_duels_won_P90',
        'percentage_passing',
        'passes_into_last_third_P90',
        'percentage_passes_to_last_third',
        'ratio_through_balls',
        'crosses_P90',
        'succ_box_passes_P90',
        'xa_ter_P90',
        'xa_sec_P90',
        'xa_P90',
        'box_actions_P90',
        'opp_third_actions_P90',
        'opp_third_involvment',
        'shots_P90',
        'xg_shot',
        'xg_P90',
        'pos_adj_xg_P90',
        'headers_P90',
        'progressive_passes_P90',
        'through_balls_P90',
        'flat_center_passes_P90',
        'xb_P90',
        'pos_adj_clearances_P90',
        'pos_adj_interceptions_P90',
        'pos_adj_looseballs_P90',
        'pos_adj_tackles_P90'
        ]

        order = [i for i in range(len(skills))]
        sort_d = dict(zip(skills,order))
        
        
        return sort_d

    sorter = construct_sorter()

    def get_sort(skill, sorter = sorter):
        return sorter[skill]

    def get_plot_data(player_season_ID,selected_radar):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_BI')
        
        s1 = "'"
        q = "select * from Radar_All_Averages where player_season_ID="
        query = q + s1 + player_season_ID[0] + s1
        q1 = pd.read_sql_query(
        query,
        conn
        )
        
        q = "select * from radar_skill_filter where Radar_Group="
        query = q + s1 + selected_radar + s1
        
        q2 = pd.read_sql_query(
        query,
        conn
        )

        player_radar_data = pd.DataFrame(q1)
        skill_filter = pd.DataFrame(q2)

        plot_data = player_radar_data[player_radar_data['skill'].isin(skill_filter['Skill'])]
        
        plot_data['sort'] = plot_data['skill']

        plot_data['sort'] = plot_data['sort'].apply(lambda x: get_sort(skill=x))

        plot_data['skill'] = plot_data['skill'].apply(lambda x: get_abbreviation(skill=x))

        plot_data = plot_data.sort_values(by=['sort'])

        return plot_data   
    
    def get_percentile_filter():
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_BI')

        q = "select * from radar_percentile_filter"
        q3 = pd.read_sql_query(q,conn)
        percentile_filter = pd.DataFrame(q3)

        return percentile_filter

    def get_nationality(passportID):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting')
        
        pID = str(passportID)

        s1 = "'"
        q = "select name from Wyscout_Areas where areaId="
        query = q + s1 + str(passportID) + s1

        q4 = pd.read_sql_query(query,conn)
        nationality = pd.DataFrame(q4)
        return nationality

    def get_player_img(playerID):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_Raw')

        s1 = "'"
        q = "select imageDataURL from Wyscout_Players_Image where playerId="
        query = q + s1 + str(playerID) + s1

        q5 = pd.read_sql_query(query, conn)
        url = pd.DataFrame(q5)
        if url.empty:
            url = "https://tmssl.akamaized.net/images/portrait/header/default.jpg?lm=1455618221"
        else:
            url = url.values.flatten().tolist()[0]
        return url

    def player_pos_plot(figureName):
        f1 = plt.figure(figureName,figsize = (6,3))
        ax1 = plt.subplot(111)
        plt.axis('off')
        img = plt.imread("S:/Reports/Images/Pitches/bane_standing.png")
        ax1.imshow(img)
        
        
        ax1.annotate('', xy=(-0.0125, 0), xycoords='axes fraction', 
            xytext=(-0.0125, 1), arrowprops=dict(arrowstyle="<-", color='black'))
        return f1

    def player_radar_plot(figureName):
        radar = plt.figure("radar",figsize = (12,8))
        #radar.patch.set_facecolor('#e3e3e3')
        radar.patch.set_facecolor('None')
        ax1 = plt.subplot(111)

        #plt.yticks([0.25,0.50,0.75,1], color = "None", size=10)
        #plt.ylim(0,1)
        #lt.tick_params(axis="x",direction='out',pad = 50)
        return radar

    def plot_player_radar(figureName, categories,values):
        a = plt.figure(figureName)
        
        N = len(categories)
        values += values[:1]
            
        ticks = [n / float(N)*2* pi for n in range(N)]
        ticks += ticks[:1]
            
        plt.polar(ticks, values, marker = '.',)
        plt.fill(ticks, values, alpha = 0.3)
        plt.xticks(ticks[:-1], categories)
        #a.patch.set_facecolor('None')

        return a

    def plot_player_pos(figureName, player):
        a = plt.figure(figureName)
        x,y = 1338, 2067
        
        position_d = {'WM':(.75*x,1/2*y),'LWB':(.0725*x,.55*y),
        'DM':(.5*x,.6*y),'LM':(.25*x,.5*y),'GK':(.5*x,.975*y),
        'CM':(.5*x,.5*y),'RM':(.75*x,.5*y),'LW':(.2*x,.35*y),
        'RWB':(.925*x,.55*y),'LB':(.125*x,.65*y),'RB':(.875*x,.65*y),
        'RW':(.8*x,.35*y),'LCB':(.25*x,.75*y),'FW':(.5*x,.25*y),
        'BACK':(600,1100),'RCB':(.75*x,.75*y),'CB':(.5*x,.75*y),
        'AM':(.5*x,.4*y)}

        for index, row in player.iterrows():
            #st.write(row['map_group'], row['scaling'])
            #plt.plot(position_d[position][0],position_d[position][1],'.',markersize=15,alpha=.75)
            plt.plot(position_d[row['map_group']][0],position_d[row['map_group']][1],'.',markersize=30*row['scaling'],alpha = 1,color='y')

        return

    def get_player_pos(player_season_ID):
        conn = pypy.connect(server = 'BIF-SQL02\SQLEXPRESS02', database='Scouting_BI')
        
        s1 = "'"
        q = "select * from streamlit_positions where player_season_ID="
        query = q + s1 + player_season_ID[0] + s1
        q1 = pd.read_sql_query(
        query,
        conn
        )

        s = sum(q1['t_time'].values.tolist())
        scaling = [x/s for x in q1['t_time'].values.tolist()]
        q1['scaling'] = scaling

        q2 = q1[q1['scaling'] > .1]  
        return q2

    radio = st.sidebar.radio("",("Player Profile","Player Comparison","Team Demo"))

    if radio == "Player Profile":
        player_dropdown = get_player_dropdown()

        select_player = st.multiselect('Player', player_dropdown['longID'])

        ra = st.sidebar.checkbox('Player Radar')

        if ra:
            select_radar = st.selectbox(
                label = 'Radar',
                options = ['back','center_back','back','wing_back',
                'defensive_midfielder','box_to_box_player','wing',
                'attacking_midfielder','forward'],
                )

        if select_player:
            n = len(select_player)
            x = ['x'*i for i in range(n)]
            columns = st.beta_columns(n)

            for i,player_longID in enumerate(select_player):
                
                playerseason_ID = player_dropdown[(player_dropdown['longID']== player_longID)]['player_season_ID'].tolist()
                player_info = get_player_data(playerseason_ID)
                player = player_info.values.flatten().tolist()

                if 'Average' in player_longID:
                    url = "https://raw.githubusercontent.com/lmebif/scouting/main/default.jpg"
                    
                    s = str(player_longID.split(',')[1])



                    columns[i].image(image=url, width = 200)
                    l = (player[8] + ' ' + player[9] + 
                    '\n' + s[1:] + '\n' + 'Age ' + str(player[12]) +  '\n' + str(player[10]) 
                    + ' cm' +  '\n' + str(player[11]) + ' kg' +  '\n' + player[3]
                     +  '\n' + str(int(player[13])) + ' minutes'+ '\n' + 
                    'Position: ' + str(player[16]) + '\n' + 'Foot: ' + player[14])
                
                    columns[i].text(l)
                    continue
                
                curr = columns[i]
                figureName = 'radar' + str(i)

                a = player_radar_plot(figureName)

                pos = player_pos_plot(player_longID)

                #legend = pos.legend(loc='upper center', shadow=True, fontsize='x-large')
                nationality = get_nationality(int(player[15])).values.flatten().tolist()[0]


                url = get_player_img(player[2])
                
                columns[i].image(image=url, width = 250)
                l = (player[8] + ' ' + player[9] +  '\n' + nationality + 
                '\n' + 'Age ' + str(player[12]) +  '\n' + str(player[10]) 
                + ' cm' +  '\n' + str(player[11]) + ' kg' +  '\n' + player[3]
                 +  '\n' + str(int(player[13])) + ' minutes'+ '\n' + 
                'Position: ' + str(player[16]) + '\n' + 'Foot: ' + player[14])
                
                columns[i].text(l)

                player_pos = get_player_pos(playerseason_ID)
                curr = plot_player_pos(player_longID, player=player_pos)
            
                #pos.legend(select_player, loc = 'upper right',bbox_to_anchor=(1, 1.30),fontsize = 'large')
                columns[i].pyplot(pos)
                if ra:

                    df = get_plot_data(playerseason_ID, select_radar)
                    
                    
                    legend = a.legend(loc='upper center', shadow=True, fontsize='x-large')

                    categories = df['skill'].tolist()
                    values = df['value'].tolist()
                    b = plot_player_radar(figureName=figureName,categories=categories,values=values)

                    a.legend(list(select_player), loc = 'upper right',bbox_to_anchor=(1, 1.30),fontsize = 'large')
                    plt.yticks([0.25,0.50,0.75,1], color = "None", size=10)
                    plt.ylim(0,1)
                    plt.tick_params(axis="x",direction='out',pad = 75)
                    b.patch.set_facecolor('None')

                    columns[i].pyplot(b)


    elif radio =="Player Comparison":
        player_dropdown = get_player_dropdown()
        
        #player_dropdown = player_dropdown[~player_dropdown['longID'].str.contains("Average")]

        select_player = st.multiselect('Player', player_dropdown['longID'])

        if select_player:
            colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b',
            '#e377c2','#7f7f7f','#bcbd22','#17becf']
            
            select_radar = st.selectbox(
                label = 'Radar',
                options = ['back','center_back','wing_back','defensive_midfielder','box_to_box_player','wing','attacking_midfielder','forward'],
                )

            pc = st.sidebar.checkbox('Player Career')
            #ppos = st.sidebar.checkbox('Player Position')
            org_stats = st.sidebar.checkbox('Original Stats')   
            
            new = []

            radar = player_radar_plot("radar")
            #legend = radar.legend(loc='upper center', shadow=True, fontsize='x-large')

            names = []
            long_to_short = {}

            for player_longID in select_player:
                playerseason_ID = player_dropdown[(player_dropdown['longID']== player_longID)]['player_season_ID'].tolist()
                player = get_player_data(playerseason_ID)
                T_player = player.T
                
                player = player.values.flatten().tolist()
                df = get_plot_data(playerseason_ID, select_radar)

                name = [player_longID.split(',')[0]]
                short_name = name[0].split(' ')[0] + ' ' + name[0].split(' ')[-1][:1] + '.'
                names.append(player_longID)

                playerID = playerseason_ID[0].split(',')[0]
                c = get_player_contract(playerID).values.tolist()[0][0]

                def color_sidebar(val,colors=colors):
                    col = [colors[i] for i in range(len(names))]

                    color_map = dict(zip(names,col))

                    color = color_map[val] if val in color_map.keys() else 'black'

                    return f'color: {color}'
                
                if 'Average' in player_longID:
                    percentile_filter = get_percentile_filter()

                    choices = {
                    'percentile_25':'Bottom 25%',
                    'percentile_50':'Median',
                    'average_value':'Average',
                    'percentile_75':'Top 25%',
                    'percentile_100':'Top 1%'}

                    def format_func(option):
                        return choices[option]

                    option = st.selectbox("Select Percentile", options=list(choices.keys()), format_func=format_func,index=2)

                    df = df[df['percentile_placeholder'] == option]

                    
                    url = "https://tmssl.akamaized.net/images/portrait/header/default.jpg?lm=1455618221"
                    st.sidebar.image(image=url,width = 125)

                    left, right = st.sidebar.beta_columns(2)
                    l = player[8] + ' ' + player[9] + '\n' + player[5] + '\n' + 'Age ' + str(player[12]) +  '\n' + str(player[10]) + ' cm' +  '\n' + str(player[11]) + ' kg' +  '\n'
                    r = r = player[3] +  '\n' + str(int(player[13])) + ' minutes'+ '\n' + 'Position: ' + str(player[16] + '\n' + 'Foot: ' + player[14])
                    if c:
                        r = player[3] +  '\n' + str(int(player[13])) + ' minutes'+ '\n' + 'Position: ' + str(player[16] + '\n' + 'Foot: ' + player[14] + '\n' + 'Contract Expires:' + '\n' + c)
                    left.text(l)
                    right.text(r)

                else:
                    nationality = get_nationality(int(player[15])).values.flatten().tolist()[0]
                        
                    url = get_player_img(player[2])
                    st.sidebar.image(image=url,width = 150)
                    
                    rows = ['longID']
                    T_player = T_player.loc[rows,]
                    
                    T_player = T_player.reset_index()[[0]]
                    T_player.columns = ['']
                    T_player.index = ['']

                    p = T_player.style.applymap(color_sidebar).hide_index()
                    st.sidebar.table(p)
                    left, right = st.sidebar.beta_columns(2)
                    l = short_name +  '\n' + nationality + '\n' + 'Age ' + str(player[12]) +  '\n' + str(player[10]) + ' cm' +  '\n' + str(player[11]) + ' kg' +  '\n' + '\n' + 'Contract Expires'
                    r = player[3] +  '\n' + str(int(player[13])) + ' minutes'+ '\n' + 'Position: ' + str(player[16] + '\n' + 'Foot: ' + player[14] +  '\n' + '\n' + '\n' + "Unknown")
                    if c:
                        r = player[3] +  '\n' + str(int(player[13])) + ' minutes'+ '\n' + 'Position: ' + str(player[16] + '\n' + 'Foot: ' + player[14] +  '\n' + '\n' + '\n' + c)
                    left.text(l)
                    right.text(r)

                categories = df['skill'].tolist()
                values = df['value'].tolist()
                #st.write(categories,values)
                plot_player_radar(figureName="radar",categories=categories,values=values)

                if pc:
                    if 'Average' in short_name:
                        continue
                    st.write(short_name)
                    player_career = get_player_career_data(playerID)
                    pl = player_career[['compName','teamName','seasonName','apps','totalMinutes']]
                    #pl = pl.groupby(by=['seasonName','teamName'])
                    st.table(pl)


                if org_stats:
                    df = df[['skill','org_stats']]
                    df = df.round(2)
                    df['org_stats'] = df['org_stats'].astype("string")
                    
                    x = ["Full Name", player_longID]
                    
                    df = df.reset_index()
                    df = df[['skill','org_stats']]
                    df.loc[-1] = df.loc[0]
                    df.loc[0] = x
                    df.set_index('skill', inplace=True)
     
                    new.append(df) #

                   

                if len(select_player) and org_stats:
                    n = pd.concat(new, axis = 1)
                    
                    h = [' '*i for i in range(1,len(n.columns)+1)]
                    n.columns = h

                    def color_names(val,colors=colors):
                        col = [colors[i] for i in range(len(n.columns))]

                        color_map = dict(zip(names,col))

                        color = color_map[val] if val in color_map.keys() else 'black'

                        return f'color: {color}'

            #radar.legend(list(select_player), loc = 'upper right',bbox_to_anchor=(1, 1.30),fontsize = 'large')
            plt.yticks([0.25,0.50,0.75,1], color = "None", size=10)
            plt.ylim(0,1)
            plt.tick_params(axis="x",direction='out',pad = 75)
            st.pyplot(radar)

            if org_stats:
                n = n.style.applymap(color_names)
                st.table(n)



    else:# radio == "Team Demo":
        st.write('In Progess...')