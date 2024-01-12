# Talk about Pydantic


Talk about Pydantic, and why I think it is one of the greatest Python package ever!

## Why do I like it?
- developer ergonomics
- enforce type hints at runtime
- validating the data in a model


## Is Pydantic safe to use or depend on?
- most widely used data validation library for Python
- backed by a team that cares about quality, look at the documentation or code base
- quality and open sourced code which can be found [here](https://github.com/pydantic/pydantic)
- more then 10.000 other repositories on Github have a dependency on it
- most popular REST API framework, FastAPI, is built around Pydantic
- many companies are using [Pydantic](https://docs.pydantic.dev/latest/#who-is-using-pydantic)
- the team takes care of [issues](https://github.com/pydantic/pydantic/issues)
- started by [Samual Colvin](https://github.com/samuelcolvin) who is now building a company around it
- currently on track to make it faster by utilizing PyO3, even onboarded David Hewitt (maintainer of PyO3)

## Where do I use it?
- all over the place



The talk is one where I spend all the time in the IDE and walk people through the scenarios listed below.

Just run them using:
```
ipython .\examples\00_base_example.py
python .\examples\00_base_example.py
```

### 00: base example on creating an instance of a Pydantic class

The same developer ergonomics as with dataclasses.

Has IDE-completion and a lot of other things out of the box, like a JSON serializer and a method to convert it to a dict.

### 01: high level comparison between Pydantic and dataclass

Both are a nice way of laying out structures of data. Better than a dict, as both offer IDE-completion and mypy can validate the types throughout your application.

The really nice thing about Pydantic is the type hint validation at runtime. 

A dataclass can really be instantiated with anything, a Pydantic BaseModel will throw a validation error. Nice for input from other applications, like when offering an API or CLI.

### 02: emphasize nested models are created 'automagically'

Fields in a model are defined with a type. Pydantic will coerce input data into that type. If that type is also a BaseModel, that type will also be instantiated and the validations for that model will run.

Observe the Pydantic example. The nested Suitcase is actually of the type Suitcase. In the dataclass example, it is not coerced and it is a dict.

### 03: embedding an Enum to restrict choices

Enums used in the BaseModel are enforced. 
Input strings are coerced into the Enum and validated as such.

### 04: using Enum values instead of the Enum

When converting to dict, you can choose to emit strings or the string representation of the actual enum.

### 05: validation of data

Adding additional validators is easy, really easy!

You point the `validator` at a field and then write a method to validate the semantics. During object instantiation, you have access to the value and you can do all the things Python. Write assertions and checks, do a lookup in a database etc.



### 06: pre and post validation of data

Using `before` validators, you can massage input data into something.

Before validator: run before Pydantic's internal parsing and validation
After validator: run after Pydantic's internal parsing and validation

There are more.

### 07: validate and compare all fields of a model, pre and post

You can validate values of multiple fields in 1 method that is decorated with the `model_validator`. You access fields with `self` and you can do all the comparisons you like while evalutin all the values.

### 08: dynamic model creation

Never used it. Some people love it, so I wanted to mention it.

### 09: coercion of data and strict mode

Usually, it is great that this is happening. Python coerces a type into something that it can be. In the example, we convert string values into an Enum, a UUID and into an IP address. The string values are used to actually instantiate those instances.

This also works when you have fields that are of the type BaseModel. Those will be instantiated and those will also run their own validation logic.


In case you do not like this, you can turn it off with strict mode.

### 10: aliasing when serializing

- `serialization_alias`: serialize external fields into the fields you like. Example: Camelcase to snake case.
- `alias`: when serializing snake_case, convert it into CamelCase.
- `validation_alias`: take in Camelcase, but do not use it or emit it anywhere.

### 11: emphasizing it can be used like other classes

Turning a class into a Pydantic BaseModel does not mean you should or can only use the class for data validation. 

The BaseModel still does all the things Python.