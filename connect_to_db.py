import sqlalchemy

def create_engine():
    pg_user = 'axtwbbjtiajlqn'
    pg_pass = 'b08a23d4e8da8bb01e89b5c02e29fa7b959a3a91be994ac1e7ec0c20fb322615'
    pg_host = 'ec2-34-230-231-71.compute-1.amazonaws.com'
    pg_port = '5432'
    pg_dbname = 'de51bdao4jre75'
    connection_string = 'postgresql+psycopg2://' + pg_user + ':' + pg_pass + '@' + pg_host + ':' + pg_port + '/' + pg_dbname
    engine = sqlalchemy.create_engine(connection_string)
    return engine