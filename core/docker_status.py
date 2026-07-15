import subprocess


class DockerStatus:

    CONTAINERS = [
        "jellyfin",
        "sonarr",
        "radarr",
        "prowlarr",
        "bazarr",
        "qbittorrent",
        "jellyseerr",
    ]

    def get_status(self):

        status = {}

        for container in self.CONTAINERS:

            try:

                result = subprocess.run(
                    [
                        "docker",
                        "inspect",
                        "-f",
                        "{{.State.Running}}",
                        container,
                    ],
                    capture_output=True,
                    text=True,
                )

                running = result.stdout.strip() == "true"

                status[container] = running

            except Exception:

                status[container] = False

        return status