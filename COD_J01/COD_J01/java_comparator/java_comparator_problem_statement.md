# Java: How Will You Compare?

Create a `Comparator` class that includes three overloaded `compare` methods to evaluate strings, integers, and integer arrays. The program should:

* `boolean compare(String a, String b)`: Return `true` if $a = b$, otherwise return `false`.
* `boolean compare(int a, int b)`: Return `true` if $a = b$, otherwise return `false`.
* `boolean compare(int[] a, int[] b)`: Return `true` if both of the following conditions hold true. Otherwise, return `false`:
  1. The length of $a =$ the length of $b$.
  2. Elements $a[i] = b[i]$ for all indices.

**Class Description**
Complete the class `Comparator` in the editor with the following overloaded methods:

* `boolean compare(int a, int b)`
* `boolean compare(String a, String b)`
* `boolean compare(int[] a, int[] b)`

**Returns**

* `boolean`: Returns `true` if the conditions are met, `false` otherwise.
* The locked stub code prints "Same" for `true` and "Different" for `false`.

**Constraints**

* For strings, $1 \le length \text{ of } s, length \text{ of } b \le 2000$.
* For integers, $0 \le a, b \le 10,000,000$.
* For integer arrays, $1 \le length \text{ of } a, length \text{ of } b \le 10$.

**Input Format For Custom Testing**
The first line contains an integer $T$, the number of test cases.
Each of the next $T$ sets of lines is in one of the following formats:

* `type 1`: Next two lines contain strings $a$ and $b$.
* `type 2`: Next two lines contain integers $a$ and $b$.
* `type 3`: Next line contains lengths $n$ and $m$, followed by elements of arrays $a$ and $b$.

**Sample Case 0**
**Sample Input For Custom Testing**

```text
3
1
hello world
hello world
2
3
4
3
3 3
1 2 3
1 2 3
```

**Sample Output**

```text
Same
Different
Same
```

**Explanation**
Test Case 1: The strings are identical.
Test Case 2: The integers 3 and 4 are different ($3 \ne 4$).
Test Case 3: Both arrays have the same length and identical elements.


**Boilerplate :**

```
// student_workspace/solution.java

/* 
 * Implement the 'Comparator' class here.
 * It should have three overloaded 'compare' methods.
 * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
 */

class Comparator {
    boolean compare(int a, int b) {
        // Write your code here
        return false;
    }

    boolean compare(String a, String b) {
        // Write your code here
        return false;
    }

    boolean compare(int[] a, int[] b) {
        // Write your code here
        return false;
    }
}
```


**Solution.java :**

```
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
```
