
# DramaCharCount
DramaCharCount (DCC) is a set of Python scripts that aims to count the occurrence of each characters and words in Japanese drama subtitle files, and generate some statistics on their use. In particular, it generates a tongue-in-cheek "Japanese Drama Proficiency Test" list that groups the characters or words in a way similar to the jōyō kanji or unofficial JLPT lists.
In addition, the data is updated to a SQL and used on [jdramastuff.xyz](http://jdramastuff.xyz) to allow browsing the statistics for a particular drama. The source for the website is also contained in this repository but is not required to run the scripts (note that a SQL server is however required, see the Prerequisite chapter).

### Versions:

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

### Upcoming changes:
Development done in sprints. Please refer to https://github.com/gramm/DramaCharCount/projects/1 to see what is planned. Feel free to mail me at [info@jdramastuff.xyz](mailto:info@jdramastuff.xyz) if you have any questions.


# Usage
### Prerequisite

 - DCC requires a MySQL server to work. I recommend using [XAMPP](https://www.apachefriends.org/index.html) for local MySQL servers.
 - DCC requires a MySQL database to work. The name of the database does not matter.

### Configuration
DCC can be configured in two ways:
- Either by editing settings.py, then calling the scripts without arguments, for example

    > connection_info = dict(  
    >     host="localhost",  
    >     database="db_charcount",  
    >     user="admin",  
    >     password="adminpw"   )   
    >     subtitles_path = "C:/path/to/subtitles/"

- Or by passing all arguments as argument to the script, for example
  > DramaCharCount.py --host=localhost  --user=admin --password=adminpw --database=my_sql_database --path=C:/path/to/subtitles/

### Subtitle folder structure
DCC will assume that each subfolder under the subtitles_path folder represents one drama i.e. the name of the subfolder will be used as drama name. All nested files in a given subfolder will be considered as a subtitle file for this drama, with one file assumed to correspond to one episode of the drama.
### CleanSubtitles
DCC contains a script "CleanSubtitles.py" which can be used to remove all lines that do not contain any "readable" characters i.e. all non-text lines in a standard SRT file. This is done on all files in all nested subfolders.
Be aware that no backup of the files is created.

### How to generate the JDTP from scratch
The steps are as follow:

 - Create the drama table by executing JdsDramaHandler
 - Load all subtitle lines in the line table by executing JdsLineHandler
 - Count all characters by executing JdsCharHandler. Note that this script will mark a drama as "processed"  (drama[kanji_ok]=1) and will skip processed dramas on execution. It is therefore safe to interrupt the script to continue executing it later, or to execute it again if for example the MySQL connection failed. Clearing the "processed" state can be done by dropping all character info via  jds_char_handler.reset()
 - Generate statistics by executing JdsInfoHandler

