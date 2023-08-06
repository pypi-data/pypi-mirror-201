# YAML based Windows setup files with schema validation

As as example, consider this [README for a windows scoop-based setup](out.md).

This was produced entirely using this module's CLI from the [YAML setup file](tests/setup.yml).

The command you need is

```shell

yamlup render /path/to/setup.yml -o /path/to/README.md
```

This module doesn't have any other aims besides setup schema validation and formatting its contents.