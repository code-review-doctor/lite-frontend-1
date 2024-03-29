@licence @edit @all @open
Feature: I want to be able to edit and update an active application
  As a logged in exporter
  I want to be able to edit and update an active application
  So that any additional information and/or corrected details can be updated on my application

  @skip @LT_998_edit_open_application @regression
  Scenario: Edit an open application
    Given I go to exporter homepage and choose Test Org
    And I create an open application via api
    # Ensure automation doesn't move application to non-editable state
    And the status is set to "submitted"
    When I go to application previously created
    And I click edit application
    And I choose to make major edits
    And I click on the "goods" section
    And I remove a good type from the application
    Then no goods types are left on the application
    When I add a goods type with description "Sniper" controlled "True" control code "ML1a" incorporated "Yes"
    And I click the back link
    And I submit the application
    And I click continue
    And I agree to the declaration
    And I go to application previously created
    And I click on activity tab
    Then "updated the status to: submitted" is shown as position "1" in the audit trail
    And "added good type:" is shown as position "2" in the audit trail
    And "removed good type:" is shown as position "3" in the audit trail
