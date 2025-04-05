from CustomerFactory import CustomerFactory
import csv

def main():
    # Generate customers (e.g., 10 customers)
    customers = CustomerFactory.generate_customers(30000)

    # Define the file path
    file_path = r'C:\Proiecte\Proiecte_de_ale_mele\Python\sf_prediction_backend\customers.csv'

    # Write customers to a CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Name', 'Account Name', 'Account Industry', 'Net Revenue Per Quarter', 'Days Since Last Deal',
                         'New Customer', 'Successful Deals Closed', 'Will this customer continue to do business with us?'])
        # Write customer data
        for customer in customers:
            writer.writerow([
                customer.name,
                customer.account.name,
                customer.account.industry,
                customer.net_revenue_per_quarter,
                customer.days_since_last_deal,
                customer.new_customer,
                customer.successful_deals_closed,
                customer.future_customer
            ])

    print(f"Customers exported to '{file_path}'")

# Run the main function
if __name__ == "__main__":
    main()