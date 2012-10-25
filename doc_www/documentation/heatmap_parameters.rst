.. _heatmap_parameters:

=========================
Heatmap Parameters
=========================
The heatmap is an easy way to display the OTU-table where the colors go from blue (low-counts) to red (high-counts). The larger the OTU-table, the more difficult it is to visualize the heatmap, so be cautious when using large OTU-tables.

* Heatmap checkbox: A graphic that displays how frequently each OTU occurs in each sample.
    * *Optional Parameters* (`make_otu_heatmap_html.py <http://qiime.org/scripts/make_otu_heatmap_html.html>`_)
        * # of sequences
            * Only include OTUs with this number of sequences.
        * Perform log transformation
            * log transform the OTU frequencies
        * Replace zeros w this value x smallest non-zero value
            * When performing the log transformation, replace zeros with some small value that the user specifies. By default, this value is 1/2 the smallest non-zero value.

