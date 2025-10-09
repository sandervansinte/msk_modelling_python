"""
Complete OpenSim Analysis Workflow Example
This demonstrates a realistic workflow for musculoskeletal modeling analysis
using the n8n-inspired pipeline system.

Author: Basilio Goncalves
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import directly to avoid dependency issues in examples
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'msk_modelling_python'))
from workflow import Pipeline, WorkflowNode, create_simple_pipeline


def create_opensim_pipeline(project_folder, subject_name, trial_name):
    """
    Create a complete OpenSim analysis pipeline.
    
    Pipeline steps:
    1. Setup paths and directories
    2. Load and validate input files
    3. Run Inverse Kinematics (IK)
    4. Run Inverse Dynamics (ID)
    5. Run Static Optimization (SO)
    6. Run Joint Reaction Analysis (JRA)
    7. Generate analysis report
    
    Args:
        project_folder: Path to project directory
        subject_name: Subject identifier
        trial_name: Trial identifier
        
    Returns:
        Configured Pipeline object ready to execute
    """
    
    # Step 1: Setup paths
    def setup_paths(project_folder, subject_name, trial_name):
        """Initialize all file paths for the analysis."""
        print(f"  Setting up paths for {subject_name}/{trial_name}")
        
        paths = {
            "project_folder": project_folder,
            "subject_name": subject_name,
            "trial_name": trial_name,
            "model_scaled": os.path.join(project_folder, "models", f"{subject_name}_scaled.osim"),
            "markers_trc": os.path.join(project_folder, "data", subject_name, trial_name, "markers.trc"),
            "grf_mot": os.path.join(project_folder, "data", subject_name, trial_name, "grf.mot"),
            "output_dir": os.path.join(project_folder, "results", subject_name, trial_name),
        }
        
        # Create output directory
        os.makedirs(paths["output_dir"], exist_ok=True)
        
        # Set output file paths
        paths["ik_output"] = os.path.join(paths["output_dir"], "IK.mot")
        paths["id_output"] = os.path.join(paths["output_dir"], "ID.sto")
        paths["so_output"] = os.path.join(paths["output_dir"], "SO")
        paths["jra_output"] = os.path.join(paths["output_dir"], "JRA.sto")
        paths["report_output"] = os.path.join(paths["output_dir"], "analysis_report.txt")
        
        print(f"  Output directory: {paths['output_dir']}")
        return paths
    
    # Step 2: Validate inputs
    def validate_inputs(model_scaled, markers_trc, grf_mot):
        """Validate that all required input files exist."""
        print(f"  Validating input files...")
        
        files_to_check = {
            "Model": model_scaled,
            "Markers": markers_trc,
            "GRF": grf_mot
        }
        
        missing_files = []
        for name, filepath in files_to_check.items():
            if not os.path.exists(filepath):
                missing_files.append(f"{name}: {filepath}")
                print(f"    ⚠ Missing: {name}")
            else:
                print(f"    ✓ Found: {name}")
        
        if missing_files:
            print(f"  ⚠ Warning: {len(missing_files)} file(s) not found (demo mode)")
        
        return {
            "validation_status": "ok" if not missing_files else "missing_files",
            "missing_files": missing_files
        }
    
    # Step 3: Run Inverse Kinematics
    def run_inverse_kinematics(model_scaled, markers_trc, ik_output):
        """Run OpenSim Inverse Kinematics analysis."""
        print(f"  Running Inverse Kinematics...")
        print(f"    Model: {os.path.basename(model_scaled)}")
        print(f"    Markers: {os.path.basename(markers_trc)}")
        print(f"    Output: {os.path.basename(ik_output)}")
        
        # In real implementation:
        # import msk_modelling_python as msk
        # msk.bops.run_inverse_kinematics(model_scaled, markers_trc, ik_output)
        
        # Demo: Create placeholder output
        print(f"    [Demo mode: IK would be executed here]")
        
        return {
            "ik_status": "completed",
            "ik_duration": 15.2,  # seconds
            "ik_rms_error": 0.012  # meters
        }
    
    # Step 4: Run Inverse Dynamics
    def run_inverse_dynamics(model_scaled, ik_output, grf_mot, id_output):
        """Run OpenSim Inverse Dynamics analysis."""
        print(f"  Running Inverse Dynamics...")
        print(f"    IK results: {os.path.basename(ik_output)}")
        print(f"    GRF data: {os.path.basename(grf_mot)}")
        print(f"    Output: {os.path.basename(id_output)}")
        
        # In real implementation:
        # import msk_modelling_python as msk
        # msk.bops.run_inverse_dynamics(model_scaled, ik_output, grf_mot, id_output)
        
        print(f"    [Demo mode: ID would be executed here]")
        
        return {
            "id_status": "completed",
            "id_duration": 8.5,
            "max_hip_moment": 125.3  # Nm
        }
    
    # Step 5: Run Static Optimization
    def run_static_optimization(model_scaled, ik_output, grf_mot, so_output):
        """Run OpenSim Static Optimization analysis."""
        print(f"  Running Static Optimization...")
        print(f"    IK results: {os.path.basename(ik_output)}")
        print(f"    Output directory: {os.path.basename(so_output)}")
        
        # In real implementation:
        # import msk_modelling_python as msk
        # msk.bops.run_static_optimization(model_scaled, ik_output, grf_mot, so_output)
        
        print(f"    [Demo mode: SO would be executed here]")
        
        return {
            "so_status": "completed",
            "so_duration": 45.7,
            "rms_residual": 0.023
        }
    
    # Step 6: Run Joint Reaction Analysis
    def run_joint_reaction_analysis(model_scaled, ik_output, so_output, jra_output):
        """Run OpenSim Joint Reaction Analysis."""
        print(f"  Running Joint Reaction Analysis...")
        print(f"    SO results: {os.path.basename(so_output)}")
        print(f"    Output: {os.path.basename(jra_output)}")
        
        # In real implementation:
        # import msk_modelling_python as msk
        # msk.bops.run_jra(model_scaled, ik_output, so_output, jra_output)
        
        print(f"    [Demo mode: JRA would be executed here]")
        
        return {
            "jra_status": "completed",
            "jra_duration": 12.3,
            "peak_hip_force": 2345.6  # N
        }
    
    # Step 7: Generate Report
    def generate_report(subject_name, trial_name, report_output, 
                       ik_status, ik_duration, ik_rms_error,
                       id_status, id_duration, max_hip_moment,
                       so_status, so_duration, rms_residual,
                       jra_status, jra_duration, peak_hip_force):
        """Generate comprehensive analysis report."""
        print(f"  Generating analysis report...")
        
        report_lines = [
            "="*60,
            "OpenSim Analysis Report",
            "="*60,
            "",
            f"Subject: {subject_name}",
            f"Trial: {trial_name}",
            "",
            "Analysis Results:",
            "-"*60,
            "",
            "1. Inverse Kinematics (IK)",
            f"   Status: {ik_status}",
            f"   Duration: {ik_duration}s",
            f"   RMS Marker Error: {ik_rms_error}m",
            "",
            "2. Inverse Dynamics (ID)",
            f"   Status: {id_status}",
            f"   Duration: {id_duration}s",
            f"   Max Hip Moment: {max_hip_moment} Nm",
            "",
            "3. Static Optimization (SO)",
            f"   Status: {so_status}",
            f"   Duration: {so_duration}s",
            f"   RMS Residual: {rms_residual}",
            "",
            "4. Joint Reaction Analysis (JRA)",
            f"   Status: {jra_status}",
            f"   Duration: {jra_duration}s",
            f"   Peak Hip Force: {peak_hip_force} N",
            "",
            "="*60,
            "Analysis Complete",
            "="*60,
        ]
        
        report_text = "\n".join(report_lines)
        
        # Write report
        with open(report_output, 'w') as f:
            f.write(report_text)
        
        print(f"    Report saved: {report_output}")
        
        # Also print to console
        print("\n" + report_text)
        
        return {
            "report_status": "completed",
            "report_path": report_output
        }
    
    # Build the pipeline
    pipeline = Pipeline(
        f"OpenSim Analysis: {subject_name}/{trial_name}",
        "Complete biomechanical analysis pipeline: IK -> ID -> SO -> JRA"
    )
    
    # Create nodes
    setup_node = WorkflowNode(
        "Setup Paths",
        setup_paths,
        {
            "project_folder": project_folder,
            "subject_name": subject_name,
            "trial_name": trial_name
        },
        "Initialize file paths and output directories"
    )
    
    validate_node = WorkflowNode(
        "Validate Inputs",
        validate_inputs,
        description="Check that all required input files exist"
    )
    
    ik_node = WorkflowNode(
        "Inverse Kinematics",
        run_inverse_kinematics,
        description="Calculate joint angles from marker trajectories"
    )
    
    id_node = WorkflowNode(
        "Inverse Dynamics",
        run_inverse_dynamics,
        description="Calculate joint moments and forces"
    )
    
    so_node = WorkflowNode(
        "Static Optimization",
        run_static_optimization,
        description="Estimate muscle forces and activations"
    )
    
    jra_node = WorkflowNode(
        "Joint Reaction Analysis",
        run_joint_reaction_analysis,
        description="Calculate joint reaction forces"
    )
    
    report_node = WorkflowNode(
        "Generate Report",
        generate_report,
        description="Create comprehensive analysis summary"
    )
    
    # Add nodes to pipeline
    pipeline.add_node(setup_node, is_start=True)
    pipeline.add_node(validate_node)
    pipeline.add_node(ik_node)
    pipeline.add_node(id_node)
    pipeline.add_node(so_node)
    pipeline.add_node(jra_node)
    pipeline.add_node(report_node)
    
    # Define workflow connections
    pipeline.connect("Setup Paths", "Validate Inputs")
    pipeline.connect("Validate Inputs", "Inverse Kinematics")
    pipeline.connect("Inverse Kinematics", "Inverse Dynamics")
    pipeline.connect("Inverse Kinematics", "Static Optimization")
    pipeline.connect("Static Optimization", "Joint Reaction Analysis")
    pipeline.connect("Joint Reaction Analysis", "Generate Report")
    
    return pipeline


def batch_process_subjects(project_folder, subject_list, trial_list):
    """
    Create a batch processing pipeline for multiple subjects and trials.
    
    Args:
        project_folder: Path to project directory
        subject_list: List of subject names
        trial_list: List of trial names
        
    Returns:
        Configured Pipeline for batch processing
    """
    
    def setup_batch(project_folder, subject_list, trial_list):
        """Setup batch processing parameters."""
        print(f"  Setting up batch processing")
        print(f"    Subjects: {len(subject_list)}")
        print(f"    Trials per subject: {len(trial_list)}")
        print(f"    Total analyses: {len(subject_list) * len(trial_list)}")
        
        return {
            "total_analyses": len(subject_list) * len(trial_list),
            "completed_count": 0
        }
    
    def process_batch(project_folder, subject_list, trial_list, total_analyses):
        """Process all subjects and trials."""
        print(f"  Processing {total_analyses} analyses...")
        
        completed = 0
        for subject in subject_list:
            for trial in trial_list:
                print(f"\n  [{completed+1}/{total_analyses}] {subject} - {trial}")
                
                # In real implementation, create and execute pipeline for each:
                # pipeline = create_opensim_pipeline(project_folder, subject, trial)
                # pipeline.execute()
                
                print(f"    [Demo: Would run full pipeline here]")
                completed += 1
        
        return {"completed_count": completed}
    
    def summarize_batch(completed_count, total_analyses):
        """Create batch processing summary."""
        print(f"\n  Batch processing complete!")
        print(f"    Completed: {completed_count}/{total_analyses}")
        
        summary_file = "batch_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Batch Processing Summary\n")
            f.write(f"========================\n")
            f.write(f"Total analyses: {total_analyses}\n")
            f.write(f"Completed: {completed_count}\n")
        
        return {"summary_file": summary_file}
    
    # Create batch pipeline using helper
    tasks = [
        ("Setup Batch", setup_batch, 
         {"project_folder": project_folder, "subject_list": subject_list, "trial_list": trial_list},
         "Initialize batch processing"),
        ("Process All", process_batch, 
         {"project_folder": project_folder, "subject_list": subject_list, "trial_list": trial_list},
         "Run analysis for all subjects and trials"),
        ("Summarize", summarize_batch, {},
         "Create batch processing summary")
    ]
    
    return create_simple_pipeline("Batch Processing", tasks, 
                                 f"Process {len(subject_list)} subjects")


def main():
    """Main execution function."""
    
    print("\n" + "="*70)
    print("OpenSim Pipeline Workflow Examples")
    print("="*70)
    
    # Example 1: Single subject/trial analysis
    print("\n\nExample 1: Single Subject Analysis")
    print("-"*70)
    
    project_folder = "/tmp/opensim_project"
    subject_name = "Athlete_03"
    trial_name = "sq_90"
    
    pipeline = create_opensim_pipeline(project_folder, subject_name, trial_name)
    
    # Visualize the pipeline
    print(pipeline.visualize())
    
    # Execute the pipeline
    results = pipeline.execute()
    
    # Print summary
    print(f"\nPipeline Status: {results['status']}")
    print(f"Total Duration: {results['total_time']:.2f}s")
    
    # Example 2: Batch processing
    print("\n\n" + "="*70)
    print("Example 2: Batch Processing")
    print("-"*70)
    
    subject_list = ["Athlete_03", "Athlete_06", "Athlete_22"]
    trial_list = ["sq_70", "sq_90"]
    
    batch_pipeline = batch_process_subjects(project_folder, subject_list, trial_list)
    
    print(batch_pipeline.visualize())
    batch_results = batch_pipeline.execute()
    
    print(f"\nBatch Status: {batch_results['status']}")
    print(f"Total Duration: {batch_results['total_time']:.2f}s")
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
