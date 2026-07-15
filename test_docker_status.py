from core.docker_status import DockerStatus

status = DockerStatus().get_status()

for name, running in status.items():

    print(
        f"{name:15}",
        "🟢 Running" if running else "🔴 Stopped"
    )