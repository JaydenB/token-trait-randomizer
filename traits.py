import os
import json
import time
import random


class TraitGenerator(object):
    def __init__(self):
        # Storing all loaded in Trait data
        self.traits_raw = {}
        self.traits = {}
        self.traits_weights = {}
        self.real_weights = {}
        self.traits_max = 0

        self.orig_filepath = ""

        # Storing Generated Trait Tokens
        self.generated_trait_tokens = []
        self.sorted_trait_tokens = None

    # ----- Saving and Loading -----------------------------------------------------------
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
            self.traits_raw[trait] = traits[trait]
            self.traits[trait] = traits[trait].get('values', [])
            self.traits_weights[trait] = traits[trait].get('weights', [])
            self.real_weights[trait] = [0 for x in traits[trait].get('weights', [])]
        print(f"{len(self.traits)} traits loaded from '{filepath}'.")

    def save_to_file(self, filepath: str) -> None:
        # Generate All In One File
        saving_dict = {}
        for trait_token in self.generated_trait_tokens:
            saving_dict[trait_token[0]] = {"rarity": trait_token[1], "traits": trait_token[2]}
        save_dict_to_file(saving_dict, f"{filepath}generated_all_in_one.json")

        # Generate Rarity File
        rarity_dict = {}
        for trait_token in self.generated_trait_tokens:
            rarity_dict[trait_token[0]] = {"rarity": trait_token[1]}
        save_dict_to_file(rarity_dict, f"{filepath}generated_rarity_list.json")

        # Save Individual Files
        for trait_token in self.generated_trait_tokens:
            trait_dict = {"traits": trait_token[2]}
            save_dict_to_file(trait_dict, f"{filepath}{trait_token[0]}.json")

        # Generate Real Weights
        save_dict_to_file(self.calculate_real_weights(),
                          f"{filepath}generated_real_weights.json")

    # ----- Generator --------------------------------------------------------------------
    def generate_trait_token(self) -> dict:
        token = {}
        for trait in self.traits:
            # Skip trait if it is to run after all token generation
            # Prevents things being too similar
            if self.traits_raw[trait].get('last', False):
                continue

            # Select a random value for the trait
            token[trait] = random.choices(self.traits[trait],
                                          weights=self.traits_weights[trait],
                                          k=1)[0]
        return token

    def generate_last_trait_token(self, token: dict) -> dict:
        new_token = token.copy()
        for trait in self.traits:
            # Skip if we have already generated it (not marked as last)
            if not self.traits_raw[trait].get('last', False):
                continue

            new_token[trait] = random.choices(self.traits[trait],
                                              weights=self.traits_weights[trait],
                                              k=1)[0]

        return new_token

    def generate(self, count: int = 1, seed: int = 0) -> None:
        start_time = time.time()

        random.seed(seed)

        max_tokens = self.max_tokens_from_traits()
        if max_tokens < count:
            print("Count is too high for number of traits. Limiting to Max.")
            count = max_tokens

        print(f"Starting generation of {count}/{max_tokens} trait tokens!")
        # print(f"Progress: 1/{count} {progress_bar(0.0)}", end="")

        # Generate Initial Tokens
        tokens = []
        for i in range(count):
            print(f"Progress: {i+1}/{count} {progress_bar(float(i / count))}", end="\r")

            # Search for a token that has not already been generated
            new_token = self.generate_trait_token()
            while new_token in tokens:
                new_token = self.generate_trait_token()
            tokens.append(new_token)

        print("\nFinishing up Tokens.")

        # Generate 'Last' Token Traits
        last_tokens = []
        for token in tokens:
            new_token = self.generate_last_trait_token(token)
            while new_token in last_tokens:
                new_token = self.generate_last_trait_token(token)
            last_tokens.append(new_token)

        # Generate Rarities
        for i, token in enumerate(last_tokens):
            # Update Real Weights to track final rarity of each trait
            self.update_real_weights(token)

            # Add to our list of generated tokens
            self.generated_trait_tokens.append([i, self.token_rarity(token), token])

        # Sort Generated Tokens based on their rarity indicator
        self.sorted_trait_tokens = sorted(
            self.generated_trait_tokens, key=lambda x: x[1], reverse=False)

        print(f"\n---------- Completed Trait Generation in "
              f"{round(time.time() - start_time, 2)} seconds. ----------\n")

    def calculate_real_weights(self) -> dict:
        d = {}
        for trait in self.real_weights:
            d[trait] = {}
            for i, a in enumerate(self.real_weights[trait]):
                generated = round((a / sum(self.real_weights[trait])) * 100.0, 2)
                d[trait][self.traits[trait][i]] = \
                    {"original": self.traits_weights[trait][i], "generated": generated}
        return d

    # ----- Printing for Debug -----------------------------------------------------------
    def top_rarity(self, count: int = 10) -> str:
        if self.sorted_trait_tokens is None:
            return "No data generated yet! Cancelling Top Rarity Print."

        msg = f"Top {count} Rarity items:"
        for i in range(count):
            msg += f"\n\t#{i}: index-{self.sorted_trait_tokens[i][0]} " \
                   f"{self.sorted_trait_tokens[i][1]}r\t" \
                   f"{self.sorted_trait_tokens[i][2]}"
        return f"{msg}"

    def bottom_rarity(self, count: int = 10) -> str:
        if self.sorted_trait_tokens is None:
            return "No data generated yet! Cancelling Bottom Rarity Print."

        reversed_sorted = list(reversed(self.sorted_trait_tokens))

        msg = f"\nBottom {count} Rarity items:"
        for i in range(count):
            msg += f"\n\t#{len(reversed_sorted)-1-i}: index-{reversed_sorted[i][0]} " \
                   f"{reversed_sorted[i][1]}r\t" \
                   f"{reversed_sorted[i][2]}"
        return f"{msg}\n"

    # ----- Utilities --------------------------------------------------------------------
    def update_real_weights(self, token: dict) -> None:
        for trait in token:
            self.real_weights[trait][self.index_of_trait(token, trait)] += 1

    def index_of_trait(self, token, trait) -> int:
        return self.traits[trait].index(token[trait])

    def token_rarity(self, token) -> int:
        return sum([self.traits_weights[trait][self.index_of_trait(token, trait)]
                    for trait in self.traits])

    def max_tokens_from_traits(self) -> int:
        m = 1
        for trait in self.traits:
            if self.traits_raw[trait].get('last', False):
                continue
            m *= len(self.traits[trait])
        return m

    def dict_check(self, token: dict) -> bool:
        for trait_token in self.generated_trait_tokens:
            if token == trait_token[2]:
                return True
        return False


