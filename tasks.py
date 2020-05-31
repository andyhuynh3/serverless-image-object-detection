from invoke import task


@task
def tf_init(c, env="dev"):
    backend_config_path = f"config/backend-{env}.conf"
    c.run(
        "cd terraform && "
        f"terraform init -input=false -backend-config={backend_config_path}"
    )


@task
def tf_plan(c, env="dev"):
    var_path = f"config/{env}.tfvars"
    c.run(
        f"cd terraform && terraform plan -out=tfplan -input=false -var-file={var_path}"
    )


@task
def tf_apply(c, env="dev"):
    c.run("cd terraform && terraform apply -input=false tfplan")


@task
def tf_destroy(c, env="dev"):
    var_path = f"config/{env}.tfvars"
    c.run(f"cd terraform && terraform destroy -var-file={var_path} -auto-approve")


@task(tf_init, tf_plan, tf_apply)
def deploy(c, env="dev"):
    pass


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
