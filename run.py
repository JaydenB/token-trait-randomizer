import traits

FILE_PATH = "test_traits.json"
TOKEN_COUNT = 1111

if __name__ == '__main__':
    generator = traits.TraitGenerator()
    generator.load_traits(filepath=FILE_PATH)

    generator.generate(count=TOKEN_COUNT)
    generator.save_to_file()
    print("")

    print(generator.top_rarity(count=10))
    print(generator.bottom_rarity(count=10))