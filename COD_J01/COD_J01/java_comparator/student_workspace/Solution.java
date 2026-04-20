// // import java.util.Arrays;

// /* 
//  * Implement the 'Comparator' class here.
//  * It should have three overloaded 'compare' methods.
//  * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
//  */

// class Comparator {
//     boolean compare(int a, int b) {
//         // Write your code here
//         return false;
//     }

//     boolean compare(String a, String b) {
//         // Write your code here
//         return false;
//     }

//     boolean compare(int[] a, int[] b) {
//         // Write your code here
//         return false;
//     }
// }

// import java.util.Arrays;

class Comparator {
    boolean compare(int a, int b) {
        return a == b;
    }

    boolean compare(String a, String b) {
        return a.equals(b);
    }

    boolean compare(int[] a, int[] b) {
        if (a.length != b.length)
            return false;
        for (int i = 0; i < a.length; i++) {
            if (a[i] != b[i])
                return false;
        }
        return true;
    }
}
