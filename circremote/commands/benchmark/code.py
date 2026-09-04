# SPDX-FileCopyrightText: 2025 John Romkey
#
# SPDX-License-Identifier: CC0-1.0

import time
import gc
import json
import sys

# Benchmark configuration
iterations = {{ iterations }}
warmup_runs = {{ warmup_runs }}
output_json = "{{ output_json }}".lower() in ("true", "1", "yes", "on")

def get_system_info():
    """Get system information for JSON output."""
    try:
        import microcontroller
        import sys
        import board
        
        # Get CPU information
        cpu_name = getattr(microcontroller.cpu, 'part_number', None)
        if not cpu_name:
            cpu_name = getattr(microcontroller.cpu, 'name', None)
        if not cpu_name:
            cpu_name = str(microcontroller.cpu).replace('<', '').replace('>', '')
        
        cpu_info = {
            'cpu': cpu_name,
            'frequency': getattr(microcontroller.cpu, 'frequency', None),
            'temperature': getattr(microcontroller.cpu, 'temperature', None)
        }
    except Exception:
        cpu_info = {
            'cpu': 'Unknown',
            'frequency': None,
            'temperature': None
        }
    
    try:
        circuitpython_version = sys.version
    except Exception:
        circuitpython_version = 'Unknown'
    
    try:
        import board
        board_id = getattr(board, 'board_id', None)
        if not board_id:
            board_id = getattr(board, 'board', None)
        if not board_id:
            board_id = 'Unknown'
    except Exception:
        board_id = 'Unknown'
    
    return {
        'cpu_info': cpu_info,
        'board_id': board_id,
        'circuitpython_version': circuitpython_version,
        'platform': sys.platform if hasattr(sys, 'platform') else 'circuitpython'
    }

def run_benchmark(name, func, test_id, *args):
    """Run a benchmark function multiple times and return timing results."""
    # Warmup runs
    for _ in range(warmup_runs):
        func(*args)
    
    # Force garbage collection before timing
    gc.collect()
    
    # Actual benchmark (monotonic_ns avoids the float precision loss of
    # time.monotonic() as device uptime grows)
    start_time = time.monotonic_ns()
    for _ in range(iterations):
        func(*args)
    end_time = time.monotonic_ns()
    
    total_time = (end_time - start_time) / 1_000_000_000
    avg_time = total_time / iterations
    ops_per_second = iterations / total_time if total_time > 0 else 0
    
    return {
        'test_id': test_id,
        'name': name,
        'iterations': iterations,
        'total_time': total_time,
        'avg_time': avg_time,
        'ops_per_second': ops_per_second
    }

def benchmark_integer_addition():
    """Benchmark integer addition."""
    a, b = 12345, 67890
    result = a + b
    return result

def benchmark_integer_multiplication():
    """Benchmark integer multiplication."""
    a, b = 12345, 67890
    result = a * b
    return result

def benchmark_integer_division():
    """Benchmark integer division."""
    a, b = 12345, 67890
    result = a // b  # Floor division for integers
    return result

def benchmark_float_addition():
    """Benchmark float addition."""
    a, b = 123.45, 678.90
    result = a + b
    return result

def benchmark_float_multiplication():
    """Benchmark float multiplication."""
    a, b = 123.45, 678.90
    result = a * b
    return result

def benchmark_float_division():
    """Benchmark float division."""
    a, b = 123.45, 678.90
    result = a / b
    return result

def benchmark_list_append():
    """Benchmark list append operation."""
    lst = []
    for i in range(100):
        lst.append(i)
    return len(lst)

def benchmark_list_access():
    """Benchmark list element access."""
    lst = list(range(100))
    result = 0
    for i in range(100):
        result += lst[i]
    return result

def benchmark_dict_set():
    """Benchmark dictionary key-value setting."""
    d = {}
    for i in range(100):
        d[i] = i * 2
    return len(d)

def benchmark_dict_get():
    """Benchmark dictionary key-value getting."""
    d = {i: i * 2 for i in range(100)}
    result = 0
    for i in range(100):
        result += d[i]
    return result

def benchmark_string_concat():
    """Benchmark string concatenation."""
    result = ""
    for i in range(50):
        result += str(i)
    return len(result)

def benchmark_function_call():
    """Benchmark simple function calls."""
    def simple_func(x):
        return x + 1
    
    result = 0
    for i in range(100):
        result += simple_func(i)
    return result

def benchmark_memory_allocation():
    """Benchmark memory allocation patterns."""
    # Create and destroy many small objects
    for _ in range(50):
        lst = [i for i in range(20)]
        del lst
    return 50

def benchmark_string_formatting():
    """Benchmark string formatting operations."""
    result = ""
    for i in range(50):
        result += f"Item {i}: {i * 2}"
    return len(result)

def benchmark_array_slicing():
    """Benchmark array slicing operations."""
    arr = list(range(100))
    result = 0
    for i in range(50):
        slice_data = arr[i:i+10]
        result += len(slice_data)
    return result

def benchmark_set_operations():
    """Benchmark set operations."""
    set1 = set(range(50))
    set2 = set(range(25, 75))
    
    # Union operation
    union_result = set1 | set2
    
    # Intersection operation
    intersection_result = set1 & set2
    
    # Difference operation
    difference_result = set1 - set2
    
    return len(union_result) + len(intersection_result) + len(difference_result)

