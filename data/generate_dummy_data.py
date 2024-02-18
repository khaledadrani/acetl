import random
from typing import List, Dict
import pandas as pd
from faker import Faker
import csv

random.seed(42)
fake = Faker()


def generate_fake_data(num_records: int, unclean_prob: float = 0.2) -> List[Dict]:
    data_list = []
    for _ in range(num_records):

        record = {
            'Product Name': fake.word(),
            'Product Code': fake.uuid4(),
            'Price': fake.random_number(digits=2),
            'Quantity': fake.random_number(digits=1),
            'Category': fake.word()
        }

        current_proba = random.uniform(0, 1)
        is_bad_data = current_proba < unclean_prob

        if is_bad_data:
            # Simulate null values or incorrect data types
            field_to_unclean = random.choice(list(record.keys()))
            record[field_to_unclean] = None if random.choice([True, False]) else fake.word()

        data_list.append(record)

    df = pd.DataFrame(data_list)
    # simply to check if generated data contains missing values
    print("NA columns? ", df.isna().sum())
    return data_list


# Save data to CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data:
            writer.writerow(record)


save_to_csv(generate_fake_data(100), 'retail_data_small.csv')
save_to_csv(generate_fake_data(10000), 'retail_data_medium.csv')
save_to_csv(generate_fake_data(1000000), 'retail_data_large.csv')

print("CSV files generated successfully.")
