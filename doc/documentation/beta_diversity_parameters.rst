.. _beta_diversity_parameters:

=============================
Beta-Diversity Parameters
=============================
Beta-diversity allows for calculating *between* sample diversity in an OTU table, using a variety of beta-diversity metrics.

The steps performed by this option are: 
    #. Generate rarefied OTU table
    #. Compute beta-diversity metrics on rarefied OTU table
    #. Perform principal coordinate analysis on beta-diversity table
    #. Generate a preferences file
    #. Generate 2D/3D PCoA Plots or distance histograms.

* Beta-Diversity checkbox: Visual representation of the distance between each sample's phylogenetic diversity
    * *Optional Parameters* (`rarefaction.py <http://qiime.org/scripts/single_rarefaction.html>`_)
        * Rarefied at
            * Number of seqs/sample used to calculate beta-diversity.
    * *Optional Parameters* BETA_DIVERSITY.PY
        * List of samples to compute  
            * Compute only these rows of the distance matrix. User should pass a list of sample names. This allows the user to essentially filter the OTU table and compute the beta-diversity calculations for only the samples passed
        * Metrics to use
            * `List of beta-diversity metrics <http://qiime.org/scripts/beta_diversity_metrics.html>`_
        * Tree already trimmed
            * By default, tips not corresponding to OTUs in the OTU table are removed from the for diversity calculations. Select this option to skip step if you're already passing a minimal tree. Beware with "full_tree" metrics, as extra tips in the tree will change the result.
    * 2D PCoA Plots checkbox (`make_2d_plots.py <http://qiime.org/scripts/make_2d_plots.html>`_)
        * Color by category  
            * Comma-separated list of metadata categories to color by in the plots. The categories must match the column header in the mapping file exactly. Multiple categories can be listed by comma separating them without spaces. The user can also combine columns by separating  the categories by "&&" without spaces.
            * Background color
                * Background color to be used in the plots. 
            * Ellipsoid opacity
                * Used only plotting ellipsoids for jackknifed beta-diversity (i.e. using a directory of coord files instead of a single coord file). Valid range is 0-1, with 0 being completely  transparent.
            * Ellipsoid method
                * Used only plotting ellipsoids for jackknifed beta-diversity (i.e. using a directory of coord files instead of a single coord file). Valid values are IQR or sdev.
            * Scree 
                * The scree plot is a simple line segment plot that shows the fraction of total variance in the data as explained or represented by each principal coordinate (PC).  
    * 3D PCoA Plots checkbox (`make_3d_plots.py <http://qiime.org/scripts/make_3d_plots.html>`_)
        * Color by category
            * Comma-separated list of metadata categories to color by in the plots. The categories must match the column header in the mapping file exactly. Multiple categories can be listed by comma separating them without spaces. The user can also combine columns by separating  the categories by "&&" without spaces
        * Custom axis
            * This is the category from the metadata mapping file to use as a custom axis in the plot.  For example, if there is a pH category and you like to see the samples plotted on that axis instead of PC1, or PC2, etc., one can use this option. It is also useful for plotting time-series data. NOTE: if there are any non-numeric data in the column, it will not be plotted.  
        * Background color
            * Background color of the plot.
        * Ellipsoid smoothness
            * Used only when plotting ellipsoids for jackknifed beta-diversity (i.e. using a directory of coord files instead of a single coord file). Valid choices are 0-3. A value of 0produces very coarse ellipsoids but is fast to render. If you encounter a memory error when generating or displaying your plots, try including just one metadata column in the analysis. If you still have problems, reduce the smoothness to 0.  
        * Ellipsoid opacity
            * Used only plotting ellipsoids for jackknifed beta-diversity (i.e. using a directory of coord files instead of a single coord file). Valid range is 0-1, with 0 being completely transparent. 
        * Ellipsoid method
            * Used only plotting ellipsoids for jackknifed beta-diversity (i.e. using a directory of coord files instead of a single coord file). Valid values are IQR or sdev.  
        * # of taxa to keep
            * Used only when generating BiPlots. This is the number of taxa to display. Use -1 to display all. 
        * Output format
            * If this option is set to inVUE, you will also need to use the -b option to define which columns from the metadata file the script should use when writing the output file.
        * # of interpolation points
            * Used only when generating inVUE plots. Number of points between samples for interpolation.  
        * # of polyhedron points 
            * Used only when generating inVUE plots. The number of points to be generated when creating a frame around the the PCoA plots.
        * Polyhedron offset
            * Used only when generating inVUE plots. The offset to be added to each point being created when using the --polyhedron_points option. This is only used when using the invue output_format.
        * Create vectors based on metadata  
            * Create vectors based on a column of the mapping file. This parameter accepts up to two columns: (1) create the vectors, (2) sort them. If you want to group by Species and order by SampleID, you will pass, "--add_vectors=Species" but if you want to group by species but order by DOB you will pass, "--add_vectors=Species,DOB; this is useful when you use --custom_axes param.  
        * RMS algorithm  
            * The algorithm to calculate RMS, either avg or trajectory; both algorithms use all the dimensions and weights them using their percentage explained; return the norm of the vectors created. and their confidence using ANOVA. The vectors are created as follows: for avg, it calculates the average at each timepoint (averaging within the group), then calculated the norm for each point; for trajectory, calculates the norm from the 1st-2nd, 2nd-3rd, etc.
        * RMS output path calculations
            * Name of the file to save the RMS of the vectors grouped by the column used with the --add_vectors function. NOTE: this option only works with --add_vectors. The file is going to be created inside the output_dir and its name will start with "RMS".  
    * Distance Histograms checkbox (`make_distance_histograms.py <http://qiime.org/scripts/make_distance_histograms.html>`_)
        * Background color
            * Background color of the plot.
        * Suppress HTML 
            * This gives the user the ability to only plot out the calculations, so they can replot the data in other tools (e.g. Excel)  
        * Categories to compare  
            * Comma-separated list of fields to compare, where the list of fields should be in quotes. NOTE: if this option is passed on the command-line, it will overwrite the fields in prefs file...  
        * # of monte carlo iterations  
            * Number of iterations to perform for Monte Carlo analysis.
