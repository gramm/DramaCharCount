


# DramaCharCount
DramaCharCount (DCC) is a set of Python scripts that aims to count the occurrence of each characters and words in Japanese drama subtitle files, and generate some statistics on their use. In particular, it generates a tongue-in-cheek "Japanese Drama Proficiency Test" list that groups the characters or words in a way similar to the jōyō kanji or unofficial JLPT lists.
In addition, the data is updated to a SQL and used on [jdramastuff.xyz](http://jdramastuff.xyz) to allow browsing the statistics for a particular drama. The source for the website is also contained in this repository but is not required to run the scripts (note that a SQL server is however required, see the Prerequisite chapter).

### Output
The output of DCC is available in [data_kanji_raw.csv](https://github.com/gramm/DramaCharCount/blob/master/web/public_html/data_kanji_raw.csv). The columns are:
 - kanji	
 The kanji itself :o)
 - count	
The number of occurrences between all subtitle files.
 - freq	
The occurrence frequency i.e. count for this kanji divided by total kanji count (not total character count i.e. does not include hiragana for example).
 - cumul_freq	
The cumulative frequency. For example a value of 50% means that the number of occurrences of all kanji up to the current kanji represent 50% of every kanji in every dramas.
 - drama_freq	
The frequency of appearance of this kanji across dramas. For example a value of 30% means that this kanji appears in 30% of all dramas (and is never used in the other 70% of dramas).
 - episode_freq	
The frequency of appearance of this kanji across episodes. For example a value of 30% means that this kanji appears in 30% of all episodes (and is never used in the other 70% of episodes).
 - jdpt	
The JDPT level for this kanji. The JDPT is defined using the cumulative frequency as follows:


Level|Cumulative frequency|Number of kanji in this level
|--|--|--|
JDPT 5:|50%|143 kanji
JDPT 4:|75%|281 kanji
JDPT 3:|90%|435 kanji
JDPT 2:|95%|323 kanji
JDPT 1:|98%|391 kanji
JDPT 0:|99%|266 kanji
Number of JDPT kanji:||1839 kanji
Not in JDPT:|100%|2173 kanji
 - jdpt_pos	
The position as JDPT kanji i.e. the position when sorted by count.
 - jouyou	
The jouyou level.
 - jouyou_pos
The jouyou position i.e. the position when sorted by jouyou level then by count within each level.
### Upcoming changes:
Development done in sprints. Please refer to https://github.com/gramm/DramaCharCount/projects/1 to see what is planned. Feel free to mail me at [info@jdramastuff.xyz](mailto:info@jdramastuff.xyz) if you have any questions.


# Usage
### Prerequisite

 - DCC requires a MySQL server to work. I recommend using [XAMPP](https://www.apachefriends.org/index.html) for local MySQL servers.
 - DCC requires a MySQL database to work. The name of the database does not matter.

### Configuration
DCC can be configured in two ways:
- Either by editing settings.py, then calling the scripts without arguments, for example

	    connection_info = dict(
        host="localhost",  
        database="db_charcount",  
        user="admin",  
        password="adminpw"   )   
        subtitles_path = "C:/path/to/subtitles/"



- Or by passing all arguments as argument to the script, for example

	    DramaCharCount.py --host=localhost  --user=admin --password=adminpw --database=my_sql_database --path=C:/path/to/subtitles/
    
	

Other configuration options are all contained in settings.py and should be relatively straightforward:

     # Absolute path to the directory containing all subtitle files
     subtitles_path = "C:/Users/Max/Documents/_tmp/all_drama/"
     
     # Enable to print SQL requests in the console
     print_sql = False
     
     # Enable to profile execution time of scripts
     enable_profiler = False
     
     # Path to CSV dump (used in JdcCsvGen.py)
     csv_path_kanji = "../web/public_html/data_kanji_raw.csv"

### Subtitle folder structure
DCC will assume that each subfolder under the subtitles_path folder represents one drama i.e. the name of the subfolder will be used as drama name. All nested files in a given subfolder will be considered as a subtitle file for this drama, with one file assumed to correspond to one episode of the drama.
### CleanSubtitles
DCC contains a script "CleanSubtitles.py" which can be used to remove all lines that do not contain any "readable" characters i.e. all non-text lines in a standard SRT file. This is done on all files in all nested subfolders.
Be aware that no backup of the files is created.

### How to generate the JDTP from scratch
The steps are as follow:
 - Configure Settings.py
 - Create the drama table by executing JdsDramaHandler
 - Load all subtitle lines in the line table by executing JdsLineHandler
 - Count all characters by executing JdsCharHandler. Note that this script will mark a drama as "processed"  (drama[kanji_ok]=1) and will skip processed dramas on execution. It is therefore safe to interrupt the script to continue executing it later, or to execute it again if for example the MySQL connection failed. Clearing the "processed" state can be done by dropping all character info via  jds_char_handler.reset()
 - Optional: build reference of each character to all lines containing this character by executin JdsLineHandler. This script is used to be able to display example usage of characters in a given drama when browed from [jdramastuff.xyz](http://jdramastuff.xyz). The philosophy is identical to JdsCharHandler i.e. drama[kanji_line_ref_ok] will indicate drama to skip. 
 - Generate statistics by executing JdsInfoHandler
 - Optional: Generate CSV output by execution JdsCsvGen

### Changelog:
##### 1.3.0
 - Compute frequency across dramas
 - Compute frequency across episodes
 - Generate JDPT base on cumulative frequency
##### 1.2.0
 - Improve runtime of char count
 - Separate char count and line to char ref
 - Add CSV generator for raw kanji info
 - Add computation of frequency and cumulative frequency
##### 1.1.0
 - Fix all PyCharm warnings
 - Greatly improve help
 - Verify generation from scratch
 - Support settings.py to configure connection info, subtitle path
 
##### 1.0.0

 - Counting of kanji occurences
 - Generation of JDPT levels based on number of kanji in JLPT levels
 - Computing of relative position within jōyō, JLPT, JDPT
 - Computing distance between JLPT and JDPT

