# basecfg

This is a Python class for specifying the configuration that an application can take using type-annotated class attributes. Once a config class is created it populates its config from an optional JSON file (such as a Kubernetes configmap), environment variables, and command-line arguments (all automatically).
