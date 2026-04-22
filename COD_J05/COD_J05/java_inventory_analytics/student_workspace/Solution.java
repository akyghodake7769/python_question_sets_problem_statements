// import java.util.*;

// /* 
//  * Implement the 'InventoryService' class here using Java Streams.
//  * The 'Product' class is already defined in the Harness.
//  * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
//  */

// class InventoryService {
//     public double calculateTotalValue(List<Product> products) {
//         // Write your code here
//         return 0;
//     }

//     public Map<String, Product> getMostExpensiveByCategory(List<Product> products) {
//         // Write your code here
//         return null;
//     }
// }

import java.util.*;
import java.util.stream.*;

class InventoryService {
    public double calculateTotalValue(List<Product> products) {
        return products.stream()
                .filter(p -> p.getQuantity() > 0)
                .mapToDouble(p -> p.getPrice() * p.getQuantity())
                .sum();
    }

    public Map<String, Product> getMostExpensiveByCategory(List<Product> products) {
        return products.stream()
                .filter(p -> p.getQuantity() > 0)
                .collect(Collectors.toMap(
                        Product::getCategory,
                        p -> p,
                        (p1, p2) -> p1.getPrice() >= p2.getPrice() ? p1 : p2));
    }
}
