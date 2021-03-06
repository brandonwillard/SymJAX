.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_examples_plot_interpolation.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_examples_plot_interpolation.py:


Basic 1d interpolation
======================

demonstration on how to perform basic 1d interpolation



.. image:: /auto_examples/images/sphx_glr_plot_interpolation_001.svg
    :alt: nearest-periodic, linear-mirror, linear-periodic, constant-0
    :class: sphx-glr-single-img






.. code-block:: default


    import matplotlib.pyplot as plt

    import symjax
    import symjax.tensor as T

    w = T.Placeholder((3,), "float32", name="w")
    w_interp1 = T.interpolation.upsample_1d(w, repeat=4, mode="nearest")
    w_interp2 = T.interpolation.upsample_1d(
        w, repeat=4, mode="linear", boundary_condition="mirror"
    )
    w_interp3 = T.interpolation.upsample_1d(
        w, repeat=4, mode="linear", boundary_condition="periodic"
    )
    w_interp4 = T.interpolation.upsample_1d(w, repeat=4)

    f = symjax.function(w, outputs=[w_interp1, w_interp2, w_interp3, w_interp4])

    samples = f([1, 2, 3])
    fig = plt.figure(figsize=(6, 6))
    plt.subplot(411)
    plt.plot(samples[0], "xg", linewidth=3, markersize=15)
    plt.plot([0, 5, 10], [1, 2, 3], "ok", alpha=0.5)
    plt.title("nearest-periodic")
    plt.xticks([])

    plt.subplot(412)
    plt.plot(samples[1], "xg", linewidth=3, markersize=15)
    plt.plot([0, 5, 10], [1, 2, 3], "ok", alpha=0.5)
    plt.title("linear-mirror")
    plt.xticks([])

    plt.subplot(413)
    plt.plot(samples[2], "xg", linewidth=3, markersize=15)
    plt.plot([0, 5, 10], [1, 2, 3], "ok", alpha=0.5)
    plt.title("linear-periodic")
    plt.xticks([])

    plt.subplot(414)
    plt.plot(samples[3], "xg", linewidth=3, markersize=15)
    plt.plot([0, 5, 10], [1, 2, 3], "ok", alpha=0.5)
    plt.title("constant-0")

    plt.tight_layout()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.337 seconds)


.. _sphx_glr_download_auto_examples_plot_interpolation.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_interpolation.py <plot_interpolation.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_interpolation.ipynb <plot_interpolation.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
