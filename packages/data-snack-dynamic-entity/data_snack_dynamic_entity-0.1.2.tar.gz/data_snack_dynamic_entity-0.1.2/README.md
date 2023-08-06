# Data Snack - Dynamic entity 

# About
Used to dynamically load `data-snack` `Entity` objects from json schema.
Especially useful for complex dataset with many fields.

## Install
Data Snack can be easily installed using pypi repository.
```bash
pip install data_snack_dynamic_entity
```

## Usage
### 1. Define Entity template 
First you need to define a dictionary containing the template - a configuration for your Entity type.
Template should contain:
- the name of the new Entity type and its properties
- each property should have:
  - `type` - type of the field
  - `default` - default value (optional property) 
  - `optional` - true if the field is optional (optional property)

Notice that your template can be saved in any file of your choosing.
Just make sure it's later parsed to a dictionary in the right format.

The template is defined using following schema: `src/data_snack_dynamic_entity/entityTemplates.schema.json`.

#### Example
```python
{
    "Car": {
        "properties": {
            "name": {
                "type": "str"
            },
            "cost": {
                "type": "float",
                "default": 10.0,
                "optional": True
            }
        }
    }
}
```

### 2. Load the template and create new types
Now you are ready to create entities based on your template:
```python
from data_snack_dynamic_entity.factory import load_entities

entities = load_entities(templates=your_config)
```

After that `entities` will contain a dictionary in the following format:
```python
{
    "entity_name": EntityType
}
```

# Contact
Plugin was created by the Data Science team from [Webinterpret](https://www.webinterpret.com/).
