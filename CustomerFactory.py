import random
import string
from Customer import Customer
from Account import Account

class CustomerFactory:
    """Generates random Customer objects."""

    @staticmethod
    def random_string(length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def create_random_account():
        industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Education', 'Banking', 'Apparel', 'Chemicals',
                      'Consulting', 'Electronics', 'Engineering', 'Government', 'Media']

        names = ['Edge Communications', 'Burlington Textiles Corp of America',
                 'Pyramid Construction Inc.', 'Dickenson plc',
                 'Grand Hotels & Resorts Ltd', 'United Oil & Gas Corp.',
                 'Express Logistics and Transport', 'University of Arizona',
                 'United Oil & Gas, UK', 'United Oil & Gas, Singapore',
                 'GenePoint', 'sForce']
        return Account(
            name=random.choice(names),
            industry=random.choice(industries)
        )

    @staticmethod
    def create_random_customer():
        new_customer = random.choices([True, False], weights=[0.1, 0.9])[0]
        future_customer = random.choices([1,0], weights=[0.82, 0.18])[0]
        return Customer(
            name=CustomerFactory.random_string(),
            account=CustomerFactory.create_random_account(),
            net_revenue_per_quarter=random.randint(1000, 100000),
            days_since_last_deal=random.randint(0, 800) if not new_customer else -1,
            new_customer=new_customer,
            successful_deals_closed=random.randint(1, 100),
            future_customer=future_customer
        )

    @staticmethod
    def generate_customers(count):
        return [CustomerFactory.create_random_customer() for _ in range(count)]