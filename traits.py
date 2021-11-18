import os
import json
import time
import random


class TraitGenerator(object):
    def __init__(self, debug: bool = True):
        self.debug_mode = debug

        # Storing all loaded in Trait data
        self.traits = {}
        self.traits_weights = {}
        self.real_weights = {}
        self.traits_max = 0

        self.orig_filepath = ""

        # Storing Generated Trait Tokens
        self.generated_trait_tokens = []
        self.sorted_trait_tokens = None

    # ----- Saving and Loading -----------------------------------------------------------------------------------------
    def load_traits(self, filepath: str) -> None:
        self.orig_filepath = os.path.splitext(filepath)[0]

        # Sanity Check for Existence
        if not os.path.isfile(filepath):
            print(f"File '{filepath}' does not exist. Cancelling.")
            return

        file_data = load_dict_from_file(filepath)
        if file_data is None:
            print(f"Error in loading '{filepath}' data.")
            return

        traits = file_data.get('traits', {})
        for trait in traits:
            self.traits[trait] = traits[trait].get('values', [])
            self.traits_weights[trait] = traits[trait].get('weights', [])
            self.real_weights[trait] = [0 for x in traits[trait].get('weights', [])]
        print(f"{len(self.traits)} traits loaded from '{filepath}'.\n")

    def save_to_file(self) -> None:
        # Generate All In One File
        saving_dict = {}
        for trait_token in self.generated_trait_tokens:
            saving_dict[trait_token[0]] = {"rarity": trait_token[1], "traits": trait_token[2]}
        save_dict_to_file(saving_dict, f"generated/{self.orig_filepath}_all_in_one.json")

        # Generate Rarity File
        rarity_dict = {}
        for trait_token in self.generated_trait_tokens:
            rarity_dict[trait_token[0]] = {"rarity": trait_token[1]}
        save_dict_to_file(rarity_dict, f"generated/{self.orig_filepath}_rarity_list.json")

        # Save Individual Files
        for trait_token in self.generated_trait_tokens:
            trait_dict = {"traits": trait_token[2]}
            save_dict_to_file(trait_dict, f"generated/{trait_token[0]}.json")

        # Generate Real Weights
        save_dict_to_file(self.calculate_real_weights(), f"generated/{self.orig_filepath}_real_weights.json")

    # ----- Generator --------------------------------------------------------------------------------------------------
    def generate_trait_token(self) -> dict:
        token = {}
        for trait in self.traits:
            token[trait] = random.choices(self.traits[trait], weights=self.traits_weights[trait], k=1)[0]
        return token

    def generate(self, count: int = 1) -> None:
        start_time = time.time()

        max_tokens = self.max_tokens_from_traits()
        if max_tokens < count:
            print("Count is too high for number of traits. Limiting to Max.")
            count = max_tokens

        print(f"Starting generation of {count}/{max_tokens} trait tokens!")

        # Initiate Core Loop
        for i in range(count):
            # Search for a token that has not already been generated
            new_token = self.generate_trait_token()
            while self.dict_check(new_token):
                new_token = self.generate_trait_token()

            # Update Real Weights to track final rarity of each trait
            self.update_real_weights(new_token)

            # Add to our list of generated tokens
            self.generated_trait_tokens.append([i, self.token_rarity(new_token), new_token])

            if self.debug_mode:
                print(f"\tGenerated #{i}: {new_token}")

        # Sort Generated Tokens based on their rarity indicator
        self.sorted_trait_tokens = sorted(self.generated_trait_tokens, key=lambda x: x[1], reverse=False)

        print(f"\n---------- Completed Trait Generation in {round(time.time() - start_time, 2)} seconds. ----------\n")

    def calculate_real_weights(self) -> dict:
        print("\n----- Calculated Real Weights -----")
        d = {}
        for trait in self.real_weights:
            d[trait] = {}
            print(f"\nTrait: {trait}")
            for i, a in enumerate(self.real_weights[trait]):
                generated = round((a / sum(self.real_weights[trait])) * 100.0, 2)
                d[trait][self.traits[trait][i]] = {"original": self.traits_weights[trait][i], "generated": generated}
                print(f"\tExpected: {self.traits_weights[trait][i]}% ---> Generated: {generated}%")
        print("")
        return d

    # ----- Printing for Debug -----------------------------------------------------------------------------------------
    def top_rarity(self, count: int = 10) -> str:
        if self.sorted_trait_tokens is None:
            return "No data generated yet! Cancelling Top Rarity Print."

        msg = f"Top {count} Rarity items:"
        for i in range(count):
            msg += f"\n\t{i}: #{self.sorted_trait_tokens[i][0]} " \
                   f"{self.sorted_trait_tokens[i][1]}%\t" \
                   f"{self.sorted_trait_tokens[i][2]}"
        return f"{msg}"

    def bottom_rarity(self, count: int = 10) -> str:
        if self.sorted_trait_tokens is None:
            return "No data generated yet! Cancelling Bottom Rarity Print."

        reversed_sorted = list(reversed(self.sorted_trait_tokens))

        msg = f"\nBottom {count} Rarity items:"
        for i in range(count):
            msg += f"\n\t{i}: #{reversed_sorted[i][0]} " \
                   f"{reversed_sorted[i][1]}%\t" \
                   f"{reversed_sorted[i][2]}"
        return f"{msg}\n"

    # ----- Utilities --------------------------------------------------------------------------------------------------
    def update_real_weights(self, token: dict) -> None:
        for trait in token:
            self.real_weights[trait][self.index_of_trait(token, trait)] += 1

    def index_of_trait(self, token, trait) -> int:
        return self.traits[trait].index(token[trait])

    def token_rarity(self, token) -> int:
        return sum([self.traits_weights[trait][self.index_of_trait(token, trait)] for trait in self.traits])

    def max_tokens_from_traits(self) -> int:
        m = 1
        for trait in self.traits:
            m *= len(self.traits[trait])
        return m

    def dict_check(self, token: dict) -> bool:
        return token in self.generated_trait_tokens


def load_dict_from_file(file_path: str) -> dict:
    try:
        with open(file_path) as _file:
            return json.load(_file)
    except:
        print("An error occurred loading '%s'.\nPlease restart and try again" % file_path)
    return {}


def save_dict_to_file(d: dict, file_path: str) -> None:
    try:
        with open(file_path, 'w') as _file:
            _file.write(json.dumps(d))
        print(f"Saved data to '{file_path}'.")
    except:
        print(f"Error on saving data to '{file_path}'.")
