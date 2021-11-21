import traits

FILE_PATH = "examples/example_traits.json"
TOKEN_COUNT = 1111

SEED = 0

if __name__ == '__main__':
    traits.run(
        input_filepath=FILE_PATH,
        output_filepath="generated/",
        count=TOKEN_COUNT,
        seed=SEED,
        print_rarities=10,
        dry_run=True
    )
