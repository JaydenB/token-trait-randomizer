# Token Traits Randomizer
Generalised randomizer for generating traits with no repeated tokens.

-----

Traits Example File Structure: *(`values` and `weights` must have equal list length)*
````
{
    "traits": {
        "Trait Name": {
            "values": ["Small", "Medium", "Large"]      # Values the Trait Attribute can be
            "weights": [10, 60, 30]                     # Percentage of Value Weights. Must sum to 100 otherwise rarities might not come out as expected.
            "last": false                               # Optional. Runs this trait after the generic random selection. Example: Prevents the same item with a different background.
        }
    }
}
````

-----

_No dependencies required outside of Python 3.x_
