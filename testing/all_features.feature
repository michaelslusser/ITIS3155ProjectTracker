Feature: Changing website style

	Scenario: User views their website style
	    Given the system has multiple styles
	    And User wants to view their current website style
	    When the User clicks the ‘Settings’ icon at the top right of the GUI
	    And User clicks ‘Theme’ from the drop down menu
	    Then system displays website styles
	
	Scenario: User changes website style
	    Given the system is displaying the ‘Theme’ menu GUI
	    When the User clicks on preferred style from menu
	    Then system updates theme with User’s selected theme
	    And the theme change is seen by User


Feature: Registering a new user

	Scenario: User wants to create new account 
	     Given the system is displaying the registration page
	     When the user enters in the necessary credentials
	     Then system adds the user’s credentials into database
	     And the user now has access to the system

    Scenario: User is already registered as a User
        Given the User is already a registered user in the system
        When the User clicks ‘Register’ button
        And User uses the same email address as a registered user
        Then system displays that the User is already registered as a user
        And denies User from registering

Feature: Create new task
	
	Scenario: User wants to create new task
	     Given that the system displays “task” page
	     When the User clicks “create new task”
	     And the enters in the necessary information 
	     And clicks “save new task”
	     Then the system will add the task to the project task page
	
	Scenario: User cancels task creation
	    Given that the User is in the task creation GUI
	    When the User clicks the ‘Cancel’ button
	    Then system exits the task creation GUI
	    And system does not add new task information

Feature: View project tasks
	
	Scenario: User wants to view project from User dashboard
	    Given that the User is logged in
	    When the User clicks ‘Dashboard’ menu
	    Then system displays all projects available to User

	Scenario: User wants to view all project details
	    Given that the system is displaying all projects
	    When the User clicks on specific project
	    Then system goes into single project view
	    And displays all selected project information
