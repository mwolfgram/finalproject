import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import random

brand_input_dict = {}

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    cache_html_data = json.loads(cache_contents)
except:
    cache_html_data = {}

class AtLeastOneClassIsDefined:
    lol = 1234

def get_data_using_cache(url):
    unique_key = url
    if unique_key not in cache_html_data.keys():
        print('this was a new call...')
        resp = requests.get(unique_key)
        cache_html_data[unique_key] = resp.text
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(cache_html_data))
        cache_file.close()
    else:
        print('getting from cache :)')
    return cache_html_data[unique_key]


super_master_dict = {}
def get_data_for_model(): #add (make, model): as params

        #start asking the user to narrow down by phone brand

        link = 'https://www.phonearena.com/phones/manufacturers'
        #print(link)
        page = get_data_using_cache(link)
        soup = BeautifulSoup(page, 'html.parser')
        #print(soup) #this works

        specific_class = soup.find_all('div', class_ = 's_listing')
        brand_attempt = soup.find_all(class_='ahover')
        for x in brand_attempt:
            brand_text_gather = x.find_all(class_ = 'title')
            brand_text_extract = ([x.text.strip() for x in brand_text_gather])
            brand_text = brand_text_extract[0]
            brand_input_dict[brand_text.lower()] = x['href']
        #print(brand_input_dict.keys())

        printStr1 = ""
        numsInRow1 = 1
        for x in brand_input_dict.keys():
            if numsInRow1 % 7 == 0:
                printStr1 += "{0:17}\n".format(x)
                numsInRow1 = 1
            else:
                printStr1 += "{0:17}\t".format(x)
                numsInRow1 += 1
        print(printStr1)

        #then, show them the available models and ask them to pick one to get details on -- make table of all phone from the device after getting the info for it?

        for comp in brand_input_dict.keys():
            indivlink = 'https://www.phonearena.com' + brand_input_dict[comp] #fill this with user input
            #print(indivlink)
            indivpage = get_data_using_cache(indivlink)
            indivsoup = BeautifulSoup(indivpage, 'html.parser')
            #print(soup)

            #all_phone_models = indivsoup.find_all(class_ = 's_listing')
            phone_model = indivsoup.find_all(class_ = 's_thumb')
            model_dict = {}
            for info in phone_model:
                #print(info['href'])
                for x in info:
                    # print('--------')
                    # print(x['alt'], info['href'])
                    model_dict[x['alt']] = info['href']
            #print(model_dict)
            printStr2 = ""
            numsInRow2 = 1
            for x in model_dict.keys():
                if numsInRow2 % 4 == 0:
                    printStr2 += "{0:18}\n".format(x)
                    numsInRow2 = 1
                else:
                    printStr2 += "{0:18}\t".format(x)
                    numsInRow2 += 1
            #print(printStr2)
            #extract info from one phone model (iphone 6s) for now, the cycle through the for loop with each phone from the model

            master_dict= {}

            for x in model_dict.keys():
                try:
                    #print('----------------------')
                    phone_key_name = x
                    #print(x)
                    phonelink = 'https://www.phonearena.com' + model_dict[x] #fill this with user model input, this is the crawling part
                    #print(phonelink)
                    a_phone = get_data_using_cache(phonelink)
                    phonesoup = BeautifulSoup(a_phone, 'html.parser')
                    # print(phonesoup)
                    ##########
                    phone_info0 = phonesoup.find(class_ = 'bottom-line') #screen size, camera mp, chip type
                    phone0list = []
                    for x in phone_info0:
                        try:
                            #print('--------')
                            infostr = (x.text.strip().split('\n'))
                            if infostr != '':
                                phone0list.append(infostr)

                        except:
                            continue

                    phone0list_tuple = (phone0list[0][0].split('"'), phone0list[1][0].split(' '), phone0list[1][1].split(' '), phone0list[2][0], phone0list[2][1])
                    isolateint = str(phone0list_tuple[-1].split(',')[-1])
                    phone0tup = (phone0list_tuple[0][0], phone0list_tuple[1][0], phone0list_tuple[2][0], phone0list_tuple[3], int(isolateint.split('MHz')[0]))
                    #print(phone0tup)

                    ##########
                    phone_info1 = phonesoup.find(class_ = 'morespecs') #RAM, memory, battery
                    phone1list = []
                    for x in phone_info1:
                        try:
                            info1str = x.text
                            if info1str != '':
                                phone1list.append(info1str)

                        except:
                            continue
                    #print(phone1list)
                    ramfig = phone1list[0].split(' ')[1]
                    memfig = phone1list[1].split(' ')[1]
                    batfig = phone1list[2].split('\n')[0].split(' ')[1]
                    phone1tup = (ramfig, memfig, batfig)
                    ##########
                    phone_info2 = phonesoup.find(class_ = 'metainfo') #release date
                    for x in phone_info2:
                        try:
                            if 'Release date:' in x:
                                dropdate = (x.split(':')[-1])

                        except:
                            dropdate = None

                    phone2tup = dropdate
                    if "," not in phone2tup:
                        phone2tup = None
                    ##########
                    phone_info3 = phonesoup.find(class_ = 's_lv_1 field-500') #pixel density
                    for x in phone_info3:
                        try:
                            pixdensity = (int(x.text.split(' ')[0]))

                        except:
                            continue
                    phone3tup = pixdensity
                    ##########
                    phone_info4 = phonesoup.find(class_ = 's_lv_1 field-552') #screen-to-body ratio !!!
                    for x in phone_info4:
                        try:
                            screenratio = (float(x.text.split(' ')[0]))
                        except:
                            continue
                    phone4tup = screenratio
                    ##########
                    phone_info5 = phonesoup.find(class_ = 's_lv_1 field-450') #price attempt
                    try:
                        for x in phone_info5:
                            try:
                                #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                                price = x.text
                                #print(price)
                                # if 'MSRP' in price:
                                #     continue
                                if '$' in price:
                                    dollar_fig = int(price.split('$')[-1])   #wait set the else statement to none if $ isn't in there
                                    #print(dollar_fig)
                                else:
                                    continue

                                #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            except:
                                continue
                        phone5tup = dollar_fig
                    except:
                        try:
                            phone_info5 = phonesoup.find(class_ = 'price') #price attempt
                            presplit = phone_info5.text.split('$')[1]
                            postsplit = int(presplit.split(' ')[0])
                            phone5tup = postsplit
                        except:
                            phone5tup =  None

                    tup2345 = (phone2tup, phone3tup, phone4tup, phone5tup)

                    final_phonetup = phone0tup + phone1tup + tup2345
                    #print(final_phonetup)       #then pair this data to the phone name as well as brand!!!! put this into the db
                    master_dict[phone_key_name] = final_phonetup

                except:
                    continue
            #print(master_dict)
            super_master_dict[comp] = master_dict


        try:
            print('Creating Database...')
            conn = sqlite3.connect('mobile.db')
            cur = conn.cursor()
        except:
            print('an error was encountered')

    #------------------------------------------------------------- formation of mobile table -------------------------------------------------------------

        statement = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'mobiledata';"
        table_exists = cur.execute(statement).fetchall()[0][0]
        if table_exists == 1:
            #user_input = input('this table already exists -- reset it by typing yes to and start fresh?')
            user_input = 'yes'
            if user_input == 'yes':
                statement = '''
                    DROP TABLE IF EXISTS 'mobiledata';
                '''
                cur.execute(statement)
                conn.commit()

                statement = '''
                    CREATE TABLE 'mobiledata' (
                        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                        'brand' TEXT NOT NULL,
                        'brandId' INTEGER NOT NULL,
                        'model' TEXT NOT NULL,
                        'screen size' INTEGER NOT NULL,
                        'rear camera (megapixels)' INTEGER NOT NULL,
                        'front camera (megapixels)' INTEGER NOT NULL,
                        'chip type' TEXT NOT NULL,
                        'processing speed (MHz)' INTEGER NOT NULL,
                        'ram size (gb)' INTEGER,
                        'storage size (gb)' INTEGER,
                        'battery size (mAh)' INTEGER,
                        'release date' TEXT,
                        'pixel density (ppi)' INTEGER,
                        'screen-body ratio' INTEGER,
                        'price' INTEGER
                    );
                '''
                cur.execute(statement)
                conn.commit()

            else:
                return
        else:
            statement = '''
                CREATE TABLE 'mobiledata' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'brand' TEXT NOT NULL,
                    'brandId' INTEGER NOT NULL,
                    'model' TEXT NOT NULL,
                    'screen size' INTEGER NOT NULL,
                    'rear camera (megapixels)' INTEGER NOT NULL,
                    'front camera (megapixels)' INTEGER NOT NULL,
                    'chip type' TEXT NOT NULL,
                    'processing speed (MHz)' INTEGER NOT NULL,
                    'ram size (gb)' INTEGER,
                    'storage size (gb)' INTEGER,
                    'battery size (mAh)' INTEGER,
                    'release date' TEXT,
                    'pixel density (ppi)' INTEGER,
                    'screen-body ratio' INTEGER,
                    'price' INTEGER
                );
            '''
            cur.execute(statement)
            conn.commit()

        brand_mapping = {}
        accum = 1
        for brand in super_master_dict.keys():
            id = accum
            brand_name = brand      #add table here that creates fkey reference table!!
            brand_mapping[brand_name] = id
            accum += 1
            #print(brand_name)

            for phone in super_master_dict[brand_name].keys():
                #print(brand_name, phone, super_master_dict[brand_name][phone]) #fourteen things total! tuple has 11

                zero = None
                one = brand_name
                brand_fkey = brand_mapping[brand_name]
                two =  phone
                three = super_master_dict[brand_name][phone][0]
                four = super_master_dict[brand_name][phone][1]
                five = super_master_dict[brand_name][phone][2]
                six = super_master_dict[brand_name][phone][3]
                seven = super_master_dict[brand_name][phone][4]
                eight = super_master_dict[brand_name][phone][5]
                nine = super_master_dict[brand_name][phone][6]
                ten = super_master_dict[brand_name][phone][7]
                eleven = super_master_dict[brand_name][phone][8]
                twelve = super_master_dict[brand_name][phone][9]
                thirteen = super_master_dict[brand_name][phone][10]
                fourteen = super_master_dict[brand_name][phone][11]

                insertion = (zero, one, brand_fkey, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen)
                statement = 'INSERT OR IGNORE INTO "mobiledata"'
                statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                conn.commit()

        statement1 = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'foreign keys';"
        table_exists = cur.execute(statement1).fetchall()[0][0]
        if table_exists == 1:
            #user_input = input('this table already exists -- reset it by typing yes to and start fresh?')
            user_input = 'yes'
            if user_input == 'yes':
                statement1 = '''
                    DROP TABLE IF EXISTS 'foreign keys';
                '''
                cur.execute(statement1)
                conn.commit()

                statement1 = '''
                    CREATE TABLE 'foreign keys' (
                        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                        'brand' TEXT NOT NULL
                    );
                '''
                cur.execute(statement1)
                conn.commit()

            else:
                return
        else:
            statement1 = '''
                CREATE TABLE 'foreign keys' (
                    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                    'brand' TEXT NOT NULL
                );
            '''

            cur.execute(statement1)
        conn.commit()

        for x in brand_mapping.keys():
            zero_one = None
            one_one = x
            insertion1 = (zero_one, one_one)
            statement1 = 'INSERT OR IGNORE INTO "foreign keys"'
            statement1 += 'VALUES (?, ?)'
            cur.execute(statement1, insertion1)
            conn.commit()


get_data_for_model()


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
#plotly stuff??




#part 2 -- generate two tables that cature the data returned by the phonearena website



#part 3 -- implement interactive setup to take user input and return the data, ask for poltly graphs
    #would you like to generate a grpah of distribution of...


#part 4 -- test cases
