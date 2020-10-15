# pre-commit-hooks

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```
  - repo: https://github.com/lowess/pre-commit-hooks
    rev: <GIT_TAG>  # Get the latest from: https://github.com/lowess/pre-commit-hooks/releases
    hooks:
      - id: prepare-commit-msg
```

### Common Hooks available

#### `prepare-commit-msg`
Prepend the branch name to the commit message. If you're using a JIRA project identifier prefix like `{PROJECT_KEY}-{ISSUE_NO}` in your branch name, it will be detected and used instead.

Example configuration:
```
  - repo: https://github.com/Lowess/pre-commit-hooks
    rev: v1.2.0 # Get the latest from: https://github.com/lowess/pre-commit-hooks/releases
    hooks:
      - id: prepare-commit-message
        args: ["--format", "jira", "--jira-projects", "TI,MLE"]
        stages: [commit-msg]
```

#### `jinja2-render-template`
Render a [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) template using [Yasha](https://github.com/kblomqvist/yasha)

Example configuration:
```
  - repo: https://github.com/Lowess/pre-commit-hooks
    rev: v1.2.0
    hooks:
      - id: jinja2-render-template
        args: ["template.j2", "--output", "myfile.yaml"]
```

---

### DevOps Hooks available

#### `ansible-molecule-lint`
Run [Molecule](https://molecule.readthedocs.io/en/latest/) lint on the current [Ansible](https://www.ansible.com/) role

#### `ansible-molecule-syntax`
Run [Molecule](https://molecule.readthedocs.io/en/latest/) syntax check on the current [Ansible](https://www.ansible.com/) role

#### `terraform-fmt`

Run [Terraform](https://www.terraform.io/) `fmt` command on `*.tf` files

Example configuration:
```
  - repo: https://github.com/lowess/pre-commit-hooks
    rev: v1.2.0 # Get the latest from: https://github.com/lowess/pre-commit-hooks/releases
    hooks:
      - id: terraform-fmt
```

#### `terragrunt-hclfmt`

Run [Terragrunt](https://terragrunt.gruntwork.io/) `hclfmt` command on `*.hcl` files

Example configuration:
```
  - repo: https://github.com/lowess/pre-commit-hooks
    rev: v1.2.0 # Get the latest from: https://github.com/lowess/pre-commit-hooks/releases
    hooks:
      - id: terragrunt-hclfmt
```
