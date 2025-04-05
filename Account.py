class Account:
    """Represents an Account object."""
    def __init__(self, name, industry):
        self.name = name
        self.industry = industry

    def __repr__(self):
        return f"Account(name='{self.name}', industry='{self.industry}')"