def benchmark_tuple_vs_list():
    """Benchmark tuple vs list performance."""
    # List operations
    lst = []
    for i in range(50):
        lst.append(i)
    
    # Tuple operations
    tup = tuple(range(50))
    
    # Access operations
    list_sum = sum(lst)
    tuple_sum = sum(tup)
    
    return list_sum + tuple_sum

def benchmark_nested_structures():
    """Benchmark nested data structure access."""
    # Create nested structure
    nested = {
        'level1': {
            'level2': {
                'level3': [i for i in range(10)]
            }
        }
    }
    
    # Access nested data
    result = 0
    for i in range(50):
        result += len(nested['level1']['level2']['level3'])
    
    return result

def main():
    print("CircuitPython Performance Benchmark")
    print("=" * 40)
    print(f"Iterations per test: {iterations}")
    print(f"Warmup runs: {warmup_runs}")
    print()
    
    benchmarks = [
        # Basic Arithmetic
        ("int_add", "Integer Addition", benchmark_integer_addition),
        ("int_mul", "Integer Multiplication", benchmark_integer_multiplication),
        ("int_div", "Integer Division", benchmark_integer_division),
        ("float_add", "Float Addition", benchmark_float_addition),
        ("float_mul", "Float Multiplication", benchmark_float_multiplication),
        ("float_div", "Float Division", benchmark_float_division),
        
        # Data Structures
        ("list_append", "List Append", benchmark_list_append),
        ("list_access", "List Access", benchmark_list_access),
        ("dict_set", "Dict Set", benchmark_dict_set),
        ("dict_get", "Dict Get", benchmark_dict_get),
        
        # Memory Operations
        ("mem_alloc", "Memory Allocation", benchmark_memory_allocation),
        ("str_fmt", "String Formatting", benchmark_string_formatting),
        ("arr_slice", "Array Slicing", benchmark_array_slicing),
        
        # Advanced Data Structures
        ("set_ops", "Set Operations", benchmark_set_operations),
        ("tuple_list", "Tuple vs List", benchmark_tuple_vs_list),
        ("nested", "Nested Structures", benchmark_nested_structures),
        
        # Other Operations
        ("str_concat", "String Concatenation", benchmark_string_concat),
        ("func_call", "Function Call", benchmark_function_call),
    ]
    
    results = []
    
    for test_id, name, func in benchmarks:
        print(f"Running {name}...", end=" ")
        try:
            result = run_benchmark(name, func, test_id)
            results.append(result)
            print(f"✓ ({result['ops_per_second']:.0f} ops/sec)")
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append({
                'test_id': test_id,
                'name': name,
                'iterations': iterations,
                'total_time': 0,
                'avg_time': 0,
                'ops_per_second': 0,
                'error': str(e)
            })
    
    print()
    print("BENCHMARK RESULTS")
    print("=" * 40)
    print(f"{'Operation':<20} {'Ops/sec':<12} {'Avg (μs)':<12} {'Total (ms)':<12}")
    print("-" * 56)
    
    for result in results:
        if 'error' in result:
            print(f"{result['name']:<20} {'ERROR':<12} {'N/A':<12} {'N/A':<12}")
        else:
            avg_us = result['avg_time'] * 1_000_000
            total_ms = result['total_time'] * 1000
            print(f"{result['name']:<20} {result['ops_per_second']:>8.0f} {avg_us:>8.1f}μs {total_ms:>8.1f}ms")
    
    print()
    print("SUMMARY")
    print("=" * 40)
    
    # Find fastest and slowest operations
    valid_results = [r for r in results if 'error' not in r and r['ops_per_second'] > 0]
    
    if valid_results:
        fastest = max(valid_results, key=lambda x: x['ops_per_second'])
        slowest = min(valid_results, key=lambda x: x['ops_per_second'])
        
        print(f"Fastest: {fastest['name']} ({fastest['ops_per_second']:.0f} ops/sec)")
        print(f"Slowest: {slowest['name']} ({slowest['ops_per_second']:.0f} ops/sec)")
        
        if fastest['ops_per_second'] > 0:
            ratio = fastest['ops_per_second'] / slowest['ops_per_second']
            print(f"Speed ratio: {ratio:.1f}x faster")
    
    print()
    print("Benchmark completed!")
    
    # Output JSON if requested
    if output_json:
        print()
        print("JSON OUTPUT")
        print("=" * 40)
        
        system_info = get_system_info()
        json_output = {
            'system': system_info,
            'benchmark_config': {
                'iterations': iterations,
                'warmup_runs': warmup_runs
            },
            'results': results
        }
        
        try:
            json_str = json.dumps(json_output)
            print(json_str)
        except Exception as e:
            print(f"Error generating JSON: {e}")
            # Fallback: print results in a simpler format
            simple_results = []
            for result in results:
                simple_results.append({
                    'test_id': result.get('test_id', 'unknown'),
                    'name': result.get('name', 'unknown'),
                    'iterations': result.get('iterations', 0),
                    'ops_per_second': result.get('ops_per_second', 0),
                    'total_time': result.get('total_time', 0)
                })
            print(json.dumps(simple_results))

if __name__ == "__main__":
    main()
