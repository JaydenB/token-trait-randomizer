# Token Traits Randomizer
Generalised randomizer for generating traits with no repeated tokens.

-----
CLI Commands:

```
python3 traits.py -h
---------------------------------------------------------------------------------------
usage: traits.py [-h] [-o OUTPUT] [-c COUNT] [-s SEED] [-pr PRINTRARITIES] [-dr] input

positional arguments:
  input                 Input File Path to traits .json file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output Directory Path for Generated Tokens.
  -c COUNT, --count COUNT
                        Final Token Count. Caps at Max from Input Traits.
  -s SEED, --seed SEED  Seed for Random Generation.
  -pr PRINTRARITIES, --printrarities PRINTRARITIES
                        Number of Top/Bottom Rarities to print out after generation.
  -dr, --dryrun         Dry Run. Doesn't generate files after generation.
```

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
