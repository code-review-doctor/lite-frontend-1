@goods @all
Feature: I want to add a clc-case good to the goods list
    As a logged in exporter
    I want to add a clc-case good to the goods list
    So that I can ensure the good is listed in my cases

    @skip @LT_1006_add_clc_query_good @regression
    Scenario: Add "I don't know" good
        Given I sign in to SSO or am signed into SSO
        And I go to internal homepage
        Then I see the clc-case previously created
