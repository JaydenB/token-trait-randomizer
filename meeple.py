import random
import time

TOKEN_COUNT = 1111


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

    for i in range(TOKEN_COUNT):
        new_token = generate_token()
        while new_token in generated_tokens:
            new_token = generate_token()

        # calculate real rarities from the generation
        background_real_weights[background.index(new_token['background'])] += 1
        color_real_weights[color.index(new_token['color'])] += 1
        material_real_weights[material.index(new_token['material'])] += 1
        pattern_real_weights[pattern.index(new_token['pattern'])] += 1
        case_real_weights[case.index(new_token['case'])] += 1

        generated_tokens.append(new_token)
        print(f"\tGenerated {i}:\t{new_token}")

    print(f"{len(generated_tokens)} of {TOKEN_COUNT} tokens generated.")
    print(f"Completed in {round(time.time() - start_time, 2)} seconds.")

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
    print(f"\nBackground Rarity: {str(b_rarity)}")
    print(f"Color Rarity: {str(co_rarity)}")
    print(f"Material Rarity: {str(m_rarity)}")
    print(f"Pattern Rarity: {str(p_rarity)}")
    print(f"Case Rarity: {str(ca_rarity)}")
