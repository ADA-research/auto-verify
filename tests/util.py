import subprocess


def run_av_cli(args: list[str]) -> str:
    base_cmd = ["auto-verify"]
    base_cmd.extend(args)

    result = subprocess.run(base_cmd, stdout=subprocess.PIPE)
    return str(result.stdout)
