from pathlib import Path
import shutil
from .suite import Benchmark


class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def run(self, input_bc: Path, output_bc: Path, bench: Benchmark):
      shutil.copy(input_bc, output_bc)
      dir = output_bc.parent
      for i, stage in enumerate(self.stages):
          stage(output_bc)

    def create_jobs(self, input_bc: Path, output_bc: Path, bench: Benchmark):
        shutil.copy(input_bc, output_bc)

        jobs = []
        for i, stage in enumerate(self.stages):
            jobs.append((f'{self.name} stage {i+1}', stage, output_bc))
        return jobs
