# Token Traits Randomizer
Generalised randomizer for generating traits with no repeated tokens.

1) Please keep a "generated" folder in the same directory as `traits.py`
   - This is where all generated data is saved too and no current processes exist to fix this if it doesn't exist.
2) Update `run.py` to include your `.json` _Traits File_ and how many tokens you want to generate.
3) All `weights` for a trait add up to 100, can be floats, and the former is important! Otherwise your generated weights will differ!

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
