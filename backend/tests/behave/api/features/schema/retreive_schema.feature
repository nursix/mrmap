Feature: OpenApi Schema
    As an API client,
    I want to fetch the openapi schema,
    so that I can configure the client dynamic based on the schema.

    Background: Setup baseurl, content-type and payload
        Given I use the endpoint http://localhost:8000/api/schema/

    Scenario: Can retreive as authenticated user
        Given I am logged in as User1 with password User1
        When I send the request with GET method
        Then I expect the response status is 200

    Scenario: Can retreive as anonymous user
        When I send the request with GET method
        Then I expect the response status is 200