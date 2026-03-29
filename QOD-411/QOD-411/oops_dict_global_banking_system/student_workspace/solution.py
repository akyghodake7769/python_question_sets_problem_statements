# class Account:
#     """
#     Data Entity representing a single bank account.
#     """
#     def __init__(self, acc_id: str, pin: int, balance: float):
#         # TODO: Initialize acc_id, pin, balance, and transaction_log
#         # transaction_log should start as: [f"Initial Deposit: ${balance}"]
#         pass

# class GlobalBankingSystem:
#     """
#     Manager class for the banking system.
#     """
#     def __init__(self):
#         # TODO: Initialize empty accounts dictionary
#         pass

#     def create_account(self, acc_id: str, pin: int, deposit: float) -> str:
#         # TODO: Create Account object and store in self.accounts
#         return ""

#     def deposit_funds(self, acc_id: str, amount: float) -> str:
#         # TODO: Update balance and append "Deposited $[amount]" to log
#         return ""

#     def secure_withdraw(self, acc_id: str, pin: int, amount: float) -> str:
#         # TODO: Verify PIN and Overdraft limit (-500)
#         # Log: "Withdrew $[amount]"
#         return ""

#     def get_transaction_history(self, acc_id: str) -> list:
#         # TODO: Return account log or ["Account not found."]
#         return []

#     def total_liquidity(self) -> float:
#         # TODO: Return net sum of all balances
#         return 0.0

#     def apply_annual_interest(self) -> int:
#         # TODO: Application 5% interest to balances > 5000. Log "Interest Credit".
#         # Return count of processed accounts.
#         return 0


class Account:
    """
    Data Entity representing a single bank account.
    """
    def __init__(self, acc_id: str, pin: int, balance: float):
        # self.acc_id = acc_id
        # self.pin = pin
        # self.balance = balance
        # self.transaction_log = [f"Initial Deposit: ${balance}"]
        pass
    
class GlobalBankingSystem:
    """
    Manager class for the banking system.
    """
    def __init__(self):
        # self.accounts = {}
        pass
    def create_account(self, acc_id: str, pin: int, deposit: float) -> str:
        """Adds a new account to the registry."""
        # self.accounts[acc_id] = Account(acc_id, pin, deposit)
        # return f"Account {acc_id} registered."
        pass
    def deposit_funds(self, acc_id: str, amount: float) -> str:
        """Updates balance and logs the deposit."""
        # if acc_id in self.accounts:
        #     acc = self.accounts[acc_id]
        #     acc.balance += amount
        #     acc.transaction_log.append(f"Deposited ${amount}")
        #     return f"Success. Balance: ${acc.balance}"
        # return "Account not found."
        pass

    def secure_withdraw(self, acc_id: str, pin: int, amount: float) -> str:
        """Subtracts funds if PIN is correct and overdraft (-500) limit is not hit."""
        if acc_id in self.accounts:
            acc = self.accounts[acc_id]
            if acc.pin == pin:
                if (acc.balance - amount) >= -500:
                    acc.balance -= amount
                    acc.transaction_log.append(f"Withdrew ${amount}")
                    return f"Withdrew ${amount}"
                else:
                    return "Overdraft limit exceeded."
            else:
                return "Security/Access Error."
        return "Security/Access Error."

    def get_transaction_history(self, acc_id: str) -> list:
        """Returns the audit trail for a specific account."""
        if acc_id in self.accounts:
            return self.accounts[acc_id].transaction_log
        return ["Account not found."]

    def total_liquidity(self) -> float:
        """Sums all account balances."""
        return sum(acc.balance for acc in self.accounts.values())

    def apply_annual_interest(self) -> int:
        """Applies 5% interest to balances > 5000 and returns count of updated accounts."""
        count = 0
        for acc in self.accounts.values():
            if acc.balance > 5000:
                interest = acc.balance * 0.05
                acc.balance += interest
                acc.transaction_log.append("Interest Credit")
                count += 1
        return count
