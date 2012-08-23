.. _otu_table_parameters:

==========================
OTU Table Parameters
==========================
The OTU-table will be in the `BIOM-format <http://biom-format.org/>`_, which is the same format that QIIME uses.

The following options are available through the **Meta-Analyses to Perform** page:

* OTU Table checkbox: A table that contains all the assigned OTUs (Operational Taxonomic Unit) and the abundance of those taxa in each sample.

    * *Optional Parameters* (taxonomy assignment and rarefaction)
        * Select Taxonomy (These assignments were retrieved from the `Greengenes website <http://greengenes.lbl.gov/>`_)
            * This refers to the taxonomy that should be added to the OTU-table.
                * PHPR *(Default)*: This is the Phil Hugenholtz Pre-Release of Greengenes from February 4, 2011.
                * G2_chip
                * Hugenholtz
                * Ludwig
                * NCBI
                * Pace
                * RDP
        * Rarefied at 
            * The number of sequences per sample to rarefy the OTU-table.
    * *Optional Parameters* (Combine Mapping Categories)
        * Select Categories 
            * This option allows users to combine multiple metadata fields to create a new metadata field, while the original fields are preserved. 
