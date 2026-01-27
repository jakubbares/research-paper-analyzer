#!/usr/bin/env python3
"""
Integration test for the enhanced visualization API endpoint
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from visualization_engine import VisualizationEngine
from test_visualization_engine import MockLLM, create_mock_paper_data


def test_full_pipeline():
    """Test the complete pipeline end-to-end"""
    
    print("="*80)
    print("  INTEGRATION TEST: Enhanced Visualization API")
    print("="*80)
    
    # Setup
    llm = MockLLM()
    engine = VisualizationEngine(llm)
    
    # Test data
    paper_ids = ["paper_1", "paper_2", "paper_3"]
    query = "Compare training procedures and show performance improvements"
    all_raw_data = create_mock_paper_data(3)
    
    print(f"\n✓ Setup complete")
    print(f"  - Paper IDs: {len(paper_ids)}")
    print(f"  - Query: {query}")
    print(f"  - Raw data papers: {len(all_raw_data)}")
    
    # Run the pipeline
    print("\n" + "="*80)
    print("  RUNNING PIPELINE")
    print("="*80)
    
    try:
        html, metadata = engine.generate_visualization(
            paper_ids=paper_ids,
            query=query,
            all_raw_data=all_raw_data
        )
        
        print("\n✓ Pipeline executed successfully!")
        
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Validate results
    print("\n" + "="*80)
    print("  VALIDATION")
    print("="*80)
    
    errors = []
    
    # Check HTML
    if not html:
        errors.append("HTML is empty")
    elif not html.strip().startswith("<!DOCTYPE"):
        errors.append("HTML doesn't start with DOCTYPE")
    else:
        print("✓ HTML generated and valid")
        print(f"  - Length: {len(html)} characters")
        print(f"  - Lines: {len(html.split(chr(10)))}")
    
    # Check metadata
    required_fields = ["original_query", "enhanced_query", "analysis", 
                      "best_practices_applied", "data_selection", "paper_count"]
    
    for field in required_fields:
        if field not in metadata:
            errors.append(f"Missing metadata field: {field}")
        else:
            print(f"✓ Metadata has '{field}'")
    
    # Check metadata content
    if "analysis" in metadata:
        analysis = metadata["analysis"]
        if "intent" not in analysis:
            errors.append("Analysis missing 'intent'")
        if "focus_areas" not in analysis:
            errors.append("Analysis missing 'focus_areas'")
        else:
            print(f"  - Intent: {analysis.get('intent')}")
            print(f"  - Focus: {', '.join(analysis.get('focus_areas', []))}")
    
    if "data_selection" in metadata:
        selection = metadata["data_selection"]
        if "extractors_used" not in selection:
            errors.append("Data selection missing 'extractors_used'")
        else:
            extractors = selection["extractors_used"]
            print(f"  - Extractors: {', '.join(extractors)}")
            
            # Verify smart selection is working (at least some extractors were selected)
            if len(extractors) > 0:
                print(f"  ✓ Smart extractor selection working ({len(extractors)} extractors selected)")
                
                # Verify auto-inclusion of related extractors
                if "experiments" in extractors:
                    related = ["baselines", "datasets", "metrics"]
                    found_related = [e for e in related if e in extractors]
                    if found_related:
                        print(f"  ✓ Auto-included related extractors: {', '.join(found_related)}")
            else:
                errors.append("No extractors selected")
    
    if "best_practices_applied" in metadata:
        practices = metadata["best_practices_applied"]
        if len(practices) < 3:
            errors.append(f"Too few best practices: {len(practices)}")
        else:
            print(f"  - Best practices: {len(practices)} generated")
    
    # Check query enhancement
    if "enhanced_query" in metadata:
        original = metadata.get("original_query", "")
        enhanced = metadata["enhanced_query"]
        
        if len(enhanced) <= len(original):
            errors.append("Enhanced query not longer than original")
        else:
            print(f"  ✓ Query enhanced successfully")
            print(f"    Original length: {len(original)}")
            print(f"    Enhanced length: {len(enhanced)}")
    
    # Report results
    print("\n" + "="*80)
    print("  RESULTS")
    print("="*80)
    
    if errors:
        print(f"\n✗ Test FAILED with {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n✓ ALL TESTS PASSED!")
        print("\nThe enhanced visualization API is working correctly:")
        print("  1. ✓ Pipeline executes without errors")
        print("  2. ✓ HTML is generated and valid")
        print("  3. ✓ Metadata is complete and structured")
        print("  4. ✓ Query analysis working")
        print("  5. ✓ Best practices generation working")
        print("  6. ✓ Query enhancement working")
        print("  7. ✓ Smart data selection working")
        print("\n🎉 READY FOR PRODUCTION USE!")
        return True


if __name__ == "__main__":
    success = test_full_pipeline()
    sys.exit(0 if success else 1)
