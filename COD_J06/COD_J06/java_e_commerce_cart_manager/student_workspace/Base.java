import java.util.*;

class Item {
    private String name;
    private double price;
    private int quantity;
    private boolean isTaxable;

    public Item(String name, double price, int quantity, boolean isTaxable) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
        this.isTaxable = isTaxable;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public int getQuantity() {
        return quantity;
    }

    public boolean isTaxable() {
        return isTaxable;
    }
}

abstract class DiscountCoupon {
    protected String code;

    public DiscountCoupon(String code) {
        this.code = code;
    }

    public String getCode() {
        return code;
    }

    public abstract double getDiscount(double subtotal);
}

class InvalidCouponException extends Exception {
    public InvalidCouponException(String message) {
        super(message);
    }
}
