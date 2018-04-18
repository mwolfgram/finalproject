import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import random


def process_command():   #add a param in later -- command!!
    DB_NAME = 'mobile.db'
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    query = "SELECT * FROM mobiledata"   #mobile is the same name as mobile.db -- be careful here!!
    cur.execute(query)

    command = ''
    while command.lower() != 'exit':
        command = input('pls say bar or scatter: ')
    #sql command assembly, put in related plotly requirements
    ######################
    #put some if statements here, name everything the same thing so it can be passed through
    #what to put for help command?
        try:
            if 'screen size ' in command:
                screen_sql = '`screen size`'
                avg_master_piece = screen_sql
                master_piece = screen_sql

                if 'scatter' in command:
                    title_from_input = 'scatterplot of screen sizes'
                    filename_bar = 'screen-bar'
                if 'bar' in command:
                    title_from_input = 'bar chart of screen sizes'
                    filename_scatter = 'screen-scatter'

                range_graph = [0, 15]

            if 'front cam ' in command:
                fcam_sql = '`front camera (megapixels)`'
                avg_master_piece = fcam_sql
                master_piece = fcam_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of front camera sizes'
                    filename_bar = 'fcam-bar'
                if 'bar' in command:
                    title_from_input = 'bar chart of front camera sizes'
                    filename_scatter = 'fcam-scatter'

                range_graph = [0, 25]

            if 'rear cam ' in command:
                rcam_sql = '`rear camera (megapixels)`'
                avg_master_piece = rcam_sql
                master_piece = rcam_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of rear camera sizes'
                    filename_bar = 'rcam-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of rear camera sizes'
                    filename_scatter = 'rcam-scatter'

                range_graph = [0, 50]

            if 'processor ' in command:
                mhz_sql = '`processing speed (MHz)`'
                avg_master_piece = mhz_sql
                master_piece = mhz_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of processing speed'
                    filename_bar = 'mhz-bar'
                if 'bar' in command:
                    title_from_input = 'bar chart of processing speed'
                    filename_scatter = 'mhz-scatter'

                range_graph = [0, 4000]

            if 'ram ' in command:
                ram_sql = '`ram size (gb)`'
                avg_master_piece = ram_sql
                master_piece = ram_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of ram size'
                    filename_bar = 'ram-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of ram size'
                    filename_scatter = 'ram-scatter'

                range_graph = [0, 10]

            if 'storage ' in command:
                storage_sql = '`storage size (gb)`'
                avg_master_piece = storage_sql
                master_piece = storage_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of storage sizes'
                    filename_bar = 'storage-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of storage sizes'
                    filename_scatter = 'storage-scatter'

                range_graph = [0, 300]

            if 'battery ' in command:
                batt_sql = '`battery size (mAh)`'
                avg_master_piece = batt_sql
                master_piece = batt_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of battery sizes'
                    filename_bar = 'battery-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of battery sizes'
                    filename_scatter = 'storage-scatter'

                range_graph = [0, 15000]

            if 'pixel density ' in command:
                ppi_sql = '`pixel density (ppi)`'
                avg_master_piece = ppi_sql
                master_piece = ppi_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of pixel density'
                    filename_bar = 'ppi-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of pixel density'
                    filename_scatter = 'ppi-scatter'

                range_graph = [0, 1000]

            if 'screen-body ' in command:
                sbr_sql = '`screen-body ratio`'
                avg_master_piece = sbr_sql
                master_piece = sbr_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of screen-body ratio'
                    filename_bar = 'sbr-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of screen-body ratio'
                    filename_scatter = 'sbr-scatter'

                range_graph = [0, 100]

            if 'price ' in command:
                price_sql = 'price'
                avg_master_piece = price_sql
                master_piece = price_sql

                if 'scatter ' in command:
                    title_from_input = 'scatterplot of prices'
                    filename_bar = 'price-bar'
                if 'bar ' in command:
                    title_from_input = 'bar chart of prices'
                    filename_scatter = 'price-scatter'

                range_graph = [0, 1500]

            if 'brand ' in command:
                master_piece = 'AVG({})'.format(avg_master_piece)
                mobiledata_format = 'mobiledata.brand'
                group_by_opt = 'GROUP BY mobiledata.brand'
                title_from_input += ' by average per brand'
                #if the last item of command is in the brand mapping dictionary, then add it to the sql statement
                #how to handle user asking for brand inspiration?
                # if command.split(' ')[-1] in brand_input_dict.keys():  #format this in later with graph title!!!!!!


            if 'brand ' not in command:
                mobiledata_format = 'mobiledata.model'
                master_piece = avg_master_piece
                group_by_opt = ''

            if command == 'exit':
                print('thanks for stopping by!!')
                break

            basic_sql_amalg ='''
            SELECT {}, {}
                    FROM mobiledata
                    JOIN `foreign keys` as f
                    ON mobiledata.brandId = f.Id
                    {}
                    ORDER BY {} DESC
            '''.format(mobiledata_format, master_piece, group_by_opt, master_piece)

            # print('-------------------------------------------------------')
            # print(basic_sql_amalg)
            # print(title_from_input, range_graph)
            # print('-------------------------------------------------------')

            strphone=str(basic_sql_amalg)
            cur.execute(strphone)
            plotlytuplist = []
            for row in cur:
                try:
                    pair = (row[0], (int(row[1])) if int(row[1]) > 5 else round(float(row[1]), 1))  #this may actually stay the same
                    plotlytuplist.append(pair)
                except:
                    if row[1] is not None:
                        pair = (row[0], row[1])  #this may actually stay the same
                        plotlytuplist.append(pair)
                    else:
                        continue

            #print(plotlytuplist)
        except:
            print('your command was not recognized -- please try again!!')
            continue

