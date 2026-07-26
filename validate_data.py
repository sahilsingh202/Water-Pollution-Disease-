"""
Data Validation Script for Water Pollution & Disease Dataset
Validates dataset structure, types, and quality before running the app
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Required columns
REQUIRED_COLUMNS = [
    'Contaminant_Level',
    'pH_Level',
    'Dissolved_Oxygen',
    'Population_Density',
    'Diarrhea_Cases'
]

def validate_dataset(filepath='water_pollution_disease.csv'):
    """
    Comprehensive dataset validation
    
    Args:
        filepath: Path to CSV file
    
    Returns:
        tuple: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    print("\n" + "="*60)
    print("📊 Water Pollution Dataset Validation")
    print("="*60 + "\n")
    
    # Check file exists
    print(f"Checking file: {filepath}")
    if not Path(filepath).exists():
        errors.append(f"❌ File not found: {filepath}")
        return False, errors, warnings
    
    print("✓ File found\n")
    
    # Load dataset
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Dataset loaded successfully")
        print(f"  - Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
    except Exception as e:
        errors.append(f"❌ Error loading CSV: {str(e)}")
        return False, errors, warnings
    
    # Check columns
    print("Checking columns...")
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    extra_cols = [col for col in df.columns if col not in REQUIRED_COLUMNS]
    
    if missing_cols:
        errors.append(f"❌ Missing columns: {missing_cols}")
    else:
        print(f"✓ All required columns present")
    
    if extra_cols:
        warnings.append(f"⚠ Extra columns found: {extra_cols}")
    
    print()
    
    # Check data types
    print("Checking data types...")
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            dtype = df[col].dtype
            if dtype in ['float64', 'int64', 'float32', 'int32']:
                print(f"✓ {col}: {dtype}")
            else:
                errors.append(f"❌ {col} has invalid type: {dtype}")
    
    print()
    
    # Check missing values
    print("Checking missing values...")
    missing = df[REQUIRED_COLUMNS].isnull().sum()
    has_missing = missing[missing > 0]
    
    if len(has_missing) > 0:
        for col, count in has_missing.items():
            warnings.append(f"⚠ {col} has {count} missing values ({count/len(df)*100:.1f}%)")
    else:
        print("✓ No missing values found")
    
    print()
    
    # Check duplicates
    print("Checking duplicates...")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        warnings.append(f"⚠ Found {duplicates} duplicate rows ({duplicates/len(df)*100:.1f}%)")
    else:
        print("✓ No duplicate rows")
    
    print()
    
    # Check for outliers
    print("Checking for outliers...")
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            
            if outliers > 0:
                pct = outliers / len(df) * 100
                if pct > 10:
                    warnings.append(f"⚠ {col} has {outliers} outliers ({pct:.1f}%)")
                else:
                    print(f"  - {col}: {outliers} outliers ({pct:.1f}%)")
    
    print("✓ Outlier check complete\n")
    
    # Statistical summary
    print("Statistical Summary:")
    print("-" * 60)
    summary = df[REQUIRED_COLUMNS].describe()
    print(summary.to_string())
    
    print("\n" + "-" * 60)
    print("\nData Quality Metrics:")
    print(f"  - Total records: {len(df)}")
    print(f"  - Complete records: {len(df) - df[REQUIRED_COLUMNS].isnull().any(axis=1).sum()}")
    print(f"  - Data completeness: {(1 - df[REQUIRED_COLUMNS].isnull().sum().sum() / (len(df) * len(REQUIRED_COLUMNS))) * 100:.1f}%")
    
    print("\n" + "="*60)
    
    # Summary
    if errors:
        print("❌ VALIDATION FAILED")
        print("\nErrors found:")
        for error in errors:
            print(f"  {error}")
        return False, errors, warnings
    
    if warnings:
        print("⚠️  VALIDATION PASSED (with warnings)")
        print("\nWarnings:")
        for warning in warnings:
            print(f"  {warning}")
        print("\n✅ Dataset is usable but review warnings")
        return True, errors, warnings
    
    print("✅ VALIDATION PASSED")
    print("\n✨ Dataset is ready to use!")
    print("="*60 + "\n")
    return True, errors, warnings

def auto_fix_dataset(filepath='water_pollution_disease.csv', output_path=None):
    """
    Attempt to automatically fix common issues
    
    Args:
        filepath: Path to CSV file
        output_path: Where to save fixed file
    """
    print("\n🔧 Attempting automatic fixes...\n")
    
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        print(f"❌ Cannot load dataset: {e}")
        return None
    
    changes = []
    
    # Rename columns if close match
    col_mapping = {}
    for required_col in REQUIRED_COLUMNS:
        if required_col not in df.columns:
            # Try to find similar column
            for actual_col in df.columns:
                if required_col.lower() in actual_col.lower() or actual_col.lower() in required_col.lower():
                    col_mapping[actual_col] = required_col
                    changes.append(f"✓ Renamed '{actual_col}' → '{required_col}'")
                    break
    
    if col_mapping:
        df = df.rename(columns=col_mapping)
    
    # Drop rows with missing values in required columns
    initial_len = len(df)
    df = df.dropna(subset=REQUIRED_COLUMNS)
    if len(df) < initial_len:
        changes.append(f"✓ Dropped {initial_len - len(df)} rows with missing values")
    
    # Remove duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_len:
        changes.append(f"✓ Removed {initial_len - len(df)} duplicate rows")
    
    # Keep only required columns
    df = df[REQUIRED_COLUMNS]
    
    # Save if output path specified
    if output_path:
        df.to_csv(output_path, index=False)
        changes.append(f"✓ Saved cleaned dataset to {output_path}")
    else:
        df.to_csv(filepath, index=False)
        changes.append(f"✓ Saved cleaned dataset to {filepath}")
    
    if changes:
        print("Changes made:")
        for change in changes:
            print(f"  {change}")
        print(f"\n✅ Dataset fixed! Now contains {len(df)} records")
    else:
        print("✅ No fixes needed - dataset is clean")
    
    return df

if __name__ == "__main__":
    """
    Run validation from command line
    
    Usage:
        python validate_data.py                    # Validate default file
        python validate_data.py path/to/file.csv   # Validate specific file
        python validate_data.py --fix              # Auto-fix issues
    """
    
    filepath = 'water_pollution_disease.csv'
    auto_fix = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--fix':
            auto_fix = True
        else:
            filepath = sys.argv[1]
    
    if auto_fix:
        auto_fix_dataset(filepath)
    
    is_valid, errors, warnings = validate_dataset(filepath)
    
    sys.exit(0 if is_valid else 1)
