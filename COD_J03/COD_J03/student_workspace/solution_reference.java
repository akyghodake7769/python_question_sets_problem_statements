
class SavingsAccount extends BankAccount {
    public SavingsAccount(String accNo, double bal) { super(accNo, bal); }

    @Override
    public void deposit(double amount) {
        this.balance += amount;
    }

    @Override
    public boolean withdraw(double amount) {
        if (this.balance - amount >= 500) {
            this.balance -= amount;
            return true;
        }
        return false;
    }
}

class CurrentAccount extends BankAccount {
    public CurrentAccount(String accNo, double bal) { super(accNo, bal); }

    @Override
    public void deposit(double amount) {
        this.balance += amount;
    }

    @Override
    public boolean withdraw(double amount) {
        if (this.balance - amount >= -2000) {
            this.balance -= amount;
            return true;
        }
        return false;
    }
}
