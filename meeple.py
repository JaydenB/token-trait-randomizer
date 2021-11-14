import random
import time

# Current max ~8000 (gets really slow around 7500)
TOKEN_COUNT = 1111
PRINT_COUNT = 25


size_weights = [70, 20, 10]
size = ["Normal", "Jumbo", "Tiny"]
size_real_weights = [0, 0, 0]


background_weights = [80, 20]
background = ["White", "Black"]
background_real_weights = [0, 0]

color_weights = [20, 20, 10, 10, 10, 5, 5, 5, 5, 5, 5]
color = ["White", "Black", "Red", "Green", "Blue", "Purple", "Pink", "Cyan", "Orange", "Yellow",
         "Teal"]
color_real_weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

material_weights = [60, 35, 5]
material = ["Wood", "Metal", "Resin"]
material_real_weights = [0, 0, 0]

pattern_weights = [40, 20, 20, 5, 5, 4, 5, 1]
pattern = ["None", "Diagonal Lines", "Straight Lines", "Skulls", "Hearts", "Flowers",
           "Checkered", "Ocean Wave"]
pattern_real_weights = [0, 0, 0, 0, 0, 0, 0, 0]

case_weights = [45, 25, 15, 10, 5]
case = ["None", "Bronze", "Silver", "Gold", "Dark Metal"]
case_real_weights = [0, 0, 0, 0, 0]


def generate_token():
    token = dict()
    token['size'] = random.choices(size, weights=size_weights, k=1)[0]
    token['background'] = random.choices(background, weights=background_weights, k=1)[0]
    token['color'] = random.choices(color, weights=color_weights, k=1)[0]
    token['material'] = random.choices(material, weights=material_weights, k=1)[0]
    token['pattern'] = random.choices(pattern, weights=pattern_weights, k=1)[0]
    token['case'] = random.choices(case, weights=case_weights, k=1)[0]
    return token


if __name__ == '__main__':
    print("Starting Rarity Generation Tool...")

    start_time = time.time()
    generated_tokens = []
    rarity_tokens = []

    # Generate all the tokens
    for i in range(TOKEN_COUNT):
        new_token = generate_token()
        while new_token in generated_tokens:
            new_token = generate_token()

        # calculate real rarities from the generation
        size_real_weights[size.index(new_token['size'])] += 1
        background_real_weights[background.index(new_token['background'])] += 1
        color_real_weights[color.index(new_token['color'])] += 1
        material_real_weights[material.index(new_token['material'])] += 1
        pattern_real_weights[pattern.index(new_token['pattern'])] += 1
        case_real_weights[case.index(new_token['case'])] += 1

        r = size_weights[size.index(new_token['size'])] + \
            background_weights[background.index(new_token['background'])] + \
            color_weights[color.index(new_token['color'])] + \
            material_weights[material.index(new_token['material'])] + \
            pattern_weights[pattern.index(new_token['pattern'])] + \
            case_weights[case.index(new_token['case'])]

        new_rarity = [i, r]

        generated_tokens.append(new_token)
        rarity_tokens.append(new_rarity)
        print(f"\tGenerated {i}:\t{new_token}")

    print(f"{len(generated_tokens)} of {TOKEN_COUNT} tokens generated.")
    print(f"Completed in {round(time.time() - start_time, 2)} seconds.")

    # Calculating True Rarity values after random spawn
    s_rarity = ' '.join([f"{round(i * 100.0, 1)}%" for i in
                         [x / sum(size_real_weights) for x in size_real_weights]])
    b_rarity = ' '.join([f"{round(i*100.0, 1)}%" for i in
                         [x/sum(background_real_weights) for x in background_real_weights]])
    co_rarity = ' '.join([f"{round(i*100.0, 1)}%" for i in
                         [x/sum(color_real_weights) for x in color_real_weights]])
    m_rarity = ' '.join([f"{round(i*100.0, 1)}%" for i in
                         [x/sum(material_real_weights) for x in material_real_weights]])
    p_rarity = ' '.join([f"{round(i*100.0, 1)}%" for i in
                         [x/sum(pattern_real_weights) for x in pattern_real_weights]])
    ca_rarity = ' '.join([f"{round(i*100.0, 1)}%" for i in
                         [x/sum(case_real_weights) for x in case_real_weights]])
    print(f"\nSize Rarity: {str(s_rarity)}")
    print(f"Background Rarity: {str(b_rarity)}")
    print(f"Color Rarity: {str(co_rarity)}")
    print(f"Material Rarity: {str(m_rarity)}")
    print(f"Pattern Rarity: {str(p_rarity)}")
    print(f"Case Rarity: {str(ca_rarity)}")

    # RARITY SORTING based off Metadata
    sorted_rarities = sorted(rarity_tokens, key=lambda x: x[1], reverse=False)
    print(f"\n\nTop {PRINT_COUNT} Rarity items:")
    for i in range(PRINT_COUNT):
        print(f"\t#{i+1}: {sorted_rarities[i][1]}%"
              f" {str(generated_tokens[sorted_rarities[i][0]])}")

    sorted_rarities = sorted(rarity_tokens, key=lambda x: x[1], reverse=True)
    print(f"\n\nLowest {PRINT_COUNT} Rarity items:")
    for i in range(PRINT_COUNT):
        print(
            f"\t#{len(sorted_rarities)-i}: {sorted_rarities[i][1]}%"
            f" {str(generated_tokens[sorted_rarities[i][0]])}")

