# Workflow Integration Guide

This guide shows how to integrate the workflow system with existing msk_modelling_python functions.

## Integration Patterns

### Pattern 1: Wrapping Existing Functions

Wrap your existing functions to make them workflow-compatible:

```python
from msk_modelling_python.workflow import Pipeline, WorkflowNode
import msk_modelling_python as msk

# Your existing function
def my_existing_analysis(subject_path, trial_name):
    # ... existing code ...
    return result

# Workflow wrapper
def workflow_analysis(subject_path, trial_name):
    """Wrapper for existing analysis function."""
    result = my_existing_analysis(subject_path, trial_name)
    # Return as dictionary for workflow compatibility
    return {"analysis_result": result, "subject": subject_path}

# Use in pipeline
node = WorkflowNode("Analysis", workflow_analysis, {
    "subject_path": "/path/to/subject",
    "trial_name": "trial01"
})
```

### Pattern 2: Direct Integration with BOPS

```python
from msk_modelling_python import bops as bp
from msk_modelling_python.workflow import Pipeline, WorkflowNode

def run_ik_wrapper(model_path, marker_path, output_folder):
    """Wrapper for bops.run_inverse_kinematics."""
    ik_output = bp.run_inverse_kinematics(
        model_file=model_path,
        marker_file=marker_path,
        output_folder=output_folder
    )
    return {
        "ik_output": ik_output,
        "status": "completed"
    }

# Create pipeline
pipeline = Pipeline("IK Pipeline")
ik_node = WorkflowNode("IK", run_ik_wrapper, {
    "model_path": "/path/to/model.osim",
    "marker_path": "/path/to/markers.trc",
    "output_folder": "/path/to/output"
})
pipeline.add_node(ik_node, is_start=True)
pipeline.execute()
```

### Pattern 3: Converting Example Scripts to Workflows

Take existing example scripts and convert them to workflows:

**Before (traditional script):**
```python
# example_run.py
import msk_modelling_python.src.ceinms_setup as cs

data_folder = cs.get_main_path()
subject_name = 'Athlete_03'
trial_name = 'sq_90'

paths = cs.subject_paths(data_folder, subject_name, trial_name)
cs.run_so(paths, rerun=True)
cs.run_jra(paths, rerun=True)
print('done!')
```

**After (workflow):**
```python
# workflow_run.py
from msk_modelling_python.workflow import Pipeline, WorkflowNode
import msk_modelling_python.src.ceinms_setup as cs

def setup_paths(data_folder, subject_name, trial_name):
    paths = cs.subject_paths(data_folder, subject_name, trial_name)
    return {"paths": paths}

def run_so_node(paths):
    cs.run_so(paths, rerun=True)
    return {"so_completed": True}

def run_jra_node(paths):
    cs.run_jra(paths, rerun=True)
    return {"jra_completed": True}

# Create workflow
pipeline = Pipeline("CEINMS Analysis", "SO and JRA analysis")

setup = WorkflowNode("Setup", setup_paths, {
    "data_folder": cs.get_main_path(),
    "subject_name": "Athlete_03",
    "trial_name": "sq_90"
})
so = WorkflowNode("Static Optimization", run_so_node)
jra = WorkflowNode("Joint Reaction", run_jra_node)

pipeline.add_node(setup, is_start=True)
pipeline.add_node(so)
pipeline.add_node(jra)

pipeline.connect("Setup", "Static Optimization")
pipeline.connect("Static Optimization", "Joint Reaction")

results = pipeline.execute()
print('Workflow completed!')
```

### Pattern 4: Multi-Subject Processing

```python
from msk_modelling_python.workflow import Pipeline, WorkflowNode
import msk_modelling_python.src.bops as bp

def load_project(project_folder):
    """Load project settings and subject list."""
    settings = bp.create_project_settings(project_folder)
    return {
        "subjects": settings['subject_list'],
        "project_folder": project_folder
    }

def process_subject(subjects, project_folder, current_idx=0):
    """Process one subject."""
    if current_idx >= len(subjects):
        return {"done": True}
    
    subject = subjects[current_idx]
    print(f"Processing {subject}")
    
    # Your processing code here
    # e.g., run_ik, run_id, run_so for this subject
    
    return {
        "processed_subject": subject,
        "current_idx": current_idx + 1
    }

def summarize_results(subjects):
    """Create summary report."""
    report = {
        "total_subjects": len(subjects),
        "report_file": "summary.txt"
    }
    
    with open(report["report_file"], 'w') as f:
        f.write(f"Processed {len(subjects)} subjects\n")
    
    return report

# Create batch pipeline
pipeline = Pipeline("Batch Processing")
pipeline.add_node(WorkflowNode("Load", load_project, 
                               {"project_folder": "/path/to/project"}), 
                  is_start=True)
pipeline.add_node(WorkflowNode("Process", process_subject))
pipeline.add_node(WorkflowNode("Summarize", summarize_results))

pipeline.connect("Load", "Process")
pipeline.connect("Process", "Summarize")

pipeline.execute()
```