# ----- File Saving and Loading Utilities ------------------------------------------------

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
        # print(f"Saved data to '{file_path}'.")
    except:
        print(f"Error on saving data to '{file_path}'.")


def progress_bar(percentage: float, bar_count: int = 25) -> str:
    progress_ascii_style = ["░", "▒", "█"]
    iteration = bar_count / 1.0
    filled = bar_count - int(iteration * (1.0 - percentage))
    progress_bar = [progress_ascii_style[2] for i in range(filled)] + \
                   [progress_ascii_style[0] for i in range(bar_count - filled)]
    return ''.join(progress_bar)


# ----- Run Function ---------------------------------------------------------------------

def run(input_filepath: str, output_filepath: str, count: int,
        seed: int = 0, print_rarities: int = 0, dry_run: bool = False) -> None:
    generator = TraitGenerator()
    generator.load_traits(filepath=input_filepath)

    generator.generate(count=count, seed=seed)

    if not dry_run:
        generator.save_to_file(filepath=output_filepath)
        print("Files saved.\n")

    if print_rarities > 0:
        print(generator.top_rarity(count=print_rarities))
        print(generator.bottom_rarity(count=print_rarities))


# ----- Main for CLI ---------------------------------------------------------------------

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    # Positional Arguments
    parser.add_argument("input",
                        help="Input File Path to traits .json file.", type=str)

    # Optional Arguments
    parser.add_argument("-o", "--output",
                        help="Output Directory Path for Generated Tokens.",
                        type=str, default="")
    parser.add_argument("-c", "--count",
                        help="Final Token Count. Caps at Max from Input Traits.",
                        type=int, default=1)
    parser.add_argument("-s", "--seed",
                        help="Seed for Random Generation.",
                        type=int, default=0)
    parser.add_argument("-pr", "--printrarities",
                        help="Number of Top/Bottom Rarities to print out after generation.",
                        type=int, default=0)
    parser.add_argument("-dr", "--dryrun",
                        help="Dry Run. Doesn't generate files after generation.",
                        action="store_true")

    args = parser.parse_args()

    run(input_filepath=args.input,
        output_filepath=args.output,
        count=args.count,
        seed=args.seed,
        print_rarities=args.printrarities,
        dry_run=args.dryrun)
