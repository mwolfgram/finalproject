# finalproject by matthew wolfgram
si 206 w '18


******overview******

my project crawls a website called phonearena (https://www.phonearena.com/phones/manufacturers), then caches HTML containing information regarding specific brands and the phones they’ve designed. After the information is retrieved, a database (mobile.db) is created—it contains a foreign key table that maps phone brands to models, as well as a mobiledata table that contains all devices and their specifications. Once the database is generated, the user is asked to input a specific command to graphically display data of their liking. The supported commands are listed below. 


******instructions/flow******

The initial page that contains the information needed for crawling is https://www.phonearena.com/phones/manufacturers — from there, the individual links of each brand are crawled, and information from the pages of each individual device (i.e. https://www.phonearena.com/phones/OPPO-F7_id10856 ) is scraped. For each phone, information about its **screen size, front camera, rear camera, processor, ram, storage, battery, pixel density, screen-body ratio, and price** are put into the mobile.db database.


******main functions/data structures******

The code is structured around three main functions:
-	fetch_data ():
	  -	caches the request data, and gathers the relevant information from the HTML of each phone on 
		https://www.phonearena.com/phones/manufacturers
	  -	populates dictionary **super_master_dict** that contains a dictionary of each brand, where each dictionary contains a 12-tuple for each phone by that brand. The 12-tuple contains the model, screen size, front camera, rear camera, processor, ram, storage, battery, release date, pixel density, screen-body ratio, and price
	  -	after that, the **database mobile.db** is populated with a mobiledata table containing these values, mapping each phone to its manufacturer via an Id in the foreign keys table 
	  -	fetch_data() **returns super_master_dict** for the test cases 
-	process_command():
	  -	once the mobile.db is created, process_command() makes a connection to the database and constructs a SQL statement depending on the inputted user command it accepts as a parameter. After this statement is executed, the results are passed through the **class MyEntity** that retrieves the information from the SQL output and populates the **plotlytuplist**— this list contains a 2-tuple that holds the name of the device and the specified metric. Each tuple is then graphed as either a bar graph or scatter plot. 
	  -	process_command() **returns plotlytuplist** for the test cases
-	interactive_prompt():
	  -	before the data collection processing is conducted, this function prompts the user to specify which information they would like to see displayed via plotly. It supports all of the commands in the help.txt file (see below).
	  -	If the command is not supported, the user is prompted to enter another 
	  -	If the command is valid, interactive_prompt() calls process_command() and fetch_data() accordingly to generate the proper plotly output

******help.txt/user guide******

  - used to help users make the correct commands 
   
        using this program requires typing a combination of primary, secondary, and tertiary commands.
        a guide to these commands has been provided for you below!

        *THE PROGRAM WILL NOT WORK IF COMMANDS AREN'T TYPED EXACTLY AS SPECIFIED*

        commands available:

        *************************** primary commands ***************************
        bar:
          description: generates a bar graph of the specified metric

        scatter:
          description: generates a bar graph of the specified metric


        ********************** secondary commands (metrics) **********************
        screen-size // generates the graph based on the screen size of all phones

        front-cam // generates the graph based on the sizes of the front camera sensor of all phones

        rear-cam // generates the graph based on the sizes of the rear camera sensor of all phones

        processor // generates the graph based on the processor sizes (in megahertz) of all phones

        ram // generates the graph based on the amount of ram (gb) in all phones

        storage // generates the graph based on the amount of storage (gb) in all phones

        battery // generates the graph based on the battery size of all phones

        pixel-density // generates the graph based on the pixel densities (in pixels per inch) of all phones

        screen-body // generates the graph based on the screen-body ratios of all phones

        price // generates the graph based on the prices of all phones

        ******************** tertiary command (average by brands) ********************
        brand // generates the specified graph by calculating the average value of the specified 
        metric for each brand—the brands and their average values are then displayed 
        
  - these commands must be typed correctly in order to generate the plotly graphs!
  - **WITHOUT THE CACHE, DATA COLLECTION TAKES UPWARDS OF THIRTY MINUTES**
    download the cache to reduce long load times to a few minutes—download it here:
    
    https://drive.google.com/openid=1UDZwmwFXaeOjwHEfFW4RIytvN4Tu8n3r
    
  - data can be gathered without the cache, but at the loss of a significant amount of your precious time on earth 
  - **THE CACHE IS VERY LARGE AND NOT INCLUDED IN THE REPO—IT MUST BE DOWNLOADED FROM GOOGLE DRIVE**
    
    

  
	


