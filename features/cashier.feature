Feature: Withdraw or Deposit balance into an account
  As a client I want to withdraw or deposit balance into an account.

  Scenario: Deposit balance
    When I make a request to cashier service
       And a request json payload
       """
        {
            "accountNumber": "123441238",
            "amount": 120,
            "operation": "debit"
        }
      """
    Then I should receive an "Accepted" response
        And I should see a "accepted" status