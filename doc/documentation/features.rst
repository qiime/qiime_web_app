.. _features:


===================
Structural Features
===================

Annotate Features
-------------------------------------------------------
If the user uploaded a tab-delimited feature list, they should see Structural Features Tab above the alignment.  Within that tab, there is an "Annotate Features" button, which will annotate the alignment according to the supplied basepair list.  Before clicking on that button, the user must select  a Reference Sequence. For information on selecting the Reference Sequence, see :ref:`select_reference`. Once the Reference Sequence is set, the user can click the "Annotate Features" button under the Structural Features Tab.  

.. image:: ../images/annotate_features.png
    :align: center
    :height: 200px

The alignment will be annotated with the descriptive names defined in the features file. Since the descriptive names may be long, the are trimmed to one character, however; the user can mouseover the letter to see the full name.

.. image:: ../images/feature_acceptor.png
    :align: center
    :height: 55px

Show/Hide Features
-------------------
Now that the alignment has been annotated with the features, the user can select specific features from the multi-select box (e.g. D_loop), then select the "Show/Hide Features" button to collapse the alignment horizontally.

.. image:: ../images/feature_select_dloop.png
    :align: center
    :height: 200px

When inspecting the alignment, the user should notice that the D_loop is not missing from the alignment. The user can click the "Show/Hide Features" button again to make the D_loop reappear.

.. image:: ../images/feature_minus_dloop.png
    :align: center
    :height: 90px
