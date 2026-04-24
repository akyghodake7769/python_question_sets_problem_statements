# Java: The Cuisines

Alex owns Dine Out, a prominent franchise restaurant that exclusively serves Chinese, Italian, Japanese, and Mexican cuisines. Design the `FoodFactory` and other necessary classes to simulate the serving process. The class should implement the following methods:

1. `FoodFactory getFactory()` to return the instance of the `FoodFactory` class.
2. `void registerCuisine(String cuisineKey, Cuisine cuisine)` to register the cuisine so that the food factory would be able to serve it. Here `Cuisine` is the abstract class provided in the locked stub code.
3. `Cuisine serveCuisine(String cuisineKey, String dish)` to serve a dish for the given cuisine. If the requested cuisine is not registered with the food factory, then the exception `UnservableCuisineRequestException` should be thrown with the message `"Unservable cuisine {cuisineKey} for dish {dish}"`.

The locked stub code in the editor validates the correctness of the `FoodFactory` class implementation by processing some cuisine requests.

**Class Description**
Complete the class `FoodFactory` and concrete `Cuisine` subclasses in the editor.

**Returns**

* `FoodFactory`: The singleton instance.
* `Cuisine`: The served food object.
* `Exception`: `UnservableCuisineRequestException` for invalid keys.

**Constraints**

* $1 \le totalNumberOfOrders \le 100$.

**Input Format For Custom Testing**
The first line contains the value of `totalNumberOfOrders` describing the total number of orders placed.
The next `totalNumberOfOrders` lines contain the cuisine key and dish name separated by space for each order.

**Sample Case 0**
**Sample Input For Custom Testing**

```text
3
Italian Lasagne
Japanese Kamameshi
Polish Marjoram
```

**Sample Output**

```text
Serving Lasagne(Italian)
Serving Kamameshi(Japanese)
Unservable cuisine Polish for dish Marjoram
```

**Explanation**

* **Italian Lasagne**: The dish Lasagne is an Italian dish. Italian cuisine is served by the restaurant, so the locked stub code prints "Serving Lasagne(Italian)".
* **Japanese Kamameshi**: The dish Kamameshi is Japanese cuisine which is served by the restaurant, so the locked stub code prints "Serving Kamameshi(Japanese)".
* **Polish Marjoram**: The dish Marjoram is Polish cuisine which is not served by the restaurant, so the `UnservableCuisineRequestException` exception is thrown.
