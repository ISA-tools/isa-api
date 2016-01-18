# Created by massi at 18/01/2016

Feature: ISA file management
  # retrieve an isa dataset in JSON format from a remote repository
  ISA-dataset should be retrieved in JSON or TAB format

  Scenario: connection to a remote GitHub repository
    Given an optional user login "test_user"
    And an optional user password "test_password"
    When a storage adapter is created
    Then it should instantiate an authenticated connector instance

  Scenario: resource retrieval with file download
    Given a valid path in the remote repository "/path/to/source"
    And an (optional) destination directory "/path/to/destination"
    When the source path points to directory
    Then it should download the whole directory it as an archived file
    When the source path points to an archive
    Then it should save it as it is (i.e. an archive)
    When the source file points to an (ISA-TAB) JSON file
    Then it should download it as a JSON file
    When the source file points to an (ISA-TAB) XML configuration file
    Then it should download it as an XML file
    When it is a different file
    Then it should raise an error (validation error)

  Scenario: resource retrieval with in-memory storage
    Given a valid path in the in the remote repository "/path/to/source"
    When the source path points to a JSON file
    Then it should store/load a Python dictionary containing the whole ISA dataset
    When the source points to an XML configuration file
    Then it should load the XML document in memory
    When it is a different file or a directory
    Then it should raise an error

  # Future scenarios: create, update, delete