## Best Practices

### 1. Return Dictionaries

Always return dictionaries from your node functions:

```python
# Good
def my_function(input_data):
    result = process(input_data)
    return {"result": result, "status": "success"}

# Avoid
def my_function(input_data):
    return process(input_data)  # Single value, not dict
```

### 2. Error Handling

Add error handling in your wrapper functions:

```python
def safe_processing_node(data_path):
    try:
        result = process_data(data_path)
        return {"result": result, "status": "success"}
    except Exception as e:
        print(f"Error processing {data_path}: {e}")
        return {"result": None, "status": "failed", "error": str(e)}
```

### 3. Logging

Integrate with existing logging:

```python
from msk_modelling_python.workflow import Pipeline, WorkflowNode
import msk_modelling_python.src.ceinms_setup as cs

def logged_analysis(subject_name, trial_name):
    cs.print_to_log_file('Running analysis', subject_name, mode='start')
    
    # Your analysis code
    result = run_analysis(subject_name, trial_name)
    
    cs.print_to_log_file('Analysis complete', '', mode='simple')
    
    return {"result": result}
```

### 4. File Path Management

Use the workflow system to manage file paths:

```python
def setup_paths(project_folder, subject, trial):
    """Setup all required paths."""
    paths = {
        "model": f"{project_folder}/models/{subject}.osim",
        "markers": f"{project_folder}/data/{subject}/{trial}/markers.trc",
        "ik_output": f"{project_folder}/results/{subject}/{trial}/IK.mot",
        "id_output": f"{project_folder}/results/{subject}/{trial}/ID.sto",
    }
    
    # Create output directories
    import os
    os.makedirs(os.path.dirname(paths["ik_output"]), exist_ok=True)
    
    return paths

# Use in pipeline
setup_node = WorkflowNode("Setup", setup_paths, {
    "project_folder": "/path/to/project",
    "subject": "Subject01",
    "trial": "walking"
})
```

### 5. Reusable Node Functions

Create a library of reusable node functions:

```python
# workflow_nodes.py
"""Reusable workflow nodes for MSK analysis."""

def create_ik_node(model_path, marker_path, output_path):
    """Create a pre-configured IK node."""
    def run_ik(model_path, marker_path, output_path):
        # IK implementation
        return {"ik_output": output_path}
    
    return WorkflowNode("IK", run_ik, {
        "model_path": model_path,
        "marker_path": marker_path,
        "output_path": output_path
    }, "Inverse Kinematics Analysis")

def create_id_node():
    """Create a pre-configured ID node."""
    def run_id(model_path, ik_output, output_path):
        # ID implementation
        return {"id_output": output_path}
    
    return WorkflowNode("ID", run_id, 
                       description="Inverse Dynamics Analysis")

# Use in your scripts
from workflow_nodes import create_ik_node, create_id_node

pipeline = Pipeline("Analysis")
pipeline.add_node(create_ik_node("/path/to/model", "/path/to/markers", "/path/to/output"))
pipeline.add_node(create_id_node())
```

## Migration Strategy

### Step 1: Identify Your Workflow

Look at your existing script and identify the steps:

```python
# Existing script steps:
# 1. Load data
# 2. Filter data
# 3. Run IK
# 4. Run ID
# 5. Create plots
# 6. Generate report
```

### Step 2: Wrap Each Step

Create wrapper functions:

```python
def step1_load_data(filepath):
    # existing code
    return {"data": data}

def step2_filter_data(data, cutoff=6):
    # existing code
    return {"filtered_data": filtered}

# ... etc
```

### Step 3: Build the Pipeline

```python
pipeline = Pipeline("My Analysis")

node1 = WorkflowNode("Load", step1_load_data, {"filepath": "/path"})
node2 = WorkflowNode("Filter", step2_filter_data, {"cutoff": 6})
# ... etc

pipeline.add_node(node1, is_start=True)
pipeline.add_node(node2)
# ... etc

pipeline.connect("Load", "Filter")
# ... etc
```

