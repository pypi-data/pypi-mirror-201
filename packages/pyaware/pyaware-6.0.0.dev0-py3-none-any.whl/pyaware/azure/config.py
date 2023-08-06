from dataclasses import dataclass


@dataclass
class DeviceCredentials:
    name: str
    primary_connection_string: str


def default_azure_parsers():
    return {
        "telemetry": {
            "factory": {"name": "telemetry_v1"},
            "model": {"name": "TelemetryV1"},
        },
        "telemetry_backlog": {
            "factory": {"name": "telemetry_v1"},
            "model": {"name": "TelemetryV1"},
            "batchable": True,
        },
        "commands": {
            "model": {"name": "CommandRequestV2"},
        },
        "command_response": {
            "model": {"name": "CommandResponse"},
        },
        "state": {
            "model": {"name": "State"},
            "device_message": False,
        },
    }


PARSERS = {"azure": default_azure_parsers}
