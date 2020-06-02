from invoke import task


def _get_tf_init_cmd(env):
    backend_config_path = f"config/backend-{env}.conf"
    cmd = (
        "cd terraform && "
        f"terraform init -input=false -backend-config={backend_config_path}"
    )
    return cmd


def _get_tf_plan_cmd(env):
    var_path = f"config/{env}.tfvars"
    cmd = (
        f"cd terraform && terraform plan -out=tfplan -input=false -var-file={var_path}"
    )
    return cmd


def _get_tf_destroy_cmd(env):
    var_path = f"config/{env}.tfvars"
    cmd = f"cd terraform && terraform destroy -var-file={var_path} -auto-approve"
    return cmd


def _get_tf_apply_cmd():
    return "cd terraform && terraform apply -input=false tfplan"


@task
def tf_init(c, env="dev"):
    c.run(_get_tf_init_cmd(env))


@task
def tf_plan(c, env="dev"):
    c.run(_get_tf_plan_cmd(env))


@task
def tf_apply(c):
    c.run(_get_tf_apply_cmd())


@task
def tf_destroy(c, env="dev"):
    c.run(_get_tf_destroy_cmd(env))


@task()
def deploy(c, env="dev"):
    c.run(_get_tf_init_cmd(env))
    c.run(_get_tf_plan_cmd(env))
    c.run(_get_tf_apply_cmd())


@task
def flake8(c):
    c.run("flake8 .")


@task
def black(c):
    c.run("black .")


@task
def mypy(c):
    c.run("mypy .")


@task
def install_deps(c, env="dev"):
    requirements_file = "requirements.txt"
    if env == "dev":
        requirements_file = f"dev-{requirements_file}"
    c.run(f"pip install -r {requirements_file}")
