class Customer:
    """Represents a Customer object."""
    def __init__(self, name, account, net_revenue_per_quarter, days_since_last_deal, new_customer, successful_deals_closed, future_customer):
        self.name = name
        self.account = account
        self.net_revenue_per_quarter = net_revenue_per_quarter
        self.days_since_last_deal = days_since_last_deal
        self.new_customer = new_customer
        self.successful_deals_closed = successful_deals_closed
        self.future_customer = future_customer

    def __repr__(self):
        return (f"Customer(name='{self.name}', account={self.account}, "
                f"net_revenue_per_quarter={self.net_revenue_per_quarter}, "
                f"days_since_last_deal={self.days_since_last_deal}, "
                f"new_customer={self.new_customer}, "
                f"successful_deals_closed={self.successful_deals_closed}"
                f"future_customer={self.future_customer})")