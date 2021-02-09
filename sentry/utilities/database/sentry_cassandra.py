from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.query import dict_factory


class Cassandra:
    def __init__(self, server, keyspace, username, password):
        self.keyspace = keyspace
        self.auth_provider = PlainTextAuthProvider(username=username,
                                                   password=password)
        self.cluster = Cluster([server], auth_provider=self.auth_provider)

    def execute_sql(self, sql):
        session = self.cluster.connect(self.keyspace)
        session.row_factory = dict_factory
        return session.execute(sql).current_rows
