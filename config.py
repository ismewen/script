container_name_template_config = {
    "wordpress": {
        "agent_name": "wordpress-agent",
        "app_name": "wordpress",
        "pod_name": "{}-cms-0",
        "sts_name": "{}-cms"
    },
    "opencart": {
        "agent_name": "opencart-agent",
        "app_name": "opencart",
        "pod_name": "{}-cms-0",
        "sts_name": "{}-cms"
    },
    "drupal": {
        "agent_name": "drupal-agent",
        "app_name": "drupal",
        "pod_name": "{}-cms-0",
        "sts_name": "{}-cms"
    },
    "magento": {
        "agent_name": "magento-agent",
        "app_name": "magento",
        "pod_name": "{}-cms-0",
        "sts_name": "{}-cms"
    },
    "postgresql": {
        "agent_name": "postgresql-agent",
        "app_name":  "postgresql",
        "pod_name": "{}-db-0",
        "sts_name": "{}-db"
    },
    "mysql": {
        "agent_name": "mysql-agent",
        "app_name": "mysql",
        "pod_name": "{}-db-0",
        "sts_name": "{}-db"
    },
    "mariadb": {
        "agent_name": "mariadb-agent",
        "app_name": "mariadb",
        "pod_name": "{}-db-0",
        "sts_name": "{}-db"
    },
    "cockroachdb": {
        "agent_name": "cockroach-agent",
        "app_name": "cockroachdb",
        "pod_name": "{}-cockroach-p-0",
        "sts_name": "{}-cockroach-p",
    }
}