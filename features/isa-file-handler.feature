# Created by massi at 18/01/2016

Feature: ISA file management
  # retrieve an isa dataset in JSON format from a remote repository
  ISA-dataset should be retrieved in JSON or TAB format

  Scenario: connection to a remote GitHub repository
    Given an optional user login "test_user"
    And an optional user password "test_password"
    When a storage adapter is created
    Then it should instantiate an authenticated connector instance

  Scenario: resource retrieval with directory download
    Given an authenticated storage adapter
    And a file object named "tests/data/BII-I-1" in the remote repository "isa-api" owned by "ISA-tools"
    And a branch named "develop"
    And a destination directory "destination_dir_0" in your home folder
    When the file object is a directory
    Then it should download the files contained within the directory
    And it should return a binary stream with the zipped content of the directory

  Scenario: resource retrieval with ZIP archive download
    Given an authenticated storage adapter
    And a file object named "ISA-tab records/sdata2014-isa1.zip" in the remote repository "ISA-tab" owned by "ScientificDataLabs"
    And a destination directory "destination_dir_1" in your home folder
    When the file object is a ZIP archive
    Then it should download it as it is

  Scenario: resource retrieval with JSON file download
    Given an authenticated storage adapter
    And a file object named "isatools/sampledata/BII-I-1.json" in the remote repository "isa-api" owned by "ISA-tools"
    And a branch named "latest-feat"
    And a destination directory "destination_dir_2" in your home folder
    When the source file points to an ISA-TAB JSON file
    Then it should download it as a JSON file
    And it should return the JSON content as a dictionary

  Scenario: resource retrieval with XML configuration file download
    Given an authenticated storage adapter
    And a file object named "tests/data/Configurations/isaconfig-default_v2015-07-02/genome_seq.xml" in the remote repository "isa-api" owned by "ISA-tools"
    And a destination directory "destination_dir_3" in your home folder
    When the source file points to an ISA-TAB XML configuration file
    Then it should download it as an XML file
    And it should return it as an XML object

  Scenario: resource retrieval of any other file
    Given an authenticated storage adapter
    And a file object named "setup.py" in the remote repository "isa-api" owned by "ISA-tools"
    And a destination directory "destination_dir_4" in your home folder
    When it is none of the allowed file types - JSON, XML, ZIP - nor a directory
    Then it should not save the file
    And it should return a falsey value

  Scenario: wrong Github path
    Given an authenticated storage adapter
    And a file object named "nonexistant/file_object.o" in the remote repository "isa-api" owned by "ISA-tools"
    And a destination directory "destination_dir_5" in your home folder
    When the remote source does not exist
    Then it should not save the file
    And it should raise an error

  # Future scenarios: create, update, delete


