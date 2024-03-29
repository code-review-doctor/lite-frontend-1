@all @internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @skip @LT_1376 @regression @skip @LT_1760
  Scenario: Give proviso advice
    Given I sign in to SSO or am signed into SSO
    And an Exhibition Clearance is created
    And I create a proviso picklist
    And I create a standard advice picklist
    And the status is set to "submitted"
    When I go to application previously created
    And I click on the user advice tab
    And I select all items in the user advice view
    And I choose to 'proviso' the licence
    And I select "UK SECRET" clearance level
    And I import text from the 'proviso' picklist
    And I import text from the 'text' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I select that a footnote is required with the note 'I believe the items are good, but have concerns about the country'
    And I click continue
    Then I see my advice has been posted successfully
    And I see added advice in the same amount of places
    When I go to grouped view
    And I select all items in the "proviso" grouped view
    And I click give advice
    And I choose to 'proviso' the licence
    Then I see the fields pre-populated with the proviso and advice picklist items

  @skip @LT_1115_grant @regression
  Scenario: Give approval advice
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And all flags are removed
    And I create a proviso picklist
    And I create a standard advice picklist
    And the status is set to "submitted"
    When I go to application previously created
    And I click on the user advice tab
    Then I see total goods value
    When I select all items in the user advice view
    And I choose to 'approve' the licence
    Then I dont see clearance level
    When I import text from the 'text' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I select that a footnote is not required
    And I click continue
    Then I see my advice has been posted successfully
    When I combine all user advice
    And I combine all team advice
    And I finalise the advice
    Then today's date and duration is filled in

  @skip @LT_966_refusal_flags @regression
  Scenario: Give refusal advice
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And the status is set to "submitted"
    When I go to application previously created
    And I click on the user advice tab
    And I select all items in the user advice view
    And I choose to 'refuse' the licence
    And I select decision "2b"
    And I import text from the 'text' picklist
    And I write 'We will get back to you in three weeks' in the note text field
    And I select that a footnote is required with the note 'These classification of items can not go to the countries selected'
    And I click continue
    Then I see my advice has been posted successfully
    And I see added advice in the same amount of places
    When I combine all user advice
    And I go to application previously created
    Then I see refusal flag is attached

  @skip @LT_920_cannot_give_advice_terminal_case @regression
  Scenario: Cannot give advice on a case in terminal state
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    And I create a proviso picklist
    And I create a standard advice picklist
    And the status is set to "submitted"
    When I go to application previously created
    And I click change status
    And I select status "Withdrawn" and save
    And I click on the user advice tab
    Then the give advice checkboxes are not present
    And the give or change advice button is not present
    When I go to the team advice
    Then the give advice checkboxes are not present
    And the give or change advice button is not present
    When I go to the final advice
    Then the give advice checkboxes are not present
    And the give or change advice button is not present
