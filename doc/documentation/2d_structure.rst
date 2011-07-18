.. _2d_structure:

==============
2D Structure
==============

.. _select_reference:

Setting Reference Sequence
---------------------------
Before using the functionality for 2D structure analysis, the user must have a 
2D mask in their FASTA file with the name "#=GC SS_cons".  If the user has this mask, they will need to set a reference sequence which corresponds to the 2D mask supplied from the Reference Sequence option.  Note: the Reference Sequence cannot be the 2D mask.

.. image:: ../images/ref_seq.png
    :align: center
    
Annotate Secondary Structure
----------------------------
Once the user has selected their reference sequence, they can annotate the alignment by clicking on the Evaluate 2D Mask button under the 2D Structure Tab. When evaluating the 2D mask, the user will see the basepair annotations for each basepair above the alignment.  Each basepair will be colored according to whether it is isosteric (green), non-isosteric (pink) or not allowed (cyan) compared to the reference sequences basepair.

.. image:: ../images/evaluate_2d_mask.png
    :align: center
    :height: 300px

Analyse Alignment Composition (based on 2D structure)
------------------------------------------------------
After evaluating the 2D structure mask in the alignment, the user may be interested in the base composition for stems, loops, or other regions of the alignment [1]_.  To view the base composition, the user should select "Base Composition" from the View menu under the 2D Structure Tab.  

.. image:: ../images/evaluate_2d_mask.png
    :align: center
    :height: 300px

This will generate a kinemage file, which will open in the `KiNG <http://kinemage.biochem.duke.edu/software/king.php>`_ java-applet. In the menu you should see "S", "L", "O" and "Total" under the RNA menu, where the letters stand for Stem, Loop, Other, and Total, respectively.

.. image:: ../images/2d_kinemage.png
    :align: center
    :height: 400px

For more information on base composition, please refer to Smit S, Knight R, Heringa J, 2009 [1]_.


Generate 2D structure
----------------------------
Once the user has selected their reference sequence and selected a sequence from the alignment, they can generate a 2D structure by selecting "2D Structure" from the View menu under the 2D Structure Tab.

.. image:: ../images/select_2d_structure.png
    :align: center
    :height: 200px

Once the new window appears, the user's sequence will be displayed in the VARNA java-applet [2]_.

.. image:: ../images/2d_structure.png
    :align: center
    :height: 500px

For more information on VARNA, please refer to Darty K, Denise A, Ponty Y, 2009 [2]_

.. [1] Smit S, Knight R, Heringa J. 2009. RNA structure prediction from evolutionary patterns of nucleotide composition. Nucleic acids research 37:1378-1386.
.. [2] Darty K, Denise A, Ponty Y. 2009. VARNA: Interactive drawing and editing of the RNA secondary structure. Bioinformatics 25:1974-1975.
