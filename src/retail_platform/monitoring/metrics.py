import time
from datetime import datetime

class PipelineMetrics:
    def __init__(self):
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = time.time()
        self.end_time = None
        self.status = "RUNNING"
        
        self.extraction = {'sales': 0, 'world_bank': 0}
        self.validation = {'passed': 0, 'rejected': 0}
        self.loading = {'dimensions': 0, 'sales': 0, 'economic_facts': 0}

    def end_run(self, status="SUCCESS"):
        self.end_time = time.time()
        self.status = status

    def print_summary(self):
        """Genera el reporte exacto requerido por la Fase 18"""
        duration = round(self.end_time - self.start_time, 1) if self.end_time else 0
        
        print("\n" + "="*40)
        print("Pipeline: RETAIL_PLATFORM")
        print(f"Run ID: {self.run_id}\n")
        
        print("EXTRACTION")
        print(f"Sales:              {self.extraction['sales']:,}")
        print(f"World Bank:         {self.extraction['world_bank']:,}\n")
        
        print("VALIDATION")
        print(f"Passed:             {self.validation['passed']:,}")
        print(f"Rejected:           {self.validation['rejected']:,}\n")
        
        print("LOADING")
        print(f"Dimensions:         {self.loading['dimensions']:,}")
        print(f"Sales:              {self.loading['sales']:,}")
        print(f"Economic facts:     {self.loading['economic_facts']:,}\n")
        
        print(f"Duration: {duration} sec\n")
        print(f"STATUS: {self.status}")
        print("="*40 + "\n")