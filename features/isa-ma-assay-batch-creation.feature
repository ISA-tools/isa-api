# Created by proccaserra

# assumption: multiplex assay: A multiplex assay is a type of assay that simultaneously measures multiple analytes (dozens or more) in a single run/cycle of the assay in one specimen

Feature: batch ma-assay object creation

	Scenario Outline: batch ma-assay object creation case1 (single channel -> one sample / microarray chip)
	Given a valid 'Material object type=Sample' or a set of size integer = n, of Materials of type = Sample
	And a parameter 'technology type' = 'DNA microarray'
	And an parameter 'single_channel_data_acquisition' set to true
	And a parameter array 'Labels'
	And an array parameter to allow specifying one or more 'microarray design' (n_mdes)
	And a parameter 'number of scans per microarray slide (n_sms)' by default set to 1
	Then create n x n_mdes x n_sms assays, each with one 'Raw Data File' with one single sample as input


	example:
		5 samples of type 'blood'
		single_channel = true
		labels = [biotin]
		array_design = [MOE430A,MOE430B,Illumina 418k]
		scan_number = 1

		15 hybridizations objects, each with one raw data file



	Scenario Outline: batch ma-assay object creation case2 (multichannel (2 channel and hybridization vs a reference))

	Given a valid 'Material object type=Sample' or a set of size integer = n, of Materials of type = Sample
	And a parameter 'technology type' = 'DNA microarray'
	And an parameter 'single_channel_data_acquisition' set to false
	And a parameter array 'Labels'
	And a boolean parameter 'dye-swap' is false
	And a boolean parameter 'pooled_reference' set to true
	And a parameter 'dye-on-reference  =Label1
	And an array parameter to allow specifying one or more 'microarray design' (n_mdes)
	And a parameter 'number of scans per microarray slide (n_sms)' by default set to 1
	Then create n x n_mdes x n_sms assays, each with one 'Raw Data File' with 1 labeled extract from one of the samples and 1 Labeled extract corresponding to the reference pool

	(if dye-swap is set to true, duplicate the number of assays and invert the value of 'label dyes' between reference_pool and test_sample)


	example:  

		5 samples, one of the following type liver,kidney,brain,heart,fat
		single_channel = false
		labels = [Cy3, Cy5] 
		dye-swap = false
		array-design = [GeneChip® Human Exon 1.0 ST , Agilent G4832A]
		pool_reference = true
		dye_on_reference = Cy3
		scan_number = 2

		5 x 2  hybridizations, each with 2 raw data files, each hybridization has 2 inputs labeled extracts, one  individual samples, one from a mix of the 5 samples.



Scenario Outline: batch ma-assay object creation case2 (multichannel (2 channel and hybridization between matched-pairs))

	Given 2 ordered sets of 'Material object type=Sample' of equal size integer = n, each set different for a boolean characteristics
	And a parameter 'technology type' = 'DNA microarray'
	And an parameter 'single_channel_data_acquisition' set to false
	And a parameter array 'Labels'
	And a boolean parameter 'matched-pairs' set to true
	And a parameter 'dye-on-first = Label1
	And a boolean parameter 'dye-swap' is false
	And an array parameter to allow specifying one or more 'microarray design' (n_mdes)
	And a parameter 'number of scans per microarray slide (n_sms)' by default set to 1
	Then create n x n_mdes x n_sms assays, each with one 'Raw Data File' with 1 labeled extract from one of the samples and 1 Labeled extract corresponding to the reference pool

	(if dye-swap is set to true, duplicate the number of assays and invert the value of 'label dyes' between reference_pool and test_sample)

example:  

		2 sets of 6 samples, set #1 -> normal, set #2 -> tumour
		single_channel = false
		labels = [Cy3, Cy5] 
		dye-swap = false
		array-design = [GeneChip® Human Exon 1.0 ST , Agilent G4832A, HG_U230_2]
		pool_reference = false
		matched-pairs = true
		dye_on_first = Cy3
		scan_number = 1



		6 (size of sample sets) x 3  (number of distinct array designs) hybridizations, each with 1 raw data file, each hybridization has 2 input labeled extracts, one  individual samples from each set at index j (0..5).


		

