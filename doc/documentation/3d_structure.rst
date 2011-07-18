.. _3d_structure:


==============
3D Structure
==============

Evaluate Watson-Crick and non-Watson-Crick basepairs
-------------------------------------------------------
If the user uploaded a tab-delimited basepair list, they should see 3D Structure Tab above the alignment.  Within that tab, there is an "Evaluate Basepairs" button, which will annotate the alignment according to the supplied basepair list.  Before clicking on that button, the user must select  a Reference Sequence. For information on selecting the Reference Sequence, see :ref:`select_reference`. Once the Reference Sequence is set, the user can click the "Evaluate Basepairs" button under the 3D Structure Tab.  The alignment will be annotated with Watson-Crick and non-Watson-Crick basepairs, which are listed above the alignment.  Since each base can make up to 3 basepair interactions, so there are three rows of basepairs, where the first row lists the first basepair that base is involved in, and the second row and third rows show additional basepairs the base is involved in.  The coloring of the cells correspond to the row the annotation appears in above the alignment, where the **background of the cell** is colored to correspond to the first row of basepair annotations, the **text of the cell** is colored when a basepair is listed in the second row of basepair annotations and the **border of the cell** corresponds to basepair annotations in the third row. The coloring corresponds whether the base participates in a basepair interaction that is isosteric (green), non-isosteric (pink) or not allowed (cyan) when compared to the Reference Sequence. 

.. image:: ../images/evaluate_3d_structure.png
    :align: center
    :height: 200px