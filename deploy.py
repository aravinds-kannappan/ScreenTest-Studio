import logging
import os

from truefoundry.deploy import (
    Build,
    DockerFileBuild,
    LocalSource,
    NodeSelector,
    Port,
    Resources,
    Service,
)


logging.basicConfig(level=logging.INFO)

workspace_fqn = os.environ["TRUEFOUNDRY_WORKSPACE_FQN"]
service_host = os.getenv("TRUEFOUNDRY_SERVICE_HOST", "")
port_config = {
    "port": 8000,
    "protocol": "TCP",
    "expose": True,
    "app_protocol": "http",
}
if service_host:
    port_config["host"] = service_host

service = Service(
    name="screentest-api",
    image=Build(
        build_source=LocalSource(project_root_path="./", local_build=True),
        build_spec=DockerFileBuild(
            build_context_path="./",
            dockerfile_path="./Dockerfile",
        ),
    ),
    resources=Resources(
        cpu_request=1.0,
        cpu_limit=2.0,
        memory_request=2048,
        memory_limit=4096,
        ephemeral_storage_request=1024,
        ephemeral_storage_limit=4096,
        node=NodeSelector(capacity_type="spot_fallback_on_demand"),
    ),
    env={
        "OPENAI_API_KEY": os.environ["OPENAI_API_KEY"],
        "SCREENTEST_LLM_MODEL": os.getenv("SCREENTEST_LLM_MODEL", "openai/gpt-4o-mini"),
        "CORS_ORIGINS": os.getenv("CORS_ORIGINS", "http://localhost:3000"),
    },
    ports=[Port(**port_config)],
    replicas=1.0,
)

service.deploy(workspace_fqn=workspace_fqn, wait=False)
