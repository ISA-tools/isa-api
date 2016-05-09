# Created by proccaserra

Feature: batch material creation

	#user story 14
	Scenario Outline: batch creation of source material
	Given a valid Material object type <source>
	And an integer ‘n’ as method parameter,
	And an (optional) array of Annotation categories and associated values 
	And an boolean parameter ‘annotation_to_all_object’ set to true
	When the source path points to a JSON file
	Then it should create ‘n’ distinct instances of Material Objects of the type defined,
	all bearing the set of annotations available in a Python dictionary.


	#user story 15
	Scenario Outline: batch material object creation other than source
	Given a valid Material object type not <source>
	And a valid protocol_type (ontology term, preferably from OBI) as method parameter
	And an integer ‘n’ as method parameter,
	And an (optional) array of Annotation categories and associated values 
	And an (optional) boolean parameter ‘annotation_to_all_object’ set to true,
	And an (optional) boolean parameter ‘annotation_specific to_object’ set to true,
	And an (optional) Annotation category with an array of n possible values 
	When the source path points to a JSON file
	Then it should create ‘n’ distinct instances of Material Objects of the type defined,
	all bearing the set of annotations available in a Python dictionary.
