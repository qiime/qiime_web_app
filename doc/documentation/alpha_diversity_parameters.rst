.. _alpha_diversity_parameters:

============================
Alpha-Diversity Parameters
============================
Alpha-diversity allows for calculating *within* sample diversity in an OTU table, using a variety of alpha-diversity metrics.

The steps performed by this option are: 
    #. Generate rarefied OTU tables
    #. Compute alpha diversity metrics for each rarefied OTU table 
    #. Collate alpha diversity results
    #. Generate alpha rarefaction plots

* Alpha Diversity checkbox: Plots the alpha-diversity for each sample using various sequences/sample constraints
    * *Required* (`multiple_rarefactions.py <http://qiime.org/scripts/multiple_rarefactions.html>`_)
        * Min # of seqs/sample
            * Minimum number of seqs/sample to be used to calculate alpha-diversity.
        * Max # of seqs/sample
            * Maximum number of seqs/sample to be used to calculate alpha-diversity.
        * Step size
            * Increment of seqs/sample between successive alpha-diversity calculations.
    * *Optional Parameters* (`multiple_rarefactions.py <http://qiime.org/scripts/multiple_rarefactions.html>`_)
        * # of iterations
            * For each seqs/sample constraint, the number of times the alpha-diversity is calculated.
        * Include lineages
            * For some calculations, such as alpha-diversity the taxonomy information may not be required, so you can choose to either include or exclude. It can be useful for very large OTU tables, since it reduces the size of the table in memory.
        * Retain empty OTUs
            * Retain OTUs of all zeros, which are usually omitted from the output of the OTU table. 
    * *Optional Parameters* (`alpha_diversity.py <http://qiime.org/scripts/alpha_diversity.html>`_)
        * metrics  
            * `List of alpha-diversity metrics <http://qiime.org/scripts/alpha_diversity_metrics.html#index-0>`_
    * *Optional Parameters* (`make_rarefaction_plots.py <http://qiime.org/scripts/make_rarefaction_plots.html>`_)
        * color by category  
            * Comma-separated list of metadata categories to color by in the plots. The categories must match the column header in the mapping file exactly. Multiple categories can be listed by comma separating them without spaces. The user can also combine columns by separating the categories by "&&" without spaces.  
        * background color 
            * Background color of the plot.
        * Image type
            * Type of image to produce. WARNING: some formats may not open properly in some browsers. 
        * Image resolution
            * Resolution of the plot (units = dpi) 
        * Y-axis height
            * Maximum Y-value to be used in the plots. Allows for directly comparable rarefaction plots between analyses.  
        * Suppress HTML
            * This gives the user the ability to only print out the calculations, so they can replot the data in other tools (e.g. Excel) std type  Method for calculating error bars.
