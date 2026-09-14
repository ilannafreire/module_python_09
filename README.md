# Python Module 09 — The Observatory: Data Validation Systems

This project is part of the 42 School Common Core and focuses on data validation,
structured modeling, and business rule enforcement using Python.

Building on previous modules, this project introduces advanced concepts such as
data validation frameworks, schema enforcement, and real-world data integrity
rules.

The goal of this module is to understand and apply:

- data modeling with pydantic
- field validation using constraints (Field)
- advanced validation using @model_validator
- handling complex data relationships (nested models)
- enum usage for controlled values
- error handling and validation feedback
- clean architecture for data pipelines

Each exercise simulates a real-world system where data must be validated before
use, resulting in a robust data validation pipeline.

---

## Table of Contents

- [Python Module 09 — The Observatory: Data Validation Systems](#python-module-09--the-observatory-data-validation-systems)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Exercises Overview](#exercises-overview)
    - [Exercise 0 — Space Station Validation](#exercise-0--space-station-validation)
    - [Exercise 1 — Alien Contact Protocol](#exercise-1--alien-contact-protocol)
    - [Exercise 2 — Space Mission Control](#exercise-2--space-mission-control)
  - [Key Learning Points](#key-learning-points)
  - [Best Practices](#best-practices)
  - [Notes](#notes)

---

## Project Structure

```text
ex0/
└── space_station.py

ex1/
└── alien_contact.py

ex2/
└── space_crew.py

data_generator.py
data_exporter.py
extracted/
```

---

## Exercises Overview

### Exercise 0 — Space Station Validation

Introduces structured data validation using Pydantic models.

- Defines a SpaceStation model
- Validates fields using:
	- string length constraints
	- numeric ranges (ge, le)
	- required timestamps
	- optional notes with limits
- Handles validation errors safely

Concepts: data validation, schema definition, field constraints

Built using BaseModel and Field.

---

### Exercise 1 — Alien Contact Protocol

Focuses on advanced validation logic and conditional rules.

- Introduces Enum for controlled values (ContactType)
- Implements complex validation using @model_validator
- Applies rules such as:
	- ID format enforcement
	- conditional validation based on contact type
	- cross-field dependency validation
	- minimum witness requirement for telepathic contact

Concepts: business logic validation, enums, conditional constraints

Uses @model_validator(mode="after") for full-object validation.

---

### Exercise 2 — Space Mission Control

Implements nested models and complex validation scenarios.

- Defines multiple models:
	- CrewMember
	- SpaceMission
- Uses nested data structures (list[CrewMember])
- Validates:
	- crew composition and leadership requirements
	- mission duration constraints
	- staff experience thresholds for long missions
	- active crew status

Concepts: nested validation, aggregation rules, system integrity

Demonstrates real-world data validation pipelines.

---

## Key Learning Points

- pydantic simplifies robust data validation
- data integrity must be enforced at model level
- validation can go beyond fields into full object logic
- enums prevent invalid categorical data
- nested models reflect real-world structured data
- clean validation logic improves maintainability

---

## Best Practices

- always validate external or user-provided data
- use clear and explicit constraints (Field)
- keep validation logic readable and separated
- avoid side effects in validation functions
- prefer returning validated objects instead of raw data
- handle validation errors gracefully

---

## Notes

- written for Python 3.10+
- uses type hints and follows flake8 standards
- focuses on data integrity and validation patterns
- designed to simulate real-world backend and data engineering scenarios
- includes support files for generating and exporting sample validation data