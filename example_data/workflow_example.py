"""
Example workflow pipelines for musculoskeletal modeling
Using the n8n-inspired workflow system

Author: Basilio Goncalves
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from msk_modelling_python.workflow import Pipeline, WorkflowNode, create_simple_pipeline


def example_opensim_pipeline():
    """
    Example OpenSim processing pipeline.
    This demonstrates how to chain IK -> ID -> SO -> JRA analyses.
    """
    
    # Define task functions
    def setup_paths(project_folder, subject_name, trial_name):
        """Setup file paths for the analysis."""
        print(f"  Setting up paths for {subject_name}/{trial_name}")
        
        paths = {
            "project_folder": project_folder,
            "subject_name": subject_name,
            "trial_name": trial_name,
            "model_path": os.path.join(project_folder, "models", f"{subject_name}_scaled.osim"),
            "markers_path": os.path.join(project_folder, "data", subject_name, trial_name, "markers.trc"),
            "output_folder": os.path.join(project_folder, "results", subject_name, trial_name)
        }
        
        os.makedirs(paths["output_folder"], exist_ok=True)
        
        return paths
    
    def run_inverse_kinematics(model_path, markers_path, output_folder):
        """Run Inverse Kinematics."""
        print(f"  Running IK...")
        print(f"    Model: {os.path.basename(model_path)}")
        print(f"    Markers: {os.path.basename(markers_path)}")
        
        ik_output = os.path.join(output_folder, "IK.mot")
        
        # In real implementation, would call:
        # msk.bops.run_inverse_kinematics(model_path, markers_path, ik_output)
        
        return {
            "ik_output": ik_output,
            "ik_status": "completed"
        }
    
    def run_inverse_dynamics(model_path, ik_output, output_folder):
        """Run Inverse Dynamics."""
        print(f"  Running ID...")
        print(f"    IK results: {os.path.basename(ik_output)}")
        
        id_output = os.path.join(output_folder, "ID.sto")
        
        # In real implementation, would call:
        # msk.bops.run_inverse_dynamics(model_path, ik_output, id_output)
        
        return {
            "id_output": id_output,
            "id_status": "completed"
        }
    
    def run_static_optimization(model_path, ik_output, output_folder):
        """Run Static Optimization."""
        print(f"  Running Static Optimization...")
        
        so_output = os.path.join(output_folder, "SO")
        
        # In real implementation, would call:
        # msk.bops.run_static_optimization(model_path, ik_output, so_output)
        
        return {
            "so_output": so_output,
            "so_status": "completed"
        }
    
    def run_joint_reaction_analysis(model_path, so_output, output_folder):
        """Run Joint Reaction Analysis."""
        print(f"  Running JRA...")
        
        jra_output = os.path.join(output_folder, "JRA.sto")
        
        # In real implementation, would call:
        # msk.bops.run_jra(model_path, so_output, jra_output)
        
        return {
            "jra_output": jra_output,
            "jra_status": "completed"
        }
    
    def generate_report(output_folder, subject_name, trial_name):
        """Generate analysis report."""
        print(f"  Generating report for {subject_name}/{trial_name}")
        
        report_path = os.path.join(output_folder, "analysis_report.txt")
        
        with open(report_path, 'w') as f:
            f.write(f"Analysis Report\n")
            f.write(f"Subject: {subject_name}\n")
            f.write(f"Trial: {trial_name}\n")
            f.write(f"All analyses completed successfully.\n")
        
        return {
            "report_path": report_path,
            "report_status": "completed"
        }
    
    # Create the pipeline
    pipeline = Pipeline(
        "OpenSim Analysis Pipeline",
        "Complete OpenSim analysis: IK -> ID -> SO -> JRA"
    )
    
    # Create nodes
    setup_node = WorkflowNode(
        "Setup Paths",
        setup_paths,
        {
            "project_folder": "/path/to/project",
            "subject_name": "Subject01",
            "trial_name": "walking_01"
        },
        "Initialize file paths and directories"
    )
    
    ik_node = WorkflowNode(
        "Inverse Kinematics",
        run_inverse_kinematics,
        description="Calculate joint angles from marker data"
    )
    
    id_node = WorkflowNode(
        "Inverse Dynamics",
        run_inverse_dynamics,
        description="Calculate joint moments and forces"
    )
    
    so_node = WorkflowNode(
        "Static Optimization",
        run_static_optimization,
        description="Estimate muscle forces"
    )
    
    jra_node = WorkflowNode(
        "Joint Reaction Analysis",
        run_joint_reaction_analysis,
        description="Calculate joint reaction forces"
    )
    
    report_node = WorkflowNode(
        "Generate Report",
        generate_report,
        description="Create analysis summary report"
    )
    
    # Add nodes to pipeline
    pipeline.add_node(setup_node, is_start=True)
    pipeline.add_node(ik_node)
    pipeline.add_node(id_node)
    pipeline.add_node(so_node)
    pipeline.add_node(jra_node)
    pipeline.add_node(report_node)
    
    # Connect nodes (define workflow)
    pipeline.connect("Setup Paths", "Inverse Kinematics")
    pipeline.connect("Inverse Kinematics", "Inverse Dynamics")
    pipeline.connect("Inverse Kinematics", "Static Optimization")  # SO also depends on IK
    pipeline.connect("Static Optimization", "Joint Reaction Analysis")
    pipeline.connect("Joint Reaction Analysis", "Generate Report")
    
    return pipeline


def example_batch_processing_pipeline():
    """
    Example batch processing pipeline for multiple subjects/trials.
    """
    
    def load_subjects(project_folder):
        """Load list of subjects from project."""
        print(f"  Loading subjects from {project_folder}")
        
        subjects = ["Subject01", "Subject02", "Subject03"]
        trials = ["walking_01", "running_01"]
        
        return {
            "subjects": subjects,
            "trials": trials
        }
    
    def process_subject(subjects, trials, subject_idx=0):
        """Process a single subject (all trials)."""
        subject = subjects[subject_idx] if subject_idx < len(subjects) else None
        if not subject:
            return {"status": "no_more_subjects"}
        
        print(f"  Processing {subject}")
        
        for trial in trials:
            print(f"    - Trial: {trial}")
            # Here you would run the OpenSim pipeline for each trial
        
        return {
            "processed_subject": subject,
            "status": "completed"
        }
    
    def aggregate_results(subjects):
        """Aggregate results from all subjects."""
        print(f"  Aggregating results from {len(subjects)} subjects")
        
        summary = {
            "total_subjects": len(subjects),
            "status": "completed"
        }
        
        return summary
    
    # Create pipeline using the helper function
    tasks = [
        ("Load Subjects", load_subjects, {"project_folder": "/path/to/project"}, 
         "Load subject and trial lists"),
        ("Process Subjects", process_subject, {}, 
         "Process all subjects and trials"),
        ("Aggregate Results", aggregate_results, {}, 
         "Combine results from all subjects")
    ]
    
    pipeline = create_simple_pipeline(
        "Batch Processing Pipeline",
        tasks,
        "Process multiple subjects and aggregate results"
    )
    
    return pipeline


def example_data_processing_pipeline():
    """
    Example data processing pipeline for C3D files.
    """
    
    def import_c3d(c3d_filepath):
        """Import C3D file."""
        print(f"  Importing C3D: {os.path.basename(c3d_filepath)}")
        
        return {
            "markers": "marker_data",
            "forces": "force_data",
            "emg": "emg_data"
        }
    
    def filter_data(markers, forces, emg, cutoff_freq=6):
        """Filter marker and force data."""
        print(f"  Filtering data (cutoff: {cutoff_freq} Hz)")
        
        return {
            "filtered_markers": f"{markers}_filtered",
            "filtered_forces": f"{forces}_filtered",
            "filtered_emg": f"{emg}_filtered"
        }
    
    def export_to_opensim(filtered_markers, filtered_forces, output_folder):
        """Export to OpenSim formats."""
        print(f"  Exporting to OpenSim formats")
        
        trc_file = os.path.join(output_folder, "markers.trc")
        mot_file = os.path.join(output_folder, "forces.mot")
        
        return {
            "trc_file": trc_file,
            "mot_file": mot_file,
            "export_status": "completed"
        }
    
    # Create pipeline
    pipeline = Pipeline(
        "Data Processing Pipeline",
        "Import, filter, and export C3D data for OpenSim"
    )
    
    # Add nodes
    import_node = WorkflowNode(
        "Import C3D",
        import_c3d,
        {"c3d_filepath": "/path/to/data.c3d"},
        "Import marker, force, and EMG data"
    )
    
    filter_node = WorkflowNode(
        "Filter Data",
        filter_data,
        {"cutoff_freq": 6},
        "Apply low-pass filter to data"
    )
    
    export_node = WorkflowNode(
        "Export to OpenSim",
        export_to_opensim,
        {"output_folder": "/path/to/output"},
        "Export TRC and MOT files"
    )
    
    pipeline.add_node(import_node, is_start=True)
    pipeline.add_node(filter_node)
    pipeline.add_node(export_node)
    
    pipeline.connect("Import C3D", "Filter Data")
    pipeline.connect("Filter Data", "Export to OpenSim")
    
    return pipeline


def run_all_examples():
    """Run all example pipelines."""
    
    print("\n" + "="*70)
    print("WORKFLOW PIPELINE EXAMPLES")
    print("Inspired by n8n workflow automation")
    print("="*70)
    
    # Example 1: OpenSim Pipeline
    print("\n\n1. OpenSim Analysis Pipeline")
    print("-" * 70)
    opensim_pipeline = example_opensim_pipeline()
    print(opensim_pipeline.visualize())
    opensim_pipeline.execute()
    
    # Example 2: Batch Processing
    print("\n\n2. Batch Processing Pipeline")
    print("-" * 70)
    batch_pipeline = example_batch_processing_pipeline()
    print(batch_pipeline.visualize())
    batch_pipeline.execute()
    
    # Example 3: Data Processing
    print("\n\n3. Data Processing Pipeline")
    print("-" * 70)
    data_pipeline = example_data_processing_pipeline()
    print(data_pipeline.visualize())
    data_pipeline.execute()
    
    print("\n\n" + "="*70)
    print("All examples completed!")
    print("="*70)


if __name__ == "__main__":
    run_all_examples()
