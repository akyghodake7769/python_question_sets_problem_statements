
// /* 
//  * Implement the 'FoodFactory' class and the specific cuisine classes here.
//  * The 'Cuisine' base class and 'UnservableCuisineRequestException' are defined in the Harness.
//  * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
//  */

// class FoodFactory {
//     // Write your code here
// }

// class Chinese extends Cuisine {
//     // Write your code here
//     @Override
//     public Cuisine serveFood(String dish) {
//         return null;
//     }
// }

// class Mexican extends Cuisine {
//     // Write your code here
//     @Override
//     public Cuisine serveFood(String dish) {
//         return null;
//     }
// }

// class Italian extends Cuisine {
//     // Write your code here
//     @Override
//     public Cuisine serveFood(String dish) {
//         return null;
//     }
// }

// class Japanese extends Cuisine {
//     // Write your code here
//     @Override
//     public Cuisine serveFood(String dish) {
//         return null;
//     }
// }

import java.util.*;

class FoodFactory {
    private static FoodFactory instance = null;
    private Map<String, Cuisine> cuisines = new HashMap<>();

    private FoodFactory() {
    }

    public static FoodFactory getFactory() {
        if (instance == null)
            instance = new FoodFactory();
        return instance;
    }

    public void registerCuisine(String key, Cuisine cuisine) {
        cuisines.put(key, cuisine);
    }

    public Cuisine serveCuisine(String key, String dish) throws UnservableCuisineRequestException {
        if (!cuisines.containsKey(key)) {
            throw new UnservableCuisineRequestException("Unservable cuisine " + key + " for dish " + dish);
        }
        return cuisines.get(key).serveFood(dish);
    }
}

class Chinese extends Cuisine {
    private String dish;

    public String getDish() {
        return dish;
    }

    @Override
    public Cuisine serveFood(String dish) {
        this.dish = dish;
        return this;
    }
}

class Mexican extends Cuisine {
    private String dish;

    public String getDish() {
        return dish;
    }

    @Override
    public Cuisine serveFood(String dish) {
        this.dish = dish;
        return this;
    }
}

class Italian extends Cuisine {
    private String dish;

    public String getDish() {
        return dish;
    }

    @Override
    public Cuisine serveFood(String dish) {
        this.dish = dish;
        return this;
    }
}

class Japanese extends Cuisine {
    private String dish;

    public String getDish() {
        return dish;
    }

    @Override
    public Cuisine serveFood(String dish) {
        this.dish = dish;
        return this;
    }
}
