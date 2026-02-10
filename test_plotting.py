#!/usr/bin/env python3
"""
Test script to verify plotting functions work correctly with test data.
This allows testing the plotting functionality without running the full simulation.
"""

import numpy as np
import os
import tempfile
import shutil

def create_test_data():
    """Create test data files to simulate AMSS-NCKU output"""

    # Create temporary directory for test data
    test_dir = tempfile.mkdtemp(prefix="amss_test_")

    # Create binary_output directory
    binary_dir = os.path.join(test_dir, "binary_output")
    os.makedirs(binary_dir)

    # Create figure directory
    figure_dir = os.path.join(test_dir, "figure")
    os.makedirs(figure_dir)

    # Create test bssn_BH.dat file (single timestep)
    bh_file = os.path.join(binary_dir, "bssn_BH.dat")
    with open(bh_file, 'w') as f:
        f.write("# File created on Test\n")
        f.write("# time\n")
        f.write("0              0               4.4615385       0               0               -5.5384615      0\n")

    # Create test bssn_ADMQs.dat file
    adm_file = os.path.join(binary_dir, "bssn_ADMQs.dat")
    with open(adm_file, 'w') as f:
        f.write("# Test ADM data\n")
        f.write("0 65.000000 0.000000 0.000000 0.000000 0.000000 0.000000 0.000000\n")

    # Create test bssn_constraint.dat file
    constraint_file = os.path.join(binary_dir, "bssn_constraint.dat")
    with open(constraint_file, 'w') as f:
        f.write("# Test constraint data\n")
        f.write("0 0.000001 0.000000 0.000000 0.000000 0.000000 0.000000 0.000000\n")

    # Create test bssn_psi4.dat file
    psi4_file = os.path.join(binary_dir, "bssn_psi4.dat")
    with open(psi4_file, 'w') as f:
        f.write("# Test psi4 data\n")
        for i in range(12):  # 12 detectors
            f.write("0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n")

    return test_dir, binary_dir, figure_dir

def test_plotting():
    """Test the plotting functions with test data"""

    print("Creating test data...")
    test_dir, binary_dir, figure_dir = create_test_data()

    try:
        # Import required modules
        import plot_xiaoqu
        import AMSS_NCKU_Input as input_data

        print("Testing BH trajectory plotting...")
        plot_xiaoqu.generate_puncture_orbit_plot(binary_dir, figure_dir)
        print("✓ BH trajectory plot test passed")

        print("Testing BH distance plotting...")
        plot_xiaoqu.generate_puncture_distence_plot(binary_dir, figure_dir)
        print("✓ BH distance plot test passed")

        print("Testing 3D trajectory plotting...")
        plot_xiaoqu.generate_puncture_orbit_plot3D(binary_dir, figure_dir)
        print("✓ 3D trajectory plot test passed")

        print("Testing ADM plotting...")
        for i in range(input_data.Detector_Number):
            plot_xiaoqu.generate_ADMmass_plot(binary_dir, figure_dir, i)
        print("✓ ADM plot test passed")

        print("Testing constraint plotting...")
        for i in range(input_data.grid_level):
            plot_xiaoqu.generate_constraint_check_plot(binary_dir, figure_dir, i)
        print("✓ Constraint plot test passed")

        print("Testing GW plotting...")
        for i in range(input_data.Detector_Number):
            plot_xiaoqu.generate_gravitational_wave_psi4_plot(binary_dir, figure_dir, i)
        print("✓ GW plot test passed")

        # Check if PDF files were created
        pdf_files = []
        for root, dirs, files in os.walk(figure_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))

        print(f"\nGenerated {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"  - {os.path.basename(pdf)}")

        if len(pdf_files) >= 3:  # At least the 3 required PDFs
            print("\n✅ All plotting tests passed! The fixes work correctly.")
            return True
        else:
            print(f"\n❌ Only {len(pdf_files)} PDF files generated, expected at least 3.")
            return False

    except Exception as e:
        print(f"\n❌ Error during plotting test: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Clean up
        shutil.rmtree(test_dir)

if __name__ == "__main__":
    success = test_plotting()
    exit(0 if success else 1)
