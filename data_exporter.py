#!/usr/bin/env python3
"""
Data export utilities for the Cosmic Data Observatory
Exports generated data to JSON, CSV, and Python formats for testing
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Union
from data_generator import SpaceStationGenerator, AlienContactGenerator, CrewMissionGenerator, DataConfig


class DataExporter:
    """Handles data export in multiple formats"""
    
    def __init__(self, output_dir: str = "generated_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_to_json(self, data: List[Dict[str, Any]], filename: str) -> Path:
        """Export data to JSON format"""
        filepath = self.output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def export_to_csv(self, data: List[Dict[str, Any]], filename: str) -> Path:
        """Export flat data to CSV format"""
        if not data:
            return None
        
        filepath = self.output_d