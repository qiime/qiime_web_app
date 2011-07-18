
.. QIIME documentation master file, created by
   sphinx-quickstart on Mon Jan 25 12:57:02 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################################################
QIIME: Quantitative Insights Into Microbial Ecology
######################################################
QIIME (canonically pronounced 'Chime') is a pipeline for performing microbial community analysis that integrates many third party tools which have become standard in the field. 

A standard QIIME analysis begins with sequence data from one or more sequencing platforms, including Sanger, Roche/454, and Illumina GAIIx. QIIME can perform library de-multiplexing and quality filtering; denoising with PyroNoise; OTU and representative set picking with uclust, cdhit, mothur, BLAST, or other tools; taxonomy assignment with BLAST or the RDP classifier; sequence alignment with PyNAST, muscle, infernal, or other tools; phylogeny reconstruction with FastTree, raxml, clearcut, or other tools; alpha diversity and rarefaction, including visualization of results, using over 20 metrics including Phylogenetic Diversity, chao1, and observed species; beta diversity and rarefaction, including visualization of results, using over 25 metrics including weighted and unweighted UniFrac, Euclidean distance, and Bray-Curtis; summarization and visualization of taxonomic composition of samples using pie charts and histograms; and many other features.

QIIME includes parallelization capabilities for many of the computationally intensive steps. By default, these are configured to utilize a mutli-core environment, and are easily configured to run in a cluster environment. QIIME is built in Python using the open-source PyCogent_ toolkit. It makes extensive use of unit tests, and is highly modular to facilitate custom analyses.

Blog and Mailing List
======================
We recommend that all QIIME users keep an eye on the QIIME blog for important announcements. You can `subscribe to the RSS feed <http://qiime.wordpress.com/feed/>`_ or `sign up for e-mail notifications on the front page of the blog <http://qiime.wordpress.com>`_. This is a very low traffic list (typically around one message per month), and we will not share subscriber information with anyone.


Contact Us
===========
The quickest way to get help with QIIME is to search or ask questions in the `QIIME Forum <http://groups.google.com/group/qiime-forum>`_. This is a public space for users to ask questions, search previous questions and answers, and share any tips they've found. The QIIME Developers moderate this forum, and we aim to respond to questions within one working day.

If your question can't be posted in the public forum because you would need to share private data, contact `QIIME Support <qiime.help@colorado.edu>`_. We aim to respond to e-mail questions within three to five working days. 

Users can also submit `bug reports <http://sourceforge.net/tracker/?group_id=272178&atid=1157164>`_ and `feature requests <http://sourceforge.net/tracker/?group_id=272178&atid=1157167>`_ using via Sourceforge.


Citing QIIME
============
If you use QIIME for any published research, please include the following citation:

	**QIIME allows analysis of high-throughput community sequencing data**
	
	J Gregory Caporaso, Justin Kuczynski, Jesse Stombaugh, Kyle Bittinger, Frederic D Bushman, Elizabeth K Costello, Noah Fierer, Antonio Gonzalez Pena, Julia K Goodrich, Jeffrey I Gordon, Gavin A Huttley, Scott T Kelley, Dan Knights, Jeremy E Koenig, Ruth E Ley, Catherine A Lozupone, Daniel McDonald, Brian D Muegge, Meg Pirrung, Jens Reeder, Joel R Sevinsky, Peter J Turnbaugh, William A Walters, Jeremy Widmann, Tanya Yatsunenko, Jesse Zaneveld and Rob Knight; Nature Methods, 2010; doi:10.1038/nmeth.f.303


You can find the `QIIME paper here <http://www.nature.com/nmeth/journal/vaop/ncurrent/full/nmeth.f.303.html>`_, and the data presented in this paper can be found `here <http://bmf.colorado.edu/QIIME/QIIME_NM_2010.tgz>`_.

.. _PyCogent: http://pycogent.sourceforge.net