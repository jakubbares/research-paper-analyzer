"""
Aggregation Engine - Cross-paper analysis and insights
"""
from typing import List, Dict, Any
from collections import defaultdict
from pathlib import Path
import json


class AggregationEngine:
    """Aggregate and analyze data across multiple papers"""
    
    def __init__(self, extracted_dir: Path):
        self.extracted_dir = extracted_dir
    
    def aggregate_contributions(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Aggregate contributions across multiple papers"""
        all_contributions = []
        
        for paper_id in paper_ids:
            contrib_file = self.extracted_dir / f"{paper_id}_contributions.json"
            if contrib_file.exists():
                with open(contrib_file, 'r') as f:
                    contributions = json.load(f)
                    for contrib in contributions:
                        contrib['paper_id'] = paper_id
                        all_contributions.append(contrib)
        
        # Count by type
        by_type = defaultdict(list)
        for contrib in all_contributions:
            by_type[contrib['contribution_type']].append(contrib)
        
        # Get most common types
        type_counts = {k: len(v) for k, v in by_type.items()}
        most_common = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_papers": len(paper_ids),
            "total_contributions": len(all_contributions),
            "by_type": type_counts,
            "most_common": [{"type": t, "count": c} for t, c in most_common],
            "contributions": all_contributions
        }
    
    def aggregate_experiments(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Aggregate experiments across multiple papers"""
        all_experiments = []
        all_datasets = defaultdict(int)
        all_tasks = defaultdict(int)
        
        for paper_id in paper_ids:
            exp_file = self.extracted_dir / f"{paper_id}_experiments.json"
            if exp_file.exists():
                with open(exp_file, 'r') as f:
                    experiments = json.load(f)
                    for exp in experiments:
                        exp['paper_id'] = paper_id
                        all_experiments.append(exp)
                        
                        # Count datasets
                        for dataset in exp.get('datasets', []):
                            if isinstance(dataset, dict):
                                all_datasets[dataset.get('name', 'Unknown')] += 1
                        
                        # Count tasks
                        task = exp.get('task', 'Unknown')
                        all_tasks[task] += 1
        
        # Get most common datasets and tasks
        common_datasets = sorted(all_datasets.items(), key=lambda x: x[1], reverse=True)[:10]
        common_tasks = sorted(all_tasks.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_papers": len(paper_ids),
            "total_experiments": len(all_experiments),
            "common_datasets": [{"name": d, "count": c} for d, c in common_datasets],
            "common_tasks": [{"name": t, "count": c} for t, c in common_tasks],
            "experiments": all_experiments
        }
    
    def find_patterns(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Detect patterns across papers"""
        contributions = self.aggregate_contributions(paper_ids)
        experiments = self.aggregate_experiments(paper_ids)
        
        patterns = []
        
        # Pattern: Popular contribution types
        if contributions['most_common']:
            top_type = contributions['most_common'][0]
            patterns.append({
                "type": "contribution_trend",
                "title": f"Most Common Contribution Type",
                "description": f"{top_type['type']} appears in {top_type['count']} papers",
                "confidence": "high"
            })
        
        # Pattern: Popular datasets
        if experiments['common_datasets']:
            top_dataset = experiments['common_datasets'][0]
            patterns.append({
                "type": "dataset_trend",
                "title": f"Most Used Dataset",
                "description": f"{top_dataset['name']} used in {top_dataset['count']} papers",
                "confidence": "high"
            })
        
        # Pattern: Task distribution
        if experiments['common_tasks']:
            top_task = experiments['common_tasks'][0]
            patterns.append({
                "type": "task_trend",
                "title": f"Most Common Task",
                "description": f"{top_task['name']} in {top_task['count']} papers",
                "confidence": "high"
            })
        
        return {
            "total_patterns": len(patterns),
            "patterns": patterns
        }
    
    def find_gaps(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Identify research gaps"""
        contributions = self.aggregate_contributions(paper_ids)
        experiments = self.aggregate_experiments(paper_ids)
        
        gaps = []
        
        # Gap: Underexplored contribution types
        all_possible_types = [
            "Novel Architecture", "Novel Loss Function", "Training Procedure",
            "Data Augmentation", "Evaluation Metric", "Theoretical Framework",
            "Novel Algorithm", "Sampling Procedure"
        ]
        
        explored_types = set(contributions['by_type'].keys())
        unexplored = [t for t in all_possible_types if t not in explored_types]
        
        if unexplored:
            gaps.append({
                "type": "unexplored_contribution",
                "title": "Unexplored Contribution Types",
                "description": f"Types not seen: {', '.join(unexplored[:3])}",
                "opportunity": "high"
            })
        
        # Gap: Dataset combinations
        datasets = [d['name'] for d in experiments['common_datasets']]
        if len(datasets) >= 2:
            gaps.append({
                "type": "dataset_combination",
                "title": "Cross-Dataset Evaluation",
                "description": f"Try combining {datasets[0]} with {datasets[1]}",
                "opportunity": "medium"
            })
        
        return {
            "total_gaps": len(gaps),
            "gaps": gaps
        }

