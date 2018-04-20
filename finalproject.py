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


def get_data_using_cache(url):
    unique_key = url
    if unique_key not in cache_html_data.keys():
        resp = requests.get(unique_key)
        cache_html_data[unique_key] = resp.text
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(cache_html_data))
        cache_file.close()
    else:
        one = 1
    return cache_html_data[unique_key]

super_master_dict = {}
def get_data_for_model():

        link = 'https://www.phonearena.com/phones/manufacturers'
        page = get_data_using_cache(link)
        soup = BeautifulSoup(page, 'html.parser')

        specific_class = soup.find_all('div', class_ = 's_listing')
        brand_attempt = soup.find_all(class_='ahover')
        for x in brand_attempt:
            brand_text_gather = x.find_all(class_ = 'title')
            brand_text_extract = ([x.text.strip() for x in brand_text_gather])
            brand_text = brand_text_extract[0]
            brand_input_dict[brand_text.lower()] = x['href']

        return brand_input_dict

def fetch_data(test_inp0 = None):
        dict_results = get_data_for_model()

        if test_inp0 is not None:
            new_brand_input_dict = {}
            new_brand_input_dict[test_inp0] = dict_results[test_inp0]
            brand_input_dict = new_brand_input_dict
        else:
            brand_input_dict = dict_results

        for comp in brand_input_dict.keys():

            indivlink = 'https://www.phonearena.com' + brand_input_dict[comp]
            indivpage = get_data_using_cache(indivlink)
            indivsoup = BeautifulSoup(indivpage, 'html.parser')

            phone_model = indivsoup.find_all(class_ = 's_thumb')
            model_dict = {}
            for info in phone_model:
                for x in info:
                    model_dict[x['alt']] = info['href']

            master_dict= {}
            for x in model_dict.keys():
                try:
                    phone_key_name = x
                    phonelink = 'https://www.phonearena.com' + model_dict[x]
                    a_phone = get_data_using_cache(phonelink)
                    phonesoup = BeautifulSoup(a_phone, 'html.parser')
                    phone_info0 = phonesoup.find(class_ = 'bottom-line')
                    phone0list = []
                    for x in phone_info0:
                        try:
                            infostr = (x.text.strip().split('\n'))
                            if infostr != '':
                                phone0list.append(infostr)

                        except:
                            continue

                    phone0list_tuple = (phone0list[0][0].split('"'), phone0list[1][0].split(' '), phone0list[1][1].split(' '), phone0list[2][0], phone0list[2][1])
                    isolateint = str(phone0list_tuple[-1].split(',')[-1])
                    phone0tup = (phone0list_tuple[0][0], phone0list_tuple[1][0], phone0list_tuple[2][0], phone0list_tuple[3], int(isolateint.split('MHz')[0]))

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
                    ramfig = phone1list[0].split(' ')[1]
                    memfig = phone1list[1].split(' ')[1]
                    batfig = phone1list[2].split('\n')[0].split(' ')[1]
                    phone1tup = (ramfig, memfig, batfig)
                    ##########
                    phone_info2 = phonesoup.find(class_ = 'metainfo') #release-date
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
                    phone_info3 = phonesoup.find(class_ = 's_lv_1 field-500') #pixel-density
                    for x in phone_info3:
                        try:
                            pixdensity = (int(x.text.split(' ')[0]))

                        except:
                            continue
                    phone3tup = pixdensity
                    ##########
                    phone_info4 = phonesoup.find(class_ = 's_lv_1 field-552') #screen-body ratio
                    for x in phone_info4:
                        try:
                            screenratio = (float(x.text.split(' ')[0]))
                        except:
                            continue
                    phone4tup = screenratio
                    ##########
                    phone_info5 = phonesoup.find(class_ = 's_lv_1 field-450') #price
                    try:
                        for x in phone_info5:
                            try:
                                price = x.text
                                if '$' in price:
                                    dollar_fig = int(price.split('$')[-1])
                                else:
                                    continue

                            except:
                                continue
                        phone5tup = dollar_fig
                    except:
                        try:
                            phone_info5 = phonesoup.find(class_ = 'price')
                            presplit = phone_info5.text.split('$')[1]
                            postsplit = int(presplit.split(' ')[0])
                            phone5tup = postsplit
                        except:
                            phone5tup =  None

                    tup2345 = (phone2tup, phone3tup, phone4tup, phone5tup)
                    final_phonetup = phone0tup + phone1tup + tup2345
                    master_dict[phone_key_name] = final_phonetup

                except:
                    continue
            super_master_dict[comp] = master_dict

    #------------------------------------------------------------- formation of mobile table -------------------------------------------------------------

        if test_inp0 is None:
            try:
                print('Creating Database...')
                conn = sqlite3.connect('mobile.db')
                cur = conn.cursor()
            except:
                print('an error was encountered')

            statement = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'mobiledata';"
            table_exists = cur.execute(statement).fetchall()[0][0]
            if table_exists == 1:
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
                brand_name = brand
                brand_mapping[brand_name] = id
                accum += 1

                for phone in super_master_dict[brand_name].keys():

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
        else:
            return super_master_dict