#---------------------------------------------------------------- making scatterplot ----------------------------------------------------------------
        if 'scatter' in command:
            try:
                trace1=go.Scatter(  #***THIS IS THE SCATTER FOR PIXEL DENSITY BC EVERYTHING IS HUGE***      #.format bar or scatter here?
                    type='scatter', #format here for bar or scatter!
                    x=[x[0] for x in plotlytuplist],  #this will remain the same
                    y=[x[1] for x in plotlytuplist],
                    marker=dict(
                        color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
                        size=10
                    ),
                    line=dict(
                        color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
                        width=4
                    ),
                    mode='markers+lines' #what does this do???
                )
                data=[trace1]
                layout=go.Layout(
                    title="{}".format(title_from_input), #.format the title based on the user input here
                    xaxis=dict(
                        range=len(plotlytuplist)
                    ),
                    yaxis=dict(
                        range=[range_graph[0], range_graph[1]]# change the range depending on what is being shown!
                    )
                )
                fig=go.Figure(data=data, layout=layout)
                py.plot(fig, filename='final-project-plotly')#change filename??
            except:
                print('an error was made while generating your scatterplot')

#---------------------------------------------------------------- making bar graph ----------------------------------------------------------------

        if 'bar' in command:
            try:
                trace2=go.Bar(  #lmao figure out what this does in documentation
                    type='bar',
                    x=[x[0] for x in plotlytuplist],
                    y=[x[1] for x in plotlytuplist],
                    marker=dict(
                        color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
                        line=dict(
                            color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
                            width=1.5
                            )
                    )
                )
                data=[trace2]
                layout=go.Layout(
                    title="{}".format(title_from_input),
                    xaxis = dict(
                        range=len(plotlytuplist)
                    ),
                    yaxis = dict(
                        range=[range_graph[0], range_graph[1]]
                    )
                )
                fig=go.Figure(data=data, layout=layout)
                py.plot(fig, filename='final-project-plotly')
            except:
                print('an error was made while generating your bar graph')



process_command()
