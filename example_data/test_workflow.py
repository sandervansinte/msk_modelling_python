"""
Simple test script for the workflow module.
This tests basic functionality without requiring OpenSim or other dependencies.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from msk_modelling_python.workflow import Pipeline, WorkflowNode, create_simple_pipeline


def test_basic_pipeline():
    """Test a basic linear pipeline."""
    print("\n" + "="*60)
    print("Test 1: Basic Linear Pipeline")
    print("="*60)
    
    def step1(x):
        return {"y": x + 1}
    
    def step2(y):
        return {"z": y * 2}
    
    def step3(z):
        return {"result": z ** 2}
    
    pipeline = Pipeline("Basic Test", "Simple 3-step pipeline")
    
    pipeline.add_node(WorkflowNode("Step1", step1, {"x": 5}), is_start=True)
    pipeline.add_node(WorkflowNode("Step2", step2))
    pipeline.add_node(WorkflowNode("Step3", step3))
    
    pipeline.connect("Step1", "Step2")
    pipeline.connect("Step2", "Step3")
    
    print(pipeline.visualize())
    
    results = pipeline.execute()
    
    assert results["status"] == "completed", "Pipeline should complete successfully"
    assert results["final_context"]["result"] == 144, "Result should be 144: (5+1)*2^2"
    
    print("✓ Test 1 passed: Basic pipeline works correctly\n")
    return True


def test_branching_pipeline():
    """Test a pipeline with branching."""
    print("\n" + "="*60)
    print("Test 2: Branching Pipeline")
    print("="*60)
    
    def start(value):
        return {"data": value}
    
    def branch_a(data):
        return {"result_a": data + 10}
    
    def branch_b(data):
        return {"result_b": data * 2}
    
    def merge(result_a, result_b):
        return {"final": result_a + result_b}
    
    pipeline = Pipeline("Branching Test", "Pipeline with parallel branches")
    
    pipeline.add_node(WorkflowNode("Start", start, {"value": 5}), is_start=True)
    pipeline.add_node(WorkflowNode("BranchA", branch_a))
    pipeline.add_node(WorkflowNode("BranchB", branch_b))
    pipeline.add_node(WorkflowNode("Merge", merge))
    
    pipeline.connect("Start", "BranchA")
    pipeline.connect("Start", "BranchB")
    pipeline.connect("BranchA", "Merge")
    pipeline.connect("BranchB", "Merge")
    
    print(pipeline.visualize())
    
    results = pipeline.execute()
    
    assert results["status"] == "completed", "Pipeline should complete successfully"
    assert results["final_context"]["final"] == 25, "Result should be 25: (5+10)+(5*2)"
    
    print("✓ Test 2 passed: Branching pipeline works correctly\n")
    return True


def test_simple_pipeline_helper():
    """Test the create_simple_pipeline helper function."""
    print("\n" + "="*60)
    print("Test 3: Simple Pipeline Helper")
    print("="*60)
    
    def load(filepath):
        return {"data": f"loaded_{filepath}"}
    
    def process(data):
        return {"processed": f"processed_{data}"}
    
    def save(processed, output):
        return {"saved": f"saved_{processed}_to_{output}"}
    
    tasks = [
        ("Load", load, {"filepath": "input.txt"}, "Load data"),
        ("Process", process, {}, "Process data"),
        ("Save", save, {"output": "output.txt"}, "Save results")
    ]
    
    pipeline = create_simple_pipeline("Helper Test", tasks, "Test helper function")
    
    print(pipeline.visualize())
    
    results = pipeline.execute()
    
    assert results["status"] == "completed", "Pipeline should complete successfully"
    assert "saved" in results["final_context"], "Should have 'saved' in final context"
    
    print("✓ Test 3 passed: Helper function works correctly\n")
    return True


def test_error_handling():
    """Test error handling in pipeline."""
    print("\n" + "="*60)
    print("Test 4: Error Handling")
    print("="*60)
    
    def step1():
        return {"value": 10}
    
    def step2_fails(value):
        raise ValueError("Intentional error for testing")
    
    def step3(value):
        return {"final": value * 2}
    
    pipeline = Pipeline("Error Test", "Test error handling")
    
    pipeline.add_node(WorkflowNode("Step1", step1), is_start=True)
    pipeline.add_node(WorkflowNode("Step2", step2_fails))
    pipeline.add_node(WorkflowNode("Step3", step3))
    
    pipeline.connect("Step1", "Step2")
    pipeline.connect("Step2", "Step3")
    
    print(pipeline.visualize())
    
    results = pipeline.execute(stop_on_error=True)
    
    assert results["status"] == "failed", "Pipeline should fail"
    assert results["nodes"]["Step1"]["status"] == "completed", "Step1 should complete"
    assert results["nodes"]["Step2"]["status"] == "failed", "Step2 should fail"
    assert results["nodes"]["Step3"]["status"] == "pending", "Step3 should not run"
    
    print("✓ Test 4 passed: Error handling works correctly\n")
    return True


def test_parameter_filtering():
    """Test that only required parameters are passed to functions."""
    print("\n" + "="*60)
    print("Test 5: Parameter Filtering")
    print("="*60)
    
    def step1():
        return {"a": 1, "b": 2, "c": 3, "d": 4}
    
    def step2(a, b):
        # Should only receive a and b, not c and d
        return {"result": a + b}
    
    pipeline = Pipeline("Filter Test", "Test parameter filtering")
    
    pipeline.add_node(WorkflowNode("Step1", step1), is_start=True)
    pipeline.add_node(WorkflowNode("Step2", step2))
    
    pipeline.connect("Step1", "Step2")
    
    results = pipeline.execute()
    
    assert results["status"] == "completed", "Pipeline should complete successfully"
    assert results["final_context"]["result"] == 3, "Result should be 3 (1+2)"
    
    print("✓ Test 5 passed: Parameter filtering works correctly\n")
    return True


def test_execution_timing():
    """Test that execution timing is tracked."""
    print("\n" + "="*60)
    print("Test 6: Execution Timing")
    print("="*60)
    
    import time
    
    def slow_step():
        time.sleep(0.1)
        return {"done": True}
    
    pipeline = Pipeline("Timing Test", "Test execution timing")
    pipeline.add_node(WorkflowNode("Slow", slow_step), is_start=True)
    
    results = pipeline.execute()
    
    assert results["status"] == "completed", "Pipeline should complete"
    assert results["total_time"] >= 0.1, "Total time should be at least 0.1s"
    assert results["nodes"]["Slow"]["execution_time"] >= 0.1, "Node time should be at least 0.1s"
    
    print("✓ Test 6 passed: Timing tracking works correctly\n")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "#"*60)
    print("# WORKFLOW MODULE TESTS")
    print("#"*60)
    
    tests = [
        ("Basic Pipeline", test_basic_pipeline),
        ("Branching Pipeline", test_branching_pipeline),
        ("Simple Pipeline Helper", test_simple_pipeline_helper),
        ("Error Handling", test_error_handling),
        ("Parameter Filtering", test_parameter_filtering),
        ("Execution Timing", test_execution_timing),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ Test failed: {test_name}")
            print(f"  Error: {e}\n")
    
    print("\n" + "#"*60)
    print(f"# TEST SUMMARY: {passed} passed, {failed} failed")
    print("#"*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
