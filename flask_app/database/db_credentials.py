import os

host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")


# For OSU Flip Servers

# host = 'classmysql.engr.oregonstate.edu'      # MUST BE THIS
# user = '<your-cs-340-db-username-here>'       # don't forget the CS_340 prefix
# passwd = '<your-password-here>'               # should only be 4 digits if default
# db = '<name-of-database-on-osu-server>'                                  