### Step 4: Test and Refine

Run the pipeline and adjust as needed:

```python
# Visualize first
print(pipeline.visualize())

# Execute
results = pipeline.execute()

# Check results
print(f"Status: {results['status']}")
print(f"Time: {results['total_time']:.2f}s")
```

## Common Use Cases

### Use Case 1: Subject Analysis Pipeline

```python
tasks = [
    ("Load Subject", load_subject_data, {"subject": "S01"}, "Load subject data"),
    ("Scale Model", scale_model, {}, "Scale generic model"),
    ("Run IK", run_ik, {}, "Inverse Kinematics"),
    ("Run ID", run_id, {}, "Inverse Dynamics"),
    ("Run SO", run_so, {}, "Static Optimization"),
    ("Generate Report", create_report, {}, "Create analysis report")
]

pipeline = create_simple_pipeline("Subject Analysis", tasks)
pipeline.execute()
```

### Use Case 2: Data Processing Pipeline

```python
pipeline = Pipeline("Data Processing")

import_node = WorkflowNode("Import C3D", import_c3d, {"file": "trial.c3d"})
filter_node = WorkflowNode("Filter", filter_signals, {"cutoff": 6})
export_node = WorkflowNode("Export", export_to_opensim, {})

pipeline.add_node(import_node, is_start=True)
pipeline.add_node(filter_node)
pipeline.add_node(export_node)

pipeline.connect("Import C3D", "Filter")
pipeline.connect("Filter", "Export")

pipeline.execute()
```

### Use Case 3: Comparison Study

```python
def run_analysis_generic(subject, trial):
    """Run with generic model."""
    # analysis code
    return {"generic_results": results}

def run_analysis_personalized(subject, trial):
    """Run with personalized model."""
    # analysis code
    return {"personalized_results": results}

def compare_results(generic_results, personalized_results):
    """Compare the two analyses."""
    # comparison code
    return {"comparison": comparison}

pipeline = Pipeline("Model Comparison Study")

generic_node = WorkflowNode("Generic Model", run_analysis_generic, {
    "subject": "S01", "trial": "walking"
})
personalized_node = WorkflowNode("Personalized Model", run_analysis_personalized, {
    "subject": "S01", "trial": "walking"
})
compare_node = WorkflowNode("Compare", compare_results)

pipeline.add_node(generic_node, is_start=True)
pipeline.add_node(personalized_node, is_start=True)  # Parallel execution
pipeline.add_node(compare_node)

pipeline.connect("Generic Model", "Compare")
pipeline.connect("Personalized Model", "Compare")

pipeline.execute()
```

## Troubleshooting

### Issue 1: Function Parameter Mismatch

**Problem:** `TypeError: function() got an unexpected keyword argument 'x'`

**Solution:** The workflow passes all context variables. Make sure your function only accepts the parameters it needs, or use `**kwargs`:

```python
# Option 1: Specific parameters
def my_function(param1, param2):
    # ...

# Option 2: Accept extra parameters
def my_function(param1, param2, **kwargs):
    # kwargs will catch extra parameters
    # ...
```

### Issue 2: Missing Required Parameters

**Problem:** `TypeError: function() missing required positional argument 'x'`

**Solution:** Ensure required parameters are provided either in node inputs or from previous nodes:

```python
# Provide in node inputs
node = WorkflowNode("My Node", my_function, {
    "required_param": "value"
})

# Or ensure previous node outputs it
previous_node_function(...):
    return {"required_param": "value"}
```

### Issue 3: Node Not Executing

**Problem:** A node never runs

**Solution:** Check connections - the node must be connected from the start node:

```python
# Visualize to check connections
print(pipeline.visualize())
```

## Summary

The workflow system provides a structured way to organize your analysis code:

1. **Break down** your analysis into discrete steps
2. **Wrap** each step in a function that returns a dictionary
3. **Create** nodes for each step
4. **Connect** nodes to define execution order
5. **Execute** and monitor the pipeline

This approach makes your code more:
- **Modular**: Easy to swap or update individual steps
- **Reusable**: Share and reuse workflows across projects
- **Maintainable**: Clear structure and documentation
- **Debuggable**: Easy to identify where issues occur
- **Reproducible**: Same workflow = same results
