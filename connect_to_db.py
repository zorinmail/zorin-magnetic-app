import sqlalchemy

# класс со всякой исходной информацией для подключения
class connectionInfo:

    def __init__(self, key):
        """Constructor"""
        self._pg_user = ''
        self._pg_pass = ''
        self._pg_host = ''
        self._pg_port = ''
        self._pg_dbname = ''
        self.connection_string = ''
        self.__set_params(key)

    def __set_params(self, key):
        if key == 'server':
            self._pg_user = 'axtwbbjtiajlqn'
            self._pg_pass = 'b08a23d4e8da8bb01e89b5c02e29fa7b959a3a91be994ac1e7ec0c20fb322615'
            self._pg_host = 'ec2-34-230-231-71.compute-1.amazonaws.com'
            self._pg_port = '5432'
            self._pg_dbname = 'de51bdao4jre75'
        elif key == 'local':
            self._pg_user = 'postgres'
            self._pg_pass = 'admin'
            self._pg_host = 'localhost'
            self._pg_port = '5432'
            self._pg_dbname = ''
        self.connection_string = ('postgresql+psycopg2://' +
                                   self._pg_user + ':' +
                                   self._pg_pass + '@' +
                                   self._pg_host + ':' +
                                   self._pg_port + '/' +
                                   self._pg_dbname)


def create_engine(key):
    conInfo = connectionInfo(key)
    connection_string = conInfo.connection_string
    engine = sqlalchemy.create_engine(connection_string)
    return engine