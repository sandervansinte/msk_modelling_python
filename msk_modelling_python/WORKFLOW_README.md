# Workflow Pipeline System

A Python workflow automation system inspired by [n8n](https://github.com/n8n-io/n8n), designed for musculoskeletal modeling pipelines.

## Overview

This module provides a simple yet powerful way to create and execute data processing pipelines. It allows you to:

- Define workflows as a series of connected nodes (tasks)
- Execute tasks in sequence with automatic data flow
- Monitor execution progress and timing
- Handle errors gracefully
- Visualize pipeline structure
- Save and share pipeline definitions

## Key Concepts

### Pipeline
A `Pipeline` is a container for a complete workflow. It manages nodes, executions, and provides monitoring capabilities.

### WorkflowNode
A `WorkflowNode` represents a single task or operation in your pipeline. Each node:
- Has a unique name
- Executes a specific function
- Can receive inputs from previous nodes
- Produces outputs for subsequent nodes
- Tracks its execution status and timing

### Connections
Nodes are connected to define the flow of data and execution order. The output of one node automatically becomes available as input to connected nodes.

## Quick Start

### Basic Example

```python
from msk_modelling_python.workflow import Pipeline, WorkflowNode

# Define your task functions
def load_data(filepath):
    print(f"Loading {filepath}")
    return {"data": "my_data"}

def process_data(data):
    print(f"Processing {data}")
    return {"result": f"{data}_processed"}

# Create pipeline
pipeline = Pipeline("My Pipeline", "A simple data processing pipeline")

# Create nodes
load_node = WorkflowNode("Load", load_data, {"filepath": "/path/to/file.csv"})
process_node = WorkflowNode("Process", process_data)

# Add nodes to pipeline
pipeline.add_node(load_node, is_start=True)
pipeline.add_node(process_node)

# Connect nodes
pipeline.connect("Load", "Process")

# Execute pipeline
results = pipeline.execute()
```

### OpenSim Analysis Example

```python
from msk_modelling_python.workflow import Pipeline, WorkflowNode

def run_ik(model_path, markers_path):
    # Run inverse kinematics
    ik_output = "/path/to/ik.mot"
    # ... your IK code here ...
    return {"ik_output": ik_output}

def run_id(model_path, ik_output):
    # Run inverse dynamics
    id_output = "/path/to/id.sto"
    # ... your ID code here ...
    return {"id_output": id_output}

def run_so(model_path, ik_output):
    # Run static optimization
    so_output = "/path/to/so"
    # ... your SO code here ...
    return {"so_output": so_output}

# Create OpenSim pipeline
pipeline = Pipeline("OpenSim Analysis", "IK -> ID + SO pipeline")

ik_node = WorkflowNode("IK", run_ik, {
    "model_path": "/path/to/model.osim",
    "markers_path": "/path/to/markers.trc"
})

id_node = WorkflowNode("ID", run_id)
so_node = WorkflowNode("SO", run_so)

pipeline.add_node(ik_node, is_start=True)
pipeline.add_node(id_node)
pipeline.add_node(so_node)

# IK feeds into both ID and SO
pipeline.connect("IK", "ID")
pipeline.connect("IK", "SO")

# Execute
results = pipeline.execute()
```

## Features

### 1. Automatic Data Flow

Outputs from one node automatically become available to connected nodes:

```python
# Node 1 outputs: {"data": "value"}
# Node 2 can access "data" as a parameter
def node2_function(data):
    print(data)  # Will print "value"
```

### 2. Pipeline Visualization

See your pipeline structure:

```python
pipeline = Pipeline("My Pipeline")
# ... add nodes and connections ...

print(pipeline.visualize())
# Output:
# Pipeline: My Pipeline
# Flow:
# Start Node
#   └─ Process Node
#     └─ Save Node
```

### 3. Execution Monitoring

Track execution status and timing:

```python
results = pipeline.execute()

print(f"Status: {results['status']}")
print(f"Total time: {results['total_time']:.2f}s")

for node_name, node_info in results['nodes'].items():
    print(f"{node_name}: {node_info['status']} ({node_info['execution_time']:.2f}s)")
```

### 4. Error Handling

Control how errors are handled:

```python
# Stop on first error (default)
results = pipeline.execute(stop_on_error=True)

# Continue despite errors
results = pipeline.execute(stop_on_error=False)
```

### 5. Save Pipeline Definitions

Save your pipeline structure to JSON:

```python
pipeline.save_to_json("my_pipeline.json")
```

## Advanced Usage

### Simple Linear Pipelines

For simple sequential workflows, use the helper function:

```python
from msk_modelling_python.workflow import create_simple_pipeline

tasks = [
    ("Load", load_function, {"filepath": "/path/to/file"}, "Load data"),
    ("Process", process_function, {}, "Process data"),
    ("Save", save_function, {"output": "/path/to/output"}, "Save results")
]

pipeline = create_simple_pipeline("My Pipeline", tasks, "Process data from A to B")
pipeline.execute()
```

### Branching Workflows

Create pipelines with multiple branches where one node feeds into multiple:

```python
pipeline = Pipeline("Branching Pipeline")

# One node can feed into multiple nodes (fan-out)
pipeline.connect("Load", "Process_A")
pipeline.connect("Load", "Process_B")
pipeline.connect("Load", "Process_C")
```

**Note**: Currently, merging multiple branches into one node (fan-in) requires manual handling. Use sequential processing or ensure dependencies are properly ordered:

```python
# Workaround for merge nodes
def process_all(data):
    result_a = process_a(data)
    result_b = process_b(data)
    return {"result_a": result_a, "result_b": result_b, "merged": merge(result_a, result_b)}
```

### Context Management

Pass initial context to your pipeline:

```python
initial_context = {
    "project_folder": "/path/to/project",
    "subject_list": ["Subject01", "Subject02"],
    "cutoff_frequency": 6
}

results = pipeline.execute(initial_context=initial_context)

# Access final context with all outputs
final_data = results['final_context']
```

### Node Descriptions

Add descriptions to help document your pipeline:

```python
node = WorkflowNode(
    name="Process Data",
    function=process_function,
    inputs={"param": "value"},
    description="Apply butterworth filter and normalize data"
)
```

## Real-World Examples

### Complete OpenSim Analysis Pipeline

```python
from msk_modelling_python.workflow import Pipeline, WorkflowNode

def setup_paths(project_folder, subject_name, trial_name):
    paths = {
        "model": f"{project_folder}/models/{subject_name}.osim",
        "markers": f"{project_folder}/data/{subject_name}/{trial_name}/markers.trc",
        "output": f"{project_folder}/results/{subject_name}/{trial_name}"
    }
    os.makedirs(paths["output"], exist_ok=True)
    return paths

def run_ik(model, markers, output):
    ik_output = f"{output}/IK.mot"
    # Run IK using your preferred method
    return {"ik_output": ik_output}

def run_id(model, ik_output, output):
    id_output = f"{output}/ID.sto"
    # Run ID
    return {"id_output": id_output}

def run_so(model, ik_output, output):
    so_output = f"{output}/SO"
    # Run SO
    return {"so_output": so_output}

def run_jra(model, so_output, output):
    jra_output = f"{output}/JRA.sto"
    # Run JRA
    return {"jra_output": jra_output}

# Build pipeline
pipeline = Pipeline("Complete OpenSim Analysis", "Full analysis pipeline")

setup_node = WorkflowNode("Setup", setup_paths, {
    "project_folder": "/path/to/project",
    "subject_name": "Subject01",
    "trial_name": "walking"
})
ik_node = WorkflowNode("IK", run_ik, description="Inverse Kinematics")
id_node = WorkflowNode("ID", run_id, description="Inverse Dynamics")
so_node = WorkflowNode("SO", run_so, description="Static Optimization")
jra_node = WorkflowNode("JRA", run_jra, description="Joint Reaction Analysis")

pipeline.add_node(setup_node, is_start=True)
pipeline.add_node(ik_node)
pipeline.add_node(id_node)
pipeline.add_node(so_node)
pipeline.add_node(jra_node)

pipeline.connect("Setup", "IK")
pipeline.connect("IK", "ID")
pipeline.connect("IK", "SO")
pipeline.connect("SO", "JRA")

# Run
pipeline.execute()
```

### Batch Processing Pipeline

```python
def load_subject_list(project_folder):
    subjects = os.listdir(f"{project_folder}/data")
    return {"subjects": subjects}

def process_subject(subjects, subject_idx, project_folder):
    if subject_idx >= len(subjects):
        return {"done": True}
    
    subject = subjects[subject_idx]
    # Process subject...
    
    return {"processed": subject}

def aggregate_results(subjects, project_folder):
    # Combine results from all subjects
    summary = {"total": len(subjects)}
    return summary

# Create batch pipeline
tasks = [
    ("Load Subjects", load_subject_list, {"project_folder": "/path"}, "Get subject list"),
    ("Process All", process_subject, {}, "Process each subject"),
    ("Aggregate", aggregate_results, {}, "Combine results")
]

batch_pipeline = create_simple_pipeline("Batch Processing", tasks)
batch_pipeline.execute()
```

## Comparison with n8n

| Feature | n8n | This Module |
|---------|-----|-------------|
| Visual Editor | ✅ Yes | ❌ No (code-based) |
| Node Execution | ✅ Yes | ✅ Yes |
| Data Flow | ✅ Automatic | ✅ Automatic |
| Error Handling | ✅ Yes | ✅ Yes |
| Workflow Monitoring | ✅ Yes | ✅ Yes |
| Execution Logging | ✅ Yes | ✅ Yes |
| Language | JavaScript/TypeScript | Python |
| Use Case | General automation | MSK modeling pipelines |

## Benefits

1. **Reproducibility**: Define your analysis pipeline once, run it many times
2. **Clarity**: Clear visualization of workflow structure
3. **Debugging**: Easy to identify which step failed and why
4. **Modularity**: Reuse nodes across different pipelines
5. **Monitoring**: Track execution time and status of each step
6. **Documentation**: Self-documenting workflows with descriptions

## Tips

1. **Keep nodes focused**: Each node should do one thing well
2. **Use descriptive names**: Make node names and descriptions clear
3. **Handle errors**: Add try-except blocks in your functions for robustness
4. **Test incrementally**: Build and test your pipeline one node at a time
5. **Visualize first**: Use `pipeline.visualize()` before executing
6. **Log important data**: Return dictionaries with all relevant outputs

## See Also

- [n8n workflow automation](https://github.com/n8n-io/n8n)
- Example workflows in `example_data/workflow_example.py`
- OpenSim documentation: https://simtk.org/projects/opensim

## License

Same license as msk_modelling_python package (MIT).
