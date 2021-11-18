# Token Traits Randomizer
Generalised randomizer for generating traits with no repeated tokens.

1) Please keep a "generated" folder in the same directory as `traits.py`
2) Update `run.py` to include your `.json` _Traits File_ and how many tokens you want to generate.

-----

Traits Example File Structure: *(`values` and `weights` must have equal list length)*
````
{
    "traits": {
        "Trait Name": {
            "values": ["Small", "Medium", "Large"]
            "weights": [10, 60, 30]
        }
    }
}
````

-----

_No dependencies required outside of Python 3.x_ 
_(Only tested in Python 3.8)_