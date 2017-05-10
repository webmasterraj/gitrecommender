import MySQLdb
import os
import sys
import urlparse

def get_db_variables():
    urlparse.uses_netloc.append("mysql")

    try:

        # Check to make sure DATABASES is set in settings.py file.
        # If not default to {}

        if 'DATABASES' not in locals():
            DATABASES = {}

        if 'CLEARDB_DATABASE_URL' in os.environ:
            url = urlparse.urlparse(os.environ['CLEARDB_DATABASE_URL'])

            # Ensure default database exists.
            DATABASES['default'] = DATABASES.get('default', {})

            # Update with environment configuration.
            DATABASES['default'].update({
                'NAME': url.path[1:],
                'USER': url.username,
                'PASSWORD': url.password,
                'HOST': url.hostname,
                'PORT': url.port,
            })
            if url.scheme == 'mysql':
                DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
    except Exception:
        print 'Unexpected error:', sys.exc_info()

    return DATABASES
 

def str_for_mysql(s):
    if isinstance(s, basestring):
        s = s.replace("'", "''")
    # Add any more string formatting steps here
    return s
    

def date_for_mysql(d):
    d = d.strftime("%Y-%m-%d %H:%M")
    # Add any more date formatting steps here
    return d


class DB(object):
  conn = None

  def connect(self):
    db_params = get_db_variables()
    self.conn = MySQLdb.connect(db_params['default']['HOST'], 
                                db_params['default']['USER'], 
                                db_params['default']['PASSWORD'], 
                                db_params['default']['NAME'], 
                                charset='utf8')
    print "DB >> Opened connection to database."

  def query(self, sql):
    try:
      cursor = self.conn.cursor()
      cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      cursor = self.conn.cursor()
      cursor.execute(sql)
    return cursor

  def commit(self):
    try:
      self.conn.commit()
    except (AttributeError, MySQLdb.OperationalError):
      self.connect()
      self.conn.commit()

  def close(self):
    try:
      self.conn.close()
      print "DB >> Closed connection to database."
    except (AttributeError, MySQLdb.OperationalError):
      pass


