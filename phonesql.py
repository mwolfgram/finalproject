def process_command():   #add a param in later -- command!!
    DB_NAME = 'mobile.db'
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    query = "SELECT * FROM mobile"   #mobile is the same name as mobile.db -- be careful here!!
    cur.execute(query)

    #plotly .format test

    test_user_input = input('pls say bar or scatter: ')

#okay i guess make a separate parts of the function with separate configurable sql statments inside of each
    if 'scatter' in test_user_input:
        #this changes what is displayed!!
        basicphone ='''
        SELECT mobile.model, `pixel density (ppi)`
        FROM mobile
    	JOIN `foreign keys`
    	ON `foreign keys`.Id = brandId
        ORDER BY `pixel density (ppi)` DESC
        '''  #put the .format here eventually

        strphone=str(basicphone)
        cur.execute(strphone)
        plotlytuplist = []
        for row in cur:
            pair = (row[0], (int(row[1])) if int(row[1]) > 5 else round(float(row[1]), 1))  #change this depending!!!
            plotlytuplist.append(pair)
        print(plotlytuplist)

        title_based_on_input = 'pixel densities!!'

        range1 = (165, 538)
        range2 = (100, 600)
        height1 = 500
        width1 = 1000
        height2 = 600
        width2 = 1100

        trace1 = go.Scatter(  #***THIS IS THE SCATTER FOR PIXEL DENSITY BC EVERYTHING IS HUGE***      #.format bar or scatter here?
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
        data = [trace1]

        layout = go.Layout(
            title="{}".format(title_based_on_input), #.format the title based on the user input here
            xaxis = dict(
                range=len(plotlytuplist)
            ),
            yaxis = dict(
                range=[range1[0], range1[1]]# change the range depending on what is being shown!
            ),
            height= height1, #as with this
            width=width1 #and this
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename = 'phone-scatter')#change filename??

    if 'bar' in test_user_input:

        # SELECT mobile.brand, AVG(`screensize`)  #put different brand average features in here with .format!!!
        # FROM mobile
        # JOIN `foreign keys` as f
        # ON mobile.brandId = f.Id
        # GROUP BY mobile.brand

        basicphone ='''
        SELECT mobile.brand, AVG(`ram size`)
        FROM mobile
    	JOIN `foreign keys`
    	   ON `foreign keys`.Id = brandId
        GROUP BY mobile.brand
        ORDER BY AVG(`ram size`) DESC
        '''  #put the .format here eventually

        strphone=str(basicphone)
        cur.execute(strphone)
        plotlytuplist = []
        for row in cur:
            pair = (row[0], (int(row[1])) if int(row[1]) > 5 else round(float(row[1]), 1))
            plotlytuplist.append(pair)
        print(plotlytuplist)


        title_based_on_input = 'ram bar chart!!'

        range1 = (0, 10) #proper
        range2 = (1, 12)
        height1 = 700 #proper
        width1 = 1500
        height2 = 600
        width2 = 1100


        trace2 = go.Bar(  #lmao figure out what this does in documentation
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
        data = [trace2]
        layout = go.Layout(
            title="{}".format(title_based_on_input),
            xaxis = dict(
                range=len(plotlytuplist)
            ),
            yaxis = dict(
                range=[range1[0], range1[1]]
            ),
            height= height1,
            width= width1
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename = 'phone-bar')
#process_command()
