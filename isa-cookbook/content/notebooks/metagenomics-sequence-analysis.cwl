#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow
requirements:
   - class: StepInputExpressionRequirement
   - class: InlineJavascriptRequirement
   - class: MultipleInputFeatureRequirement

label: Quality assessment, amplicon classification and functional prediction
doc: | 
  Workflow for quality assessment of paired reads and classification using NGTax 2.0 and functional annotation using picrust2. 
  In addition files are exported to their respective subfolders for easier data management in a later stage.
  Steps:  
      - FastQC (read quality control)
      - NGTax 2.0
      - Picrust 2
      - Export module for ngtax

inputs:
  forward_reads:
    type: File
    doc: forward sequence file locally
    label: forward reads
  reverse_reads:
    type: File?
    doc: reverse sequence file locally
    label: reverse reads
  forward_primer: 
    type: string
    doc: Forward primer used
    label: Forward primer
  reverse_primer:
    type: string?
    doc: Reverse primer used
    label: Reverse primer
  reference_db:
    type: string?
    doc: Reference database used in FASTA format
    label: Reference database
  rev_read_len: 
    type: int?
    doc: Read length of the reverse read
    label: Reverse read length
  for_read_len: 
    type: int
    doc: Read length of the reverse read
    label: Reverse read length
  sample:
    type: string
    doc: Name of the sample being analysed
    label: Sample name
  fragment:
    type: string
    doc: Subfragment that is being analysed (e.g. V1-V3 or V5-region)
    label: Subfragment name
  primersRemoved:
    type: boolean?
    doc: Wether the primers are removed or not from the input files
    label: Primers are removed
  threads:
    type: int?
    doc: number of threads to use for computational processes
    label: number of threads
    default: 2
  metadata:
    type: File?
    doc: UNLOCK assay metadata file
    label: Metadata file


steps:
############################
  fastqc:
    run: ../fastqc/fastqc.cwl
    in:
      fastqs: 
        source: [forward_reads, reverse_reads]
        linkMerge: merge_flattened
        pickValue: all_non_null
    out: [html_files]
#############################
  reads_to_folder:
    run: ../expressions/files_to_folder.cwl
    in:
      files: 
        source: [forward_reads, reverse_reads]
        linkMerge: merge_flattened
        pickValue: all_non_null
      destination: 
        valueFrom: $("reads")
    out:
      [results]
############################
  ngtax:
    run: ../ngtax/ngtax.cwl
    in:
      forward_primer: forward_primer
      reverse_primer: reverse_primer
      reference_db: reference_db
      folder: reads_to_folder/results
      rev_read_len: rev_read_len
      for_read_len: for_read_len
      sample: sample
      fragment: fragment
      primersRemoved: primersRemoved
    out: [biom, turtle]
#############################
  ngtax_to_tsv-fasta:
    run: ../ngtax/ngtax_to_tsv-fasta.cwl
    in:
        input: ngtax/turtle
        identifier: sample
        fragment: fragment
        metadata: metadata
    out:
      [picrust_fasta, picrust_tsv, physeq_asv, physeq_seq, physeq_tax, physeq_met]
############################
  picrust2:
    when: $(inputs.fasta.size > 0)
    run: ../picrust2/picrust2_pipeline.cwl
    in:
        identifier: sample
        input_table: ngtax_to_tsv-fasta/picrust_tsv
        fasta: ngtax_to_tsv-fasta/picrust_fasta
        threads: threads
    out: [EC_metagenome_out,PFAM_metagenome_out,TIGRFAM_metagenome_out,COG_metagenome_out,KO_metagenome_out,intermediate,pathways_out,EC_predicted.tsv.gz,PFAM_predicted.tsv.gz,TIGRFAM_predicted.tsv.gz,KO_predicted.tsv.gz,marker_predicted_and_nsti.tsv.gz,out.tre]
############################
  folder_compression:
    when: $(inputs.fasta.size > 0)
    run: ../bash/compress_directory.cwl
    in:
      indir: picrust2/intermediate
      # Needed for the condition
      fasta: ngtax_to_tsv-fasta/picrust_fasta
    out:
      [outfile]
############################
  fastqc_files_to_folder:
    run: ../expressions/files_to_folder.cwl
    in:
      files: 
        source: [fastqc/html_files]
      destination: 
        valueFrom: $("1_QualityControl")
    out:
      [results]
############################
  ngtax_files_to_folder:
    run: ../expressions/files_to_folder.cwl
    in:
      files:
        source: [ngtax/biom, ngtax/turtle]
      destination: 
        valueFrom: $("2_Classification")
    out:
      [results]
############################
  picrust_files_to_folder:
    when: $(inputs.fasta.size > 0)
    run: ../expressions/files_to_folder.cwl
    in:
      files:
        source: [picrust2/EC_predicted.tsv.gz, picrust2/PFAM_predicted.tsv.gz, picrust2/TIGRFAM_predicted.tsv.gz, picrust2/KO_predicted.tsv.gz, picrust2/marker_predicted_and_nsti.tsv.gz, picrust2/out.tre, folder_compression/outfile]
        linkMerge: merge_flattened
      folders:
        source: [picrust2/EC_metagenome_out, picrust2/PFAM_metagenome_out, picrust2/TIGRFAM_metagenome_out, picrust2/COG_metagenome_out, picrust2/KO_metagenome_out, picrust2/pathways_out]
        linkMerge: merge_flattened
      destination:
        valueFrom: $("3_PICRUSt2")
      # Needed for the condition
      fasta: ngtax_to_tsv-fasta/picrust_fasta
    out:
      [results]
############################
  phyloseq_files_to_folder:
    run: ../expressions/files_to_folder.cwl
    in:
      files: 
        source: [ngtax_to_tsv-fasta/physeq_asv, ngtax_to_tsv-fasta/physeq_seq, ngtax_to_tsv-fasta/physeq_tax, ngtax_to_tsv-fasta/physeq_met]
        linkMerge: merge_flattened
      destination:
        valueFrom: $("4_PHYLOSEQ")
    out:
      [results]
############################

outputs:
  turtle:
    type: File
    doc: Used for other workflows
    outputSource: ngtax/turtle
  files_to_folder_fastqc:
    type: Directory
    outputSource: fastqc_files_to_folder/results
  files_to_folder_ngtax:
    type: Directory
    outputSource: ngtax_files_to_folder/results
  files_to_folder_picrust2:
    type: Directory
    outputSource: picrust_files_to_folder/results
  files_to_folder_phyloseq:
    type: Directory
    outputSource: phyloseq_files_to_folder/results
    

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0001-8172-8981
    s:email: mailto:jasper.koehorst@wur.nl
    s:name: Jasper Koehorst
  - class: s:Person
    s:identifier: https://orcid.org/0000-0001-9524-5964
    s:email: mailto:bart.nijsse@wur.nl
    s:name: Bart Nijsse

s:citation: https://m-unlock.nl
s:codeRepository: https://gitlab.com/m-unlock/cwl
s:dateCreated: "2021-01-01"
s:license: https://spdx.org/licenses/Apache-2.0 
s:copyrightHolder: "UNLOCK - Unlocking Microbial Potential"

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/

$schemas:
 - http://edamontology.org/EDAM_1.18.owl