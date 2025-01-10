def validate_department_name(name: str) -> bool:
    return isinstance(name, str) and len(name) > 0

def validate_job_name(name: str) -> bool:
    return isinstance(name, str) and len(name) > 0
