# Experimental Data Database Documentation

## Introduction

The experimental data database is esign to store and manage experimental data obtained from scientific experiments. The database cosists of three main tables:

1. Experiment

2. ExperimentVariable

3. ExperimentVariableValue

These tables capture the essential information related to experiments, variables, and their corresponding values.

## Table Descriptions

### 1. Experiment Table

The Experiment table represents a single experiment conducted in the laboratory. It stores the following information:

- `date` (DateTime): The date and time when the experiment was conducted.

- `author` (CharField): The name of the author who performed the experiment.

- `supervisor` (CharField): The name of the supervisor overseeing the experiment.

- `laboratory` (CharField): The laboratory where the experiment took place.

- `substrate`(ForeignKey to Substrate): The substrate used in the experiment.

- `microorganism`(ForeignKey to Microorganism): The microorganism used in the experiment.

- `product`(ForeignKey to Product): The product used in the experiment.

- `experiment_type` (CharField): The type of experiment conducted, chosen from a predefined set of options.

- `observations` (TextField): Any additional observations or notes related to the experiment.

### 2. ExperimentVariable Table

The ExperimentVariable table contains metadata associated with the experimental variables measured in an experiment. It stores the following information:

- `experiment` (ForeignKey to Experiment): The experiment to which the variable belongs.

- `variable_name` (CharField): The name of the variable.

- `variable_unit` (CharField): The units of measurement for the variable.

- `variable_type` (CharField): The type of variable, either discrete or continuous.

- `detection_method` (CharField): The method used to detect or measure the variable.

- `observations` (TextField): Any additional observations or notes related to the variable.

## 3. ExperimentVariableValue Table

The ExperimentVariableValue table stores the actual set of values for each experiment variable. It contains the following information:

- `variable` (ForeignKey to ExperimentVariable): The variable to which the value belongs.

- `value` (FloatField): The measured value of the variable.

- `value_type` (CharField): Indicates whether the value is measured or obtained from literature.

## Table Relationships

1. Experiment to ExperimentVariable (One-to-Many):

- An experiment can have multiple variables.

- The ExperimentVariable table has a foreign key reference to the Experiment table, linking each variable to its corresponding experiment.

2. ExperimentVariable to ExperimentVariableValue (One-to-Many):

- Each variable can have multiple values.
- The ExperimentVariableValue table has a foreign key reference to the ExperimentVariable table, linking each value to its corresponding variable.

## Conclusion

The experimental data database provides a structured approach to store and manage experimental data. The Experiment, ExperimentVariable, and ExperimentVariableValue tables capture the necessary information about experiments, variables, and their values. The relationships between these tables allow for efficient retrieval and analysis of experimental data.
