# Created by proccaserra

Feature: batch assay object creation

	Scenario Outline: batch assay object creation case1
	Given a valid Material object type or set of Material objects  of size integer = n,
	And a boolean parameter ‘is_multiplex_assay’ (several samples run together) set to false,
	And a boolean parameter ‘is_multichannel_assay’ (several acquisition channel for each sample) set to false,
	And a integer tr parameter ‘number of technical repeats’ to indicate the number of technical replicates (the assumption is now that this setting would apply to all assays,however we can not rule out deviation or specification for only some assays),
	When the source path points to a JSON file
	Then it should create ‘n x tr’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

	Examples: 12 samples, single channel hybridization (affymetrix DNA microarray), one single chip design, one technical replicate per sample -> (12 x 1 x 1 x1)= 12 assays /data acquisition event


	Scenario: batch assay object creation case2
	Given a valid Material object type or set of Material objects of size integer = n,
	And a boolean parameter ‘is_multiplex_assay’ (several samples run together) set to true,
		And dependent integer parameter mss ‘multiplex_set_size’ 
	And a boolean parameter ‘is_multichannel_assay’ (several acquisition channel for each sample) set to false,
	And a integer tr parameter ‘number of technical repeats’ to indicate the number of technical replicates (the assumption is now that this setting would apply to all assays,however we can not rule out deviation or specification for only some assays),
	When the source path points to a JSON file
	Then it should create ‘(n/mms) * tr where n/mms is an integer’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

	Examples: 12 samples, mass spectrometry, iTRAQ labeling with 4 reagents ( ~ multiplexing), each iTRAQ pool injected 5 times on the mass spectrometer -> (12/4)*5=15 assays 


	Scenario: batch assay object creation case3
	Given a valid Material object type or set of Material objects of size integer = n,
	And a boolean parameter ‘is_multiplex_assay’ (several samples run together) set to false, 
	And a boolean parameter ‘is_multichannel_assay’ (several acquisition channel for each sample) set to true,
		And dependent integer parameter mcc ‘multichannel_count
	And a boolean parameter  ‘uses_set_list_of_features’ set to true
	And dependent integer parameter nslf ‘number_of_set_list_of_feature’	
	And a integer tr parameter ‘number of technical repeats’ to indicate the number of technical replicates (the assumption is now that this setting would apply to all assays,however we can not rule out deviation or specification for only some assays),
	When the source path points to a JSON file
	Then it should create ‘((n / mcc)* nslf * tr where n/mpa is an integer’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

	Examples: 12 samples, dual channel hybridization, 3 array designs, 2 technical replicates -> (12/2)*3*1= 18 assay

