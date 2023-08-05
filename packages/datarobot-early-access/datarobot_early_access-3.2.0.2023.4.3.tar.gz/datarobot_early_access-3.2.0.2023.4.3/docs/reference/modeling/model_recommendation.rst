.. _model_recommendation:

####################
Model Recommendation
####################

During the Autopilot modeling process, DataRobot will recommend a model for deployment based on its accuracy and complexity.

When running Autopilot in Full or Comprehensive mode, DataRobot uses the following deployment preparation process:

1. First, DataRobot calculates **Feature Impact** for the selected model and uses it to generate a reduced feature list.
2. Next, DataRobot retrains the selected model on the reduced feature list. If the new model performs better than the original model, DataRobot uses the new model for the next stage. Otherwise, the original model is used.
3. DataRobot then retrains the selected model at an up-to-holdout sample size (typically 80%). As long as the sample is under the frozen threshold (1.5GB), the stage is not frozen.
4. Finally, DataRobot retrains the selected model as a frozen run (hyperparameters are not changed from the up-to-holdout run) using a 100% sample size and selects it as **Recommended for Deployment**.

.. note::
	The higher sample size DataRobot uses in Step 3 is either:

	1. **Up to holdout** if the training sample size *does not* exceed the maximum Autopilot size threshold: sample size is the training set plus the validation set (for TVH) or 5-folds (for CV). In this case, DataRobot compares retrained and original models on the holdout score.
	2. **Up to validation** if the training sample size *does* exceed the maximum Autopilot size threshold: sample size is the training set (for TVH) or 4-folds (for CV). In this case, DataRobot compares retrained and original models on the validation score.

DataRobot gives one model the *Recommended for Deployment** badge. This is the most accurate individual, non-blender model on the Leaderboard. After completing the steps described above, it will receive the **Prepared for Deployment** badge.

Retrieve all recommendations
----------------------------

The following code will return all models recommended for the project.

.. code-block:: python

	import datarobot as dr

	recommendations = dr.ModelRecommendation.get_all(project_id)

Retrieve a default recommendation
---------------------------------

If you are unsure about the tradeoffs between the various types of recommendations, DataRobot can make this choice
for you. The following route will return the Recommended for Deployment model to use for predictions for the project.

.. code-block:: python

	import datarobot as dr

	recommendation = dr.ModelRecommendation.get(project_id)

Retrieve a specific recommendation
----------------------------------

If you know which recommendation you want to use, you can select a specific recommendation using the
following code.

.. code-block:: python

	import datarobot as dr

	recommendation_type = dr.enums.RECOMMENDED_FOR_DEPLOYMENT
	recommendations = dr.ModelRecommendation.get(project_id, recommendation_type)

Get recommended model
---------------------

You can use method `get_model()` of a recommendation object to retrieve a recommended model.

.. code-block:: python

	import datarobot as dr

	recommendation = dr.ModelRecommendation.get(project_id)
	recommended_model = recommendation.get_model()
