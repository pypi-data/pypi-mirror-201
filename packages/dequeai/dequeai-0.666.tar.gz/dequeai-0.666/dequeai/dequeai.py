from dequeai.dequeai_run import Run

run = Run()



def init( user_name, project_name=None, api_key=None):
    run.init(user_name, project_name, api_key)

def finish():
    run.finish()

def log( data, step=None, commit=True):
    run.log(data, step, commit)

def log_artifact(artifact_type, path):
    run.log_artifact(artifact_type, path)


def register_artifacts(latest=True, label=None, tags=None):
    run.register_artifacts(latest, label, tags)