@all @internal @organisation
Feature: I want to add a company to LITE
  As a logged in government user
  I want to add a new company to LITE
  So that the new company can make applications

  @skip @LT_934_register_commercial_organisation @regression
  Scenario: Registering a commercial organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new commercial organisation
    Then commercial organisation is registered
    When I click the organisation
    And I edit the organisation
    Then organisation is edited
    And the "updated" organisation appears in the audit trail

  @skip @LT_1417_register_individual_organisation @regression
  Scenario: Registering an individual
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new individual organisation
    Then individual organisation is registered
    When I click the organisation
    Then the "created" organisation appears in the audit trail

  @skip @LT_1008_register_hmrc_organisation @regression
  Scenario: Registering an HMRC organisation
    Given I sign in to SSO or am signed into SSO
    When I go to organisations
    And I add a new HMRC organisation
    And I go to organisations
    Then HMRC organisation is registered
    When I click the organisation
    Then the "created" organisation appears in the audit trail

  Scenario: Review and approve an organisation
    Given I sign in to SSO or am signed into SSO
    And an anonymous user applies for an organisation
    When I navigate to organisations
    And I click on In review tab
    Then I should see details of organisation previously created
    When I click on the organisation and click Review
    Then I should see a summary and option to approve or reject organisation
    When I select approve and Save
    Then the organisation should be set to "Active"
    And the "activated" organisation appears in the audit trail
    When I navigate to organisations
    And I click on Active tab
    Then I should see details of organisation previously created

  @skip @LT_1105_review_and_reject_an_organisation @regression
  Scenario: Review and reject an organisation
    Given I sign in to SSO or am signed into SSO
    And an anonymous user applies for an organisation
    When I go to organisations
    And I go to the in review tab
    Then the organisation previously created is in the list
    When I click the organisation
    And I click review
    Then I should see a summary of organisation details
    When I reject the organisation
    Then the organisation should be set to "Rejected"
    And the "rejected" organisation appears in the audit trail
