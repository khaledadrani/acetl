from faker import Faker
import csv

# Create a Faker instance
fake = Faker()

# Generate dummy data for healthcare
def generate_healthcare_data(num_records):
    healthcare_data = []
    for _ in range(num_records):
        record = {
            'Patient Name': fake.name(),
            'Patient ID': fake.uuid4(),
            'Doctor': fake.name(),
            'Diagnosis': fake.word(),
            'Treatment': fake.sentence()
        }
        healthcare_data.append(record)
    return healthcare_data

# Generate dummy data for retail
def generate_retail_data(num_records):
    retail_data = []
    for _ in range(num_records):
        record = {
            'Product Name': fake.word(),
            'Product ID': fake.uuid4(),
            'Price': fake.random_number(digits=2),
            'Quantity': fake.random_number(digits=1),
            'Category': fake.word()
        }
        retail_data.append(record)
    return retail_data

# Save data to CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data:
            writer.writerow(record)

# Generate and save healthcare data
num_healthcare_records = 100
healthcare_data = generate_healthcare_data(num_healthcare_records)
save_to_csv(healthcare_data, 'healthcare/healthcare_data_3.csv')

# Generate and save retail data
num_retail_records = 100
retail_data = generate_retail_data(num_retail_records)
save_to_csv(retail_data, 'retail/retail_data_3.csv')

print("CSV files generated successfully.")
