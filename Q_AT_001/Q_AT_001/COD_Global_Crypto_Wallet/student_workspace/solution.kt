class Wallet(val walletId: String, val pin: Int, var balance: Double) {
    val transactionLog: MutableList<String> = mutableListOf("Seed Deposit: $$balance")

    // Additional methods if needed
}

class CryptoExchangeSystem {
    private val walletRegistry: MutableMap<String, Wallet> = mutableMapOf()

    /**
     * Create Wallet instance with log.
     * Return "Wallet [walletId] added."
     */
    fun createWallet(walletId: String, pin: Int, initialDeposit: Double): String {
        // TODO: Implement
        return ""
    }

    /**
     * Update balance AND append "Received $[amount]" to wallet.transactionLog.
     * Return "Success. Current Balance: $[new_balance]"
     */
    fun receiveCrypto(walletId: String, amount: Double): String {
        // TODO: Implement
        return ""
    }

    /**
     * Rule: PIN must match AND (balance - amount) >= 0.
     * If valid: Deduct, log "Spent $[amount]", return "Spent $[amount]".
     * If below 0: return "Insufficient funds."
     * Else: return "Security/Access Error."
     */
    fun spendCrypto(walletId: String, pin: Int, amount: Double): String {
        // TODO: Implement
        return ""
    }

    /**
     * Return the full list of strings from wallet.transactionLog.
     * If not found, return ["Wallet not found."].
     */
    fun getTransactionLog(walletId: String): List<String> {
        // TODO: Implement
        return emptyList()
    }

    /**
     * Sum of all balances in the registry.
     * Return Double.
     */
    fun totalNetworkLiquidity(): Double {
        // TODO: Implement
        return 0.0
    }

    /**
     * For EVERY wallet where balance > 1000, add 5% reward and log "Staking Reward".
     * Return the integer count of wallets that received rewards.
     */
    fun applyStakingRewards(): Int {
        // TODO: Implement
        return 0
    }
}
