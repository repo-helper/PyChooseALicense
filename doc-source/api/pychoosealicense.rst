=========================
:mod:`pychoosealicense`
=========================

.. autosummary-widths:: 4/10


.. automodule:: pychoosealicense
	:no-members:
	:autosummary-members:

.. autofunction:: pychoosealicense.get_license

.. autosummary-widths:: 3/10

.. autoclass:: pychoosealicense.License

The :attr:`~.License.content` attribute of :class:`~.License` can be populated with project-specific metadata using the :meth:`str.format` method:

.. code-block:: python

	l = get_license("MIT")
	l.format(year=2021, fullname="Dominic Davis-Foster")

The supported fields as as follows. Note that not all licenses support all fields.

* **fullname** -- The full name or username of the repository owner
* **login** -- The repository owner's username
* **email** -- The repository owner's primary email address
* **project** -- The repository name
* **description** -- The description of the repository
* **year** -- The current year
* **projecturl** -- The repository URL or other project website
