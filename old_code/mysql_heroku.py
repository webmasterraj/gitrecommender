import MySQLdb

MYSQL_HOST = 'b0fae3776d22aa:5e93cf20@us-cdbr-iron-east-03.cleardb.net/heroku_a1d48867966bd73'
MYSQL_USER = 'b0fae3776d22aa'
MYSQL_PW = '5e93cf20'
MYSQL_DB = 'gitrecommender'
db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PW, MYSQL_DB)

