# Created by proccaserra

# assumption: multiplex assay: A multiplex assay is a type of assay that simultaneously measures multiple analytes (dozens or more) in a single run/cycle of the assay in one specimen

Feature: batch assay object creation

	Scenario Outline: batch assay object creation case1
	Given a valid 'Material object type' or a set of size integer = n, of Materials of a given type 
	And a boolean parameter ‘is_multiplexed_analyte_assay’ (multiplex_analytes meaning multiple analytes/variables being measured simultaneously in one specimen / several acquisition channels for each sample in one run of assay) set to true,
	And a boolean parameter ‘is_multiplexed_sample_assay’ (multiplex_samples meaning multiple specimens being analyzed in one run of assay) set to false,
	And a integer tr parameter ‘number of technical repeats’ to indicate the number of technical replicates (the assumption is now that this setting would apply to all assays,however we can not rule out deviation or specification for only some assays),
	When the source path points to a JSON file
	Then it should create ‘n x tr’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

	Examples: 12 samples, single channel hybridization (affymetrix DNA microarray), one single chip design, one technical replicate per sample -> (12 x 1 x 1 x1)= 12 assays /data acquisition event


	Scenario: batch assay object creation case2
	Given a valid 'Material object type' or a set of size integer = n, of Materials of a given type 
	And a boolean parameter ‘is_multiplexed_analyte_assay’ (multiplex_analytes meaning multiple analytes/variables being measured simultaneously in one specimen / several acquisition channels for each sample in one run of assay) set to true,
		

	And a boolean parameter ‘is_multiplexed_sample_assay’ (multiplex_samples meaning multiple specimens being analyzed in one run of assay) set to true,
			And dependent integer parameter msss ‘multiplex_sample_set_size’ 
	And a integer tr parameter ‘number of technical repeats’ to indicate the number of technical replicates (the assumption is now that this setting would apply to all assays,however we can not rule out deviation or specification for only some assays),
	When the source path points to a JSON file
	Then it should create ‘(n/msss) * tr where n/msss is an integer’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

	Examples: 12 samples, mass spectrometry, iTRAQ labeling with 4 reagents ( ~ multiplexed_samples), each iTRAQ pool injected 5 times on the mass spectrometer -> (12/4)*5=15 assays 



	Scenario: batch assay object creation case3
		Given a valid 'Material object type' or a set of size integer = n, of Materials of a given type 
		And a boolean parameter ‘is_multiplexed_analyte_assay’ (multiplex_analytes meaning multiple analytes/variables being measured simultaneously in one specimen / several acquisition channels for each sample in one run of assay) set to true,
		And a boolean parameter  ‘uses_set_list_of_features’ set to true
		And dependent integer parameter nslf ‘number_of_set_list_of_feature’

		And a boolean parameter ‘is_multiplexed_sample_assay’ (multiplex_samples meaning multiple specimens being analyzed in one run of assay) set to false,
			And dependent integer parameter mcc ‘multichannel_count
	
		And a integer tr parameter ‘number of technical repeats’ to indicate the number of technical replicates (the assumption is now that this setting would apply to all assays,however we can not rule out deviation or specification for only some assays),
		When the source path points to a JSON file
		Then it should create ‘((n / mcc)* nslf * tr where n/mpa is an integer’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

		Examples: 12 samples, dual channel hybridization, 3 array designs, 2 technical replicates -> (12/2)*3*1= 18 distinct assays





OLD, DEPRECATED DEFINITIONS:

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
	Then it should create ‘((n / mcc)* nslf * tr where n/mcc is an integer’ distinct instances of Assay ‘data acquisition’ process Objects of the type defined.

	Examples: 12 samples, dual channel hybridization, 3 array designs, 2 technical replicates -> (12/2)*3*1= 18 assay

