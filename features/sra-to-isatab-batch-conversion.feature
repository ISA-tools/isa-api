# Created by massi at 04/02/2016
Feature: SRA to ISA-tab Batch conversion
  # perform a batch conversion of a set of SRA datasets, retrieved from the European Nucleotide Archive
  # to ISA-tab

  Scenario Outline: Batch conversion form a list of SRA accession numbers
    Given A list of comma separated access numbers "<access_numbers>"
    When the SRA to ISA tab conversion is invoked
    Then it should return a ZIP file object
    And the ZIP file should contain as many directories as the element in the list
    Examples:
      | list |
      | ERA000059, ERP00144, ERP001440 |
