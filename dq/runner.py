from dq.models import RunReport

class PipelineHaltError(Exception):
    pass

def apply_policy(report: RunReport, fail_fast: bool = False, fail_on_warning: bool = False):
    """
    Applies severity policy.
    - Any ERROR halts the pipeline.
    - If fail_on_warning is True, WARNING also halts the pipeline.
    """
    halt = False
    
    if report.errors > 0:
        halt = True
        
    if fail_on_warning and report.warnings > 0:
        halt = True
        
    if halt:
        raise PipelineHaltError("Pipeline halted due to DQ failures.")
