
from pathlib import Path


class Runner:
    pass


class ShellRunner(Runner):
    pass


class TimeRunner(Runner):
    pass


class CondorRunner(Runner):
    pass


class Suite:
    """
    A suite is a standard benchmark suite, which contains multiple Benchmark instances.
    The main functionality of a Suite is to fetch the contents of a benchmark, initialize
    the benchmark with patches or configuration, and to expose each benchmark as a
    `waterline.Benchmark` that can be put through the benchmarking pipeline defined by the
    user. A suite also defines how a benchmark is converted from bitcode to an executable.
    """

    name = 'unknown'

    def __init__(self, workspace):
        """
        Initialize the benchmark suite with a context and a name
        """
        self.workspace = workspace
        self.benchmarks: list[Benchmark] = []

        self.src = self.workspace.src_dir / self.name
        self.bin = self.workspace.bin_dir / self.name
        self.ir = self.workspace.ir_dir / self.name

    def configure(self, *args, **kwargs):
        """
        Called by the Workspace to initialize this benchmark suite with 
        """
        pass

    def acquire(self):
        """
        Download, clone, or otherwise acquire the benchmark suite into a certain path.
        This function also emits 
        """
        print(f'acquire suite {self.name} to {self.src}')

    def add_benchmark(self, benchmark, name: str, *args):
        self.benchmarks.append(benchmark(self, name, *args))

    def get_compile_jobs(self):
        """
        Compile each of the benchmarks in the suite. By default this 
        simply defers to each benchmark, but it could do it some other
        way if the suite has a goofy build system.
        """

        jobs = []
        for benchmark in self.benchmarks:
            bench_bin_dir = self.bin / benchmark.name
            bench_bin_dir.mkdir(exist_ok=True)

            bin_file = bench_bin_dir / 'a.out'
            if not bin_file.exists():
                jobs.append((f'compile {self.name}/{benchmark.name}', benchmark.compile, bin_file))
        return jobs

class Benchmark:
    def __init__(self, suite: Suite, name: str):
        self.suite = suite
        self.name = name

    def compile(self, output: Path):
        """
        Compile this benchmark to a certain output file
        """
        pass

    def link(self, bitcode: Path, destination: Path):
        """
        Link a bitcode file of this benchmark into a complete executable.
        """
        print(f'link {bitcode} to {destination} not implemented')

    def shell(self, *args):
        self.suite.workspace.shell(*args)
