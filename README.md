# DramaCharCount
A simple script to count characters in all JPSubber subtitle files, and upload the result to a mysql database
This is a work in progress, in particular the general design will eventually change.

Example of parameters for DramaCharCount.py
--host=localhost  --user=admin --password=adminpw --database=my_sql_database --path=my_absolute_path_to_subtitles_folder

##DramaCharCount.py
DramaCharCount counts the occurrence of all kanji in all subtitles files in the provided folder. The script assumes each subfolder is one drama, with the drama name being the subfolder name. 
All files (including further nested files) will be assumed as belonging to this drama.
For each kanji, a number of lines (10 in the current implementation) are uploaded to the database to be used as an example for this kanji. The number of lines is shared between all dramas.

##DramaWordCount.py
DramaWordCount is more or less a copy/paste of DramaCharCount slightly modified to count words instead of characters. It is also implemented as class.
The counting of words is made by tokenizing lines & getting the normalized form by using sudachipy


##ResetTables.py
The script ResetTables.py will completely erase the DramaCharCount tables and create them anew. Currently this is required when executing other scripts due to unique keys in the database. 

##CleanSubtitles.py
Warning: in-place editing, no backup is created!
This script will remove all lines that do not contain any "readable" characters i.e. all non-text lines in a standard SRT file. This is done on all files in all nested subfolders.

##web
The website source is provided in the web folder.