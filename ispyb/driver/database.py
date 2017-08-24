from __future__ import division, absolute_import
import ConfigParser
import ispyb.api.main
import ispyb.exception
import mysql.connector

class ISPyBDatabaseDriver(ispyb.api.main.API):
  '''This driver connects directly to an ISPyB MySQL/MariaDB database.
  '''

  def __init__(self, host=None, port=None, database=None,
               username=None, password=None, config_file=None):
    if config_file:
      cfgparser = ConfigParser.ConfigParser(allow_no_value=True)
      if not cfgparser.read(config_file):
        raise RuntimeError('Could not read from configuration file %s' %
                           config_file)
      if not host: host = cfgparser.get('ispyb', 'host')
      if not port: port = cfgparser.get('ispyb', 'port')
      if not database: database = cfgparser.get('ispyb', 'database')
      if not username: username = cfgparser.get('ispyb', 'username')
      if not password: password = cfgparser.get('ispyb', 'password')
    if not port: port = 3306

    self._db_conndata = { 'host': host, 'port': port, 'user': username,
                          'password': password, 'database': database }
    self._db = mysql.connector.connect(**self._db_conndata)

    class context_cursor(object):
      '''Context manager for a mysql.connector cursor with two differences
         to a regular cursor: By default results are returned as a dictionary,
         and a new .run() function is an alias to .execute which accepts query
         parameters as function parameters rather than a list.'''
      def __init__(cc, **parameters):
        if 'dictionary' not in parameters:
          parameters['dictionary'] = True
        cc.cursorparams = parameters
      def __enter__(cc):
        cc.cursor = self._db.cursor(**cc.cursorparams)
        def flat_execute(stmt, *parameters):
          cc.cursor.execute(stmt, parameters)
        setattr(cc.cursor, 'run', flat_execute)
        return cc.cursor
      def __exit__(cc, *args):
        cc.cursor.close()
    self._db_cc = context_cursor

  def _db_call(self, query, *parameters):
    cursor = self._dbcursor()
    cursor.execute(query, parameters)
    return cursor

  def get_reprocessing_id(self, reprocessing_id):
    with self._db_cc() as cursor:
      cursor.run("SELECT * "
                 "FROM Reprocessing "
                 "WHERE reprocessingId = %s;", reprocessing_id)
      result = cursor.fetchone()
    if result:
      return result
    raise ispyb.exception.ISPyBNoResultException()
