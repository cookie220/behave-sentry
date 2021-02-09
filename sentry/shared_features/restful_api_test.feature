# Created by Cookie at 2020/12/3
Feature: # get random dog

  Scenario: get random dog
    Given a new request url https://dog.ceo/api/breeds/image/random
    When the request verb is GET
    Then the response json at $.status is equal to "success"
    And the response json at $.message ends with "jpg"

  """
    {
        "message": "https://images.dog.ceo/breeds/pointer-germanlonghair/hans3.jpg",
        "status": "success"
    }
   """