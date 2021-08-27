from faker import Faker
import pandas as pd

fake = Faker()
Faker.seed(0)

N_EXAMPLES = 1000

texts = fake.sentences(N_EXAMPLES)
clusters = [fake.random_int(0, 20) for _ in range(N_EXAMPLES)]

demo_df = pd.DataFrame(dict(texts=texts, clusters=clusters))
