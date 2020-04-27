# pre-commit-hooks

Some hooks for pre-commit.

See also: https://github.com/pre-commit/pre-commit

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/lowess/pre-commit-hooks
        rev: v1.0.0  # Use the ref you want to point at
        hooks:
        -   id: prepare-commit-msg

### Common Hooks available

#### `prepare-commit-msg`
Prepend the branch name to the commit message. If you're using a JIRA project identifier prefix like `{PROJECT_KEY}-{ISSUE_NO}` in your branch name, it will be detected and used instead.

Example configuration:
```
  - hooks:
      - id: prepare-commit-message
        args: ["--format", "jira", "--jira-projects", "TI,MLE"]
        stages: [commit-msg]
    repo: https://github.com/Lowess/pre-commit-hooks
    rev: v1.0.0
```

### DevOps Hooks available

#### `ansible-molecule-lint`
Run [molecule](https://molecule.readthedocs.io/en/latest/) lint on the current [Ansible](https://www.ansible.com/) role

#### `ansible-molecule-syntax`
Run [molecule](https://molecule.readthedocs.io/en/latest/) syntax check on the current [Ansible](https://www.ansible.com/) role
