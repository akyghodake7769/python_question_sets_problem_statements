
// REFRESHED: Standardized Harness for J03
import java.util.*;

/* 
 * ==========================================================
 * LOCKED CODE - DO NOT MODIFY
 * ==========================================================
 */
interface AccountOperations {
    void deposit(double amount);

    boolean withdraw(double amount);
}

abstract class BankAccount implements AccountOperations {
    protected String accountNumber;
    protected double balance;

    public BankAccount(String accountNumber, double balance) {
        this.accountNumber = accountNumber;
        this.balance = balance;
    }

    public double getBalance() {
        return balance;
    }
}

class HarnessJ03 {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            if (!sc.hasNextInt())
                return;
            int n = Integer.parseInt(sc.nextLine());

            while (n-- > 0) {
                if (!sc.hasNextLine())
                    break;
                String line = sc.nextLine();
                String[] parts = line.split(" ");
                if (parts.length < 5)
                    continue;

                String type = parts[0];
                String accNo = parts[1];
                double initialBal = Double.parseDouble(parts[2]);
                String action = parts[3];
                double amount = Double.parseDouble(parts[4]);

                BankAccount account = null;
                if (type.equalsIgnoreCase("Savings")) {
                    account = new SavingsAccount(accNo, initialBal);
                } else if (type.equalsIgnoreCase("Current")) {
                    account = new CurrentAccount(accNo, initialBal);
                }

                if (account != null) {
                    if (action.equalsIgnoreCase("Deposit")) {
                        account.deposit(amount);
                        System.out.println("Deposit Successful: New Balance: " + account.getBalance());
                    } else if (action.equalsIgnoreCase("Withdraw")) {
                        if (account.withdraw(amount)) {
                            System.out.println("Withdrawal Successful: New Balance: " + account.getBalance());
                        } else {
                            System.out.println("Withdrawal Failed: Minimum balance requirement not met.");
                        }
                    }
                }
            }
        } catch (Exception e) {
            // Silently handle parsing errors
        }
    }
}
