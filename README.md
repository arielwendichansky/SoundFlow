# SoundFlow
An analysis of data from Spotrify:

Link to video quickly explaining findings:
https://www.loom.com/share/4f4e292af4c043da9fa950429b79238f?sid=43323473-cf8e-4b00-9386-7e7e8138221f

- Based on Data Provided by Spotify, several analysis were performed with different goals. 
    1. Where are most artists originally from that have music within our dataset?
    2. How did the distribution of musical features change through out the years? 
    3. Is there a trend noticible regarding the release date of tracks? 
    4. Are certain musical features correlated?
    5. What musical features have a high correlation to the number of streams? 5. Can we predict successful songs with high number of streams based on these discovered features?

- The data optained through the Kaggle API, is saved within a PostgreSQL online database, Elephant. We have 4 tables. one with data from 2010 to 2019, another with 2020 to 2023 data, a merged table including all the years and a final table including only the artist name and country of origin.

- For efficiant data processing, best practice and principles,the project is built on OOP. All classes are saved within separate .py files and then imported straight from the Git repo to be called in this notebook. These modules include preprocessing - a class for cleaning the data like droping columns, droping null values, outlier detection and removal, replacement of values, etc. The Managedb class allows to connect to our database, upload and query data. Finally, a plotting class was created that allows the user to interactivly select the type of plot they want displayed, as well as the column names to be displayed. Title and axis labels can also be specified.  
