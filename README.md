# Restful style api test framework for python


##   How to use it?

```bash
pip3 install behave-sentry 
pip3 install -r requirements.txt
```

## Usage
```python

Feature: Sample Feature
    This is a sample feature that allows you to test that everything is working.
    You can remove it once you start adding your own features, or you can use it
    as a template for your projects.

  Scenario: Add a new book to collection.
        Given a request url http://my.reads/api/books
            And a request json payload
                """
                {
                    "category": "reference",
                    "author": "Nigel Rees",
                    "title": "Sayings of the Century",
                    "price": 8.95,
                    "status": "to-read"
                }
                """
        When the request sends POST
        Then the response status is CREATED
            And the response json matches
                """
                {
                    "title": "BookObject",
                    "type": "object"
                    "properties": {
                        "id": {"type": "number"},
                        "category": {"type": "string"},
                        "author": {"type": "string"},
                        "title": {"type": "string"},
                        "price": {"type": "number"},
                        "status": {"type": "string", "enum": ["to-read", "reading", "read"]}
                    },
                    "required": ["id", "category", "title"]
                }
                """
            And the response json at $.id is equal to 100
            And the response json at $.category is equal to "reference"
            And the response json at $.title is equal to "Sayings of the Century"
```