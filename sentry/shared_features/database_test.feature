# Created by cookie.luo at 2020-11-09
Feature:  database test


  Scenario: Execute cassandra sql successfully
    Given a cassandra server test-server
    And a cassandra keyspace test-keyspace
    And a cassandra username cassandra
    And a cassandra password cassandra
    And a sql script
        """
        SELECT * FROM test_table;
        """
    When the cassandra script is executed
    Then the data table at column id is not null
    And the data table at column id contains 34093


  Scenario: Execute cassandra sql file successfully
    Given a cassandra server test-server
    And a cassandra keyspace test-keyspace
    And a cassandra username cassandra
    And a cassandra password cassandra
    And a sql script file testcassandrasql.sql
    When the cassandra script is executed
    Then the data table at column id is not null
    And the data table at column id contains 34093


  Scenario: Execute postgresql sql successfully
    Given a postgresql server test-server
    And a postgresql keyspace test-keyspace
    And a postgresql username postgresql
    And a postgresql password postgresql
    And a sql script
        """
        select * from test_table where id = 1;
        """
    When the postgresql query script is executed
    Then the data table at column id contains 1
    And the data table at column name contains temp_test


  Scenario: Execute postgresql non sql successfully
    Given a postgresql server test_server
    And a postgresql keyspace keyspace
    And a postgresql username username
    And a postgresql password pwd
    And a sql script
        """
        update table set name ='1234' where id = 1;
        """
    When the postgresql non query script is executed


  Scenario: Execute postgresql non sql file successfully
    Given a postgresql server test_server
    And a postgresql keyspace keyspace
    And a postgresql username username
    And a postgresql password pwd
    And a sql script file testpostgresqlsql.sql
    When the postgresql query script is executed
    Then the data table at column id contains 1
    And the data table at column name contains temp_test