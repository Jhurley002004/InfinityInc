# import sqlite3 to build database tables
import sqlite3

#Create sqlite file
conn = sqlite3.connect('screen_sommelier.db')

# Create cursor to run SQL commands
cur = conn.cursor()

'''
Create table for users. Can only run this command once. Running this command more than once 
will result in error code. Tables can only be created once
'''
# cur.execute("""CREATE TABLE userAccount( 
#             ID integer, 
#             userName text, 
#             userEmail text
#             )""")


'''
Create table for movies. Can only run this command once. Running this command more than once 
will result in error code. Tables can only be created once
'''
# cur.execute("""CREATE TABLE movies(
#             ID integer
#             Title text
#             LeadActor text
#             SupportingActor text   
#             Genre text
#             Rated text
#             ReleaseYear text
#             Streaming text
#             RunTime text
#             Director text
#             Writer text
#             Language text
#             Country text
#             UserRating integer
#              )""")


#cur.execute('DROP TABLE movies')


# Commits changes to the database
conn.commit()

# Closes connection to the database
conn.close()
