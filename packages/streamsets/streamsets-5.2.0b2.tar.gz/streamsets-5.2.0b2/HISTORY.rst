History
=======
5.1.0 (December 2022)
---------------------
* Support for StreamSets Advanced Query Language has been added for Pipelines, Fragments, and Jobs. Refer
  to the :ref:`StreamSets SDK Search Documentation <search_for_objects>` for further details.

* The :py:meth:`streamsets.sdk.ControlHub.engines.get_all` method now supports filtering by the ``id`` parameter.

* Bug fixes and improvements.

5.0.0 (August 2022)
-------------------
* The :py:meth:`streamsets.sdk.ControlHub.validate_pipeline` method now supports validating SDC and Transformer
  pipelines.

* Changing the name of a :py:class:`streamsets.sdk.sch_models.Pipeline` instance is now possible by setting the ``name``
  attribute of the instance and passing it to :py:meth:`streamsets.sdk.ControlHub.publish_pipeline`.

* Improved the usability of the :py:class:`streamsets.sdk.sch_models.ApiCredentialBuilder` class and its interaction
  with the :py:meth:`streamsets.sdk.ControlHub.add_api_credential` method.

  .. note::
    Please refer to the documentation for the correct, updated usage.

* The :py:class:`streamsets.sdk.sch_models.User` and :py:class:`streamsets.sdk.sch_models.Group` classes have received
  several improvements including:

  * The :py:attr:`streamsets.sdk.sch_models.User.groups` and :py:attr:`streamsets.sdk.sch_models.Group.users` attributes
    have been improved to return :py:class:`streamsets.sdk.sch_models.Group` and :py:class:`streamsets.sdk.sch_models.User`
    instances (respectively) rather than just ID values.

  .. warning::
     This will affect existing SDK usage of the :py:attr:`streamsets.sdk.sch_models.User.groups` and
     :py:attr:`streamsets.sdk.sch_models.Group.users` attributes. Please refer to the documentation for the correct,
     updated usage.

* The :py:class:`streamsets.sdk.sch_models.DataCollector` and :py:class:`streamsets.sdk.sch_models.Transformer` classes
  have been refactored into a single class which houses the functionality for both:
  :py:class:`streamsets.sdk.sch_models.Engine`. Subsequently, the :py:attr:`streamsets.sdk.ControlHub.data_collectors`
  and :py:attr:`streamsets.sdk.ControlHub.transformers` attributes now utilize the :py:class:`streamsets.sdk.sch_models.Engines`
  class instead.

  .. warning::
     This will affect existing SDK usage of the :py:attr:`streamsets.sdk.ControlHub.data_collectors` and
     :py:attr:`streamsets.sdk.ControlHub.transformers` attributes, as these will both now return instances of the
     :py:class:`streamsets.sdk.sch_models.Engine` class. Please refer to the documentation for the correct,
     updated usage.

* Pagination improvements have been made for various classes

* When retrieving :py:class:`streamsets.sdk.sch_models.Job` instances via :py:attr:`streamsets.sdk.ControlHub.jobs` and supplying a ``job_tag`` value, including the organization that the job tag belongs to is no longer required.
  
  .. warning::
     This will affect existing SDK usage of the :py:attr:`streamsets.sdk.ControlHub.jobs` attribute. Please refer to the documentation for the correct, updated usage.

* Arguments and attributes that were marked as deprecated in the previous release have been removed.

* Bug fixes and improvements


4.3.0 (August 2022)
-------------------
* Added support for using the SDK on Python 3.10

* :py:class:`streamsets.sdk.sch_models.Users` and :py:class:`streamsets.sdk.sch_models.Groups` instances can now be
  filtered on specific text values via the ``filter_text`` parameter, as seen in the UI

* Bug fixes and improvements


4.2.1 (July 2022)
-----------------
* Fixes a bug when trying to modify or update a :py:class:`streamsets.sdk.sch_models.ACL` definition for :py:class:`streamsets.sdk.sch_models.Deployment`
  instances.

* Fixes a bug in the naming convention used for pipelines created via the :py:meth:`streamsets.sdk.ControlHub.test_pipeline_run`
  method.

* Fixes a bug that prevented users from supplying a ``'.'`` (period) character in the ``group_id`` when creating a group
  via the :py:meth:`streamsets.sdk.sch_models.GroupBuilder.build` method.


4.2.0 (May 2022)
----------------
* Programmatic User creation and management has been added

* Pagination and "lazy" loading improvements have been made to various classes

* The Group class has been refactored slightly to better match the experience seen in the UI

.. note::
  When filtering the :py:class:`streamsets.sdk.sch_models.Groups` objects in DataOps Platform, the ``id`` argument has
  been replaced by ``group_id`` to match the :py:class:`streamsets.sdk.sch_models.Group` class's representation. Please
  refer to the documentation for the correct, updated usage.

* The :py:meth:`streamsets.sdk.sch_models.DeploymentBuilder.build` and :py:meth:`streamsets.sdk.sch_models.EnvironmentBuilder.build`
  methods no longer require the ``deployment_type`` or ``environment_type`` arguments to be supplied

.. warning::
  The ``deployment_type`` and ``environment_type`` arguments are deprecated and will be removed in a future release.
  Please refer to the documentation for the correct, updated usage.

* The :py:class:`streamsets.sdk.sch_models.Deployments` and :py:class:`streamsets.sdk.sch_models.Environments` classes
  can now be filtered on ``deployment_id`` and ``environment_id`` respectively, instead of ``id``

.. warning::
  The ``id`` argument has been deprecated and will be removed in a future release. Please refer to the documentation for
  the correct, updated usage.


4.1.0 (March 2022)
--------------------
* Modified error handling to return all errors returned by an API call to DataOps Platform

* Transformer for Snowflake support

* Support for nightly builds of execution engines


4.0.0 (January 2022)
--------------------
* Activation key is no longer required

* DataCollector and Transformer classes are no longer public because these are headless engines in StreamSets DataOps Platform

* Authentication is now handled using API Credentials

* The usage and syntax for PipelineBuilder has been updated

* Support for environments and deployments