def process_command(test_inp = None):

    DB_NAME = 'mobile.db'
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    query = "SELECT * FROM mobiledata"
    cur.execute(query)

    command = str(test_inp.lower()) + ' '

    try:
        if 'screen-size ' in command:
            screen_sql = '`screen size`'
            avg_master_piece = screen_sql
            master_piece = screen_sql

            if 'scatter ' in command:
                title_from_input = 'scatterplot of screen sizes'
                filename_bar = 'screen-bar'
            if 'bar ' in command:
                title_from_input = 'bar chart of screen sizes'
                filename_scatter = 'screen-scatter'

            range_graph = [0, 15]

        if 'front-cam ' in command:
            fcam_sql = '`front camera (megapixels)`'
            avg_master_piece = fcam_sql
            master_piece = fcam_sql

            if 'scatter ' in command:
                title_from_input = 'scatterplot of front camera sizes'
                filename_bar = 'fcam-bar'
            if 'bar ' in command:
                title_from_input = 'bar chart of front camera sizes'
                filename_scatter = 'fcam-scatter'

            range_graph = [0, 25]

        if 'rear-cam ' in command:
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
            if 'bar ' in command:
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

        if 'pixel-density ' in command:
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

        if 'brand ' not in command:
            mobiledata_format = 'mobiledata.model'
            master_piece = avg_master_piece
            group_by_opt = ''

        basic_sql_amalg ='''
        SELECT {}, {}
                FROM mobiledata
                JOIN `foreign keys` as f
                ON mobiledata.brandId = f.Id
                {}
                ORDER BY {} DESC
        '''.format(mobiledata_format, master_piece, group_by_opt, master_piece)

        strphone=str(basic_sql_amalg)
        cur.execute(strphone)
        plotlytuplist = []
        my_objects = []

        class MyEntity:
            def __init__(self, init_tuple):
                self.item0 = init_tuple[0]
                self.item1 = int(init_tuple[1]) if int(init_tuple[1]) > 5 else round(float(init_tuple[1]), 1)

        for row in cur:
            try:
                my_objects.append(MyEntity(row))
            except:
                if row[1] is not None:
                    row = (row[0], row[1])
                    my_objects.append(MyEntity(row))
                else:
                    continue

        for x in my_objects:
            pair = (x.item0, x.item1)
            plotlytuplist.append(pair)

    except:
        print('your command was not recognized -- please try again!!')

    if __name__=="__main__":
#---------------------------------------------------------------- making scatterplot ----------------------------------------------------------------
        if 'scatter ' in command:
            try:
                trace1=go.Scatter(
                    type='scatter',
                    x=[x[0] for x in plotlytuplist],
                    y=[x[1] for x in plotlytuplist],
                    marker=dict(
                        color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
                        size=10
                    ),
                    line=dict(
                        color=['rgb({},{},{})'.format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)) for x in plotlytuplist],
                        width=4
                    ),
                    mode='markers+lines'
                )
                data=[trace1]
                layout=go.Layout(
                    title="{}".format(title_from_input),
                    xaxis=dict(
                        range=len(plotlytuplist)
                    ),
                    yaxis=dict(
                        range=[range_graph[0], range_graph[1]]
                    )
                )
                fig=go.Figure(data=data, layout=layout)
                py.plot(fig, filename='final-project-plotly')
            except:
                print('an error was made while generating your scatterplot')

#---------------------------------------------------------------- making bar graph ----------------------------------------------------------------

        if 'bar ' in command:
            try:
                trace2=go.Bar(
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


    return plotlytuplist

def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive_prompt():
    factors = ['screen-size', 'front-cam', 'rear-cam', 'processor', 'ram', 'storage', 'battery', 'pixel-density', 'screen-body', 'price']
    help_text = load_help_text()

    response = ''
    while response.lower() != 'exit':
        response = input('hi! enter a command, type help for a list of commands, or exit: ')
        below_response = response

        if response.lower() == 'help':
            print(help_text)
            continue

        if response.lower() == 'exit':
            print('bye!')
            break

        DB_NAME = 'mobile.db'
        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
        except Error as e:
            print(e)

        try:
            if 'bar' or 'scatter' in response.lower():
                bool1 = 'bar' in response.lower()
                bool2 = 'scatter' in response.lower()
                tupbool = (bool1, bool2)

                if tupbool != (False, False):

                    if response.lower().split()[1] in factors:
                        try:
                            statement1 = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'mobiledata';"
                            table_exists = cur.execute(statement1).fetchall()[0][0]
                            if table_exists == 1:
                                user_input = input('the information you need is already here! would you like to regenerate it? type "yes" or "no" or "exit": ')

                                if user_input.lower() == 'yes':
                                    print('getting new data -- this will take 5 to 30 minutes')
                                    try:
                                        fetch_data()
                                        process_command(below_response)
                                    except:
                                        print('command not recognized :(')
                                    continue

                                if user_input.lower() == 'no':
                                    try:
                                        print('okay, we will keep using the existing database')
                                        process_command(below_response)
                                        continue
                                    except:
                                        print('command not recognized :(')
                                        continue

                                if user_input.lower() == 'exit':
                                    print('bye!')
                                    break

                            else:
                                print('the table you need does not exist -- it will be generated again! this will take 5 to 30 minutes')
                                fetch_data()
                                process_command(below_response)
                        except:
                            print('please enter a valid command')
                            continue
                    else:
                        print('please enter a valid command')
                        continue
                else:
                    print('please enter a valid command')
                    continue
            else:
                print('please enter a valid command')
                continue
        except:
            print('please enter a valid command')
            continue


if __name__=="__main__":
    interactive_prompt()
