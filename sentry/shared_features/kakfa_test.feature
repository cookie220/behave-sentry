# Created by cookie.luo at 2020-10-28
Feature: kafka test
  # Enter feature description here

  Scenario: produce and consumer successfully
    Given a kafka server kafka_server
    And a kafka topic test_topic
    And a kafka event json
          """
            {
              "Event": {
                "Id": "5f9a894741acc0000729659d",
                "Name": "Automation",
                "Group": "Group",
                "OccurredAt": "2020-10-28T07:56:41.578Z"
              }
            }
          """
    When the event is produced
    And consumer start to consume
    Then the kafka json at $.Event.Id is equal to "5f9a894741acc0000729659d"
    Then the kafka json at $.Event.Name is not null



  Scenario: just consumer successfully
    Given a kafka server kafka_server
    And a kafka topic test_topic
    When consumer start to consume
    Then the kafka json at $.Id with Id is saved
    And the kafka json at $.name is equal to "${name}"



  Scenario: consumer multi partition successfully
    Given a kafka server kafka_server
    And a kafka topic test_topic
    When consumer start to consume
    Then the kafka json at $.PhoneNumber is equal to "1265255218"