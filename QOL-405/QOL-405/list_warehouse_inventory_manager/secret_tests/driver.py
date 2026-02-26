"""
QL-603: List Warehouse Inventory Manager
Test driver for evaluating student solution
"""

import os
import sys
import importlib.util


def validate_method_exists(obj, method_name):
    """Check if method exists and is callable."""
    if not hasattr(obj, method_name):
        return False, f"Method '{method_name}' not found in class. Please implement this method."
    if not callable(getattr(obj, method_name)):
        return False, f"'{method_name}' exists but is not callable. Make sure it's defined as a method."
    return True, None


def test_student_code(solution_path):
    """Test the student's InventoryManager solution."""
    
    # Load the student's solution
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(solution)
    except SyntaxError as e:
        print(f"SYNTAX ERROR: {str(e)}\nFix the syntax error in solution.py before running tests.")
        return
    except ImportError as e:
        print(f"IMPORT ERROR: {str(e)}\nMake sure all required modules are imported in solution.py")
        return
    
    print("Running Tests for: List Warehouse Inventory Manager\n")
    
    # Verify class exists
    if not hasattr(solution, "InventoryManager"):
        print("ERROR: InventoryManager class not found in solution.py")
        return
    
    InventoryManager = solution.InventoryManager
    
    # Test cases - Each test case is independent with its own fresh instance
    test_cases = [
        {
            "desc": "Check items in blank inventory (Initial State)",
            "method": "list_items",
            "setup": lambda: _setup_tc1(InventoryManager),
            "call": lambda obj: obj.list_items(),
            "check": lambda result: result == [],
            "expected_output": "Empty list []",
            "marks": 2,
            "is_hidden": False
        },
        {
            "desc": "Add multiple items and verify list",
            "method": "add_item",
            "setup": lambda: _setup_tc2(InventoryManager),
            "call": lambda obj: obj.list_items(),
            "check": lambda result: result == ['Laptop', 'Mouse'],
            "expected_output": "List ['Laptop', 'Mouse']",
            "marks": 2,
            "is_hidden": False
        },
        {
            "desc": "Verify the total count of items",
            "method": "count_items",
            "setup": lambda: _setup_tc3(InventoryManager),
            "call": lambda obj: obj.count_items(),
            "check": lambda result: result == 2,
            "expected_output": "Count of 2",
            "marks": 2,
            "is_hidden": False
        },
        {
            "desc": "Successfully remove an existing item",
            "method": "remove_item",
            "setup": lambda: _setup_tc4(InventoryManager),
            "call": lambda obj: obj.list_items(),
            "check": lambda result: result == ['Laptop'],
            "expected_output": "List ['Laptop'] after removing Mouse",
            "marks": 2,
            "is_hidden": False
        },
        {
            "desc": "Remove a non-existent item",
            "method": "remove_item",
            "setup": lambda: _setup_tc5(InventoryManager),
            "call": lambda obj: obj.list_items(),
            "check": lambda result: result == ['Laptop'],
            "expected_output": "List ['Laptop'] (no change when removing non-existent item)",
            "marks": 2,
            "is_hidden": False
        }
    ]

    total_score = 0
    max_score = 0
    
    for idx, case in enumerate(test_cases, 1):
        marks = case.get("marks", 2)
        max_score += marks
        
        try:
            # Verify method exists
            method_exists, error_msg = validate_method_exists(InventoryManager(), case["method"])
            if not method_exists:
                print(f"FAIL TC{idx} [{case['desc']}]: {error_msg} (0/{marks})")
                continue
            
            # Setup and execute test
            obj = case["setup"]()
            result = case["call"](obj)
            passed = case["check"](result)
            
            if passed:
                print(f"PASS TC{idx} [{case['desc']}] ({marks}/{marks})")
                total_score += marks
            else:
                print(f"FAIL TC{idx} [{case['desc']}]")
                print(f"  Expected: {case['expected_output']}")
                print(f"  Got: {repr(result)}")
        
        except AttributeError as e:
            print(f"FAIL TC{idx} [{case['desc']}]")
            print(f"  Error Type: Attribute Error")
            print(f"  Details: {str(e)}")
            print(f"  Hint: Check method implementation - ensure attribute is correctly initialized")
        
        except TypeError as e:
            print(f"FAIL TC{idx} [{case['desc']}]")
            print(f"  Error Type: Type Error")
            print(f"  Details: {str(e)}")
            print(f"  Hint: Check method return types - list_items() should return list, count_items() should return int")
        
        except Exception as e:
            print(f"FAIL TC{idx} [{case['desc']}]")
            print(f"  Error Type: {type(e).__name__}")
            print(f"  Details: {str(e)}")
    
    # Final score
    print(f"\nSCORE: {total_score}/{max_score} marks")
    if total_score < max_score:
        print("⚠️ Some tests failed. Review the implementation and ensure all methods work correctly.")


def _setup_tc1(InventoryManager):
    """TC1 Setup: Empty inventory (Initial State) - Independent fresh instance."""
    return InventoryManager()


def _setup_tc2(InventoryManager):
    """TC2 Setup: Add multiple items and verify list - Independent fresh instance."""
    manager = InventoryManager()
    manager.add_item("Laptop")
    manager.add_item("Mouse")
    return manager


def _setup_tc3(InventoryManager):
    """TC3 Setup: Verify the total count of items - Independent fresh instance."""
    manager = InventoryManager()
    manager.add_item("Laptop")
    manager.add_item("Mouse")
    return manager


def _setup_tc4(InventoryManager):
    """TC4 Setup: Successfully remove an existing item - Independent fresh instance."""
    manager = InventoryManager()
    manager.add_item("Laptop")
    manager.add_item("Mouse")
    manager.remove_item("Mouse")
    return manager


def _setup_tc5(InventoryManager):
    """TC5 Setup: Remove a non-existent item - Independent fresh instance."""
    manager = InventoryManager()
    manager.add_item("Laptop")
    manager.remove_item("Phone")
    return manager


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solution_path = sys.argv[1]
    else:
        solution_path = os.path.join(os.path.dirname(__file__), '..', 'student_workspace', 'solution.py')
    test_student_code(solution_path)
