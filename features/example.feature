Feature: Search functionality
  Scenario: User searches for a keyword
    Given the user is on the home page
    When the user searches for "Selenium"
    Then the search results are displayed

