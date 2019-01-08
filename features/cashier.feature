Feature: Withdraw or Deposit balance into an account
  As a client I want to withdraw or deposit balance into an account.

  Scenario: Deposit balance
    When I make a request to cashier service
       And a request json payload
       """
        {
            "accountName": "123441238",
            "amount": 120,
            "action": "deposit"
        }
      """
    Then I should receive a CREATED response
        And I should see a pending status