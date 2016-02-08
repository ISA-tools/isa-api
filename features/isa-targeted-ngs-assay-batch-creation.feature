# Created by proccaserra

# assumption: multiplex assay: A multiplex assay is a type of assay that simultaneously measures multiple analytes (dozens or more) in a single run/cycle of the assay in one specimen

Feature: batch ngs-assay object creation

	Scenario Outline: batch ngs-assay object creation case1
	Given a valid 'Material object type=Sample' or a set of size integer = n, of Materials of type = Sample
	And a parameter 'measurement type' = 'targeted metagenomics'
	And a parameter of type array with possible values [Archeae,Bacteria,Eukaryota,Viruses]
	And a parameter of type array 'target genes' with dependent values [Archeae{16S RNA,OTHER},Bacteria {16S RNA,OTHER}, Eukaryota{16S RNA, ITS,OTHER}, Viruses{16S RNA, OTHER}]
	And an optional parameter of type array 'target_subfragment' with dependent value Eukaryota{ITS}{V4,V5,V6}
	And an optional parameter 'is_multiplexed_library' set to true
	And a parameter 'library layout' from possible values {single,paired} with value set to 'single'
	And request 'multiplex_identifier_sequence' for each of the libraries defined by sample+target_gene_value(+target_subfragment)
	And request 'sequencing instrument' from possible values {(see configuration)}
	And assuming one run per library
	Then create n x size of 'target genes array' ngs Assays.
