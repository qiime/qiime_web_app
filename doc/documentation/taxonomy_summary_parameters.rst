.. _taxonomy_summary_parameters:

==============================
Taxonomy Summary Parameters
==============================
This option produces pie, bar and area charts showing the breakdown of taxonomy assignments by given levels.

The steps performed by this option are: 
    #. Summarize OTU table by metadata category
    #. Sorts the OTU table (Only works for OTU tables that are not summarized by a metadata category and will alphabetically if it is summarized by a metadata category)
    #. Summarize Taxonomy
    #. Plot Taxonomy Summary

* Taxonomy Summary checkbox: A graphic that deconstructs each sample into the taxa it contains.
    * Summarize OTU by Category checkbox (`summarize_otu_by_cat.py <http://qiime.org/scripts/summarize_otu_by_cat.html>`_)
        * *Required* (`summarize_otu_by_cat.py <http://qiime.org/scripts/summarize_otu_by_cat.html>`_)
            * Summarize category
                * Summarize OTU table using this category.
        * *Optional Parameters* (`summarize_otu_by_cat.py <http://qiime.org/scripts/summarize_otu_by_cat.html>`_)
            * Normalize counts
                * Normalize OTU counts, where the OTU table columns sum to 1.
    * *Optional Parameters* (`sort_otu_table.py <http://qiime.org/scripts/sort_otu_table.html>`_)
        * Category to sort by  
            * Sorts the taxonomy summary of each sample in ascending order of the value in a specified metadata field (e.g. if the category is AGE_IN_YEARS, a sample collected from a 3 year will be plotted before a sample from a 7 year old.)
    * *Optional Parameters* (`summarize_taxa.py <http://qiime.org/scripts/summarize_taxa.html>`_)
        * Summarize level  
            * The depth to which QIIME will assign some taxonomic identity to an OTU. Larger numbers correspond to a more specific taxa. Selecting multiple levels will result in a taxonomy summary for each selection.
            * md_identifier
                * The dictionary key in the biom-formatted OTU table to use for taxonomy assignment.
            * md_as_string
                * How the metadata is listed in the "taxonomy" dictionary, which can be a string or a list of taxonomy levels.
            * Taxonomic delimiter
                * Character used to separate taxonomy levels.
            * Use absolute abundance
                * Use the absolute abundance of the lineage. By default, the taxonomy summary reports the relative abundance.
            * Top % of OTUs to remove 
                * If present, OTUs having a large absolute abundance are trimmed. (e.g. a value of 0.5 will result in the removal of OTUs with an abundance larger than 5% of the total dataset)
            * Bottom OTUs to remove
                * If present, OTUs having a small absolute abundance are trimmed. To remove the OTUs that makes up less than 45% of the total dataset, you pass 0.45
            * transposed_output
                * If present, the output will be written transposed from the regular output. This is useful in cases when you want to use Site Painter to visualize your data.
    * *Optional Parameters* (`plot_taxa_summary.py <http://qiime.org/scripts/plot_taxa_summary.html>`_)
        * Taxonomic levels
            * Report a summary for each of the taxonomic levels selected
        * # of categories to retain
            * Maximum number of taxonomies to show in each pie chart. All other taxonomies will categorized in "other".
        * Background color
            * Background color of the plot.
        * Image resolution
            * Resolution of the figure (units = dpi)
        * X-axis width
            * Width of the plot.
        * Y-axis height
            * Height of the plot.
        * Bar width
            * Width of the bars in the bar chart. values must be between 0 and 1.
        * Image type
            * Format of the image (plot) to be produced.
        * Chart(s)
            * Type of plot to be produced.
        * Resize nth label
            * Increase the size of the every nth label. This is useful for large studies with many samples that need to be fit on the X-axis.
        * Include HTML legend
            * If present, writing of the legend in the HTML page is included.
        * Include HTML counts
            * By default it only shows the relative or absolute percentages, however; if you want to output the counts in other columns, then you can pass this option. It ends up doubling the width of the table, which makes visualization much more difficult.
        * X-axis label type
            * Depending on the sample_ids, you can plot the data on a numerical axis (i.e. where sample_ids are numbers, so the x-axis goes from sample-1 -> sample-10 and each point) or on a categorical axis (i.e. where sample_ids are strings (most common), so each sample is evenly spaced and not plotted on a number x-axis, instead it uses bins)
