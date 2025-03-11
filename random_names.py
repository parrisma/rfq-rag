import random

first_names = ["Alex", "Ben", "Charlie", "David", "Eva", "Frank", "Grace", "Henry", "Ivy", "Jack"]
nicknames = ["Al", "Benny", "Chuck", "Dave", "Eve", "Frankie", "Gracie", "Hank", "Ive", "Jackie"]
family_names = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson"]

def generate_random_names_list(num_names):
    """Generates a list of random names (first, family, nickname) as tuples."""

    names_list = []
    for _ in range(num_names):
        index = random.randint(0, len(first_names) - 1)
        first_name = first_names[index]
        family_name = random.choice(family_names)
        nickname = nicknames[index]
        names_list.append((first_name, family_name, nickname))
    return names_list

# Generate a list of 5 random names:
random_names = generate_random_names_list(20)
for name_tuple in random_names:
    print(name_tuple)