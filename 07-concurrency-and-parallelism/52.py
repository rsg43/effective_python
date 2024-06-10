import subprocess
import time
import os
from typing import IO


result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    encoding="utf-8",
)

result.check_returncode()
print(result.stdout)

proc = subprocess.Popen(
    ["sleep", "1"],
)

while proc.poll() is None:
    print("Working...")
    time.sleep(0.2)

start = time.time()
procs = [subprocess.Popen(["sleep", "1"]) for _ in range(10)]
for proc in procs:
    proc.communicate()
end = time.time()
print(f"Finished in {end - start:.3f} seconds")


def encrypt(data: bytes) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["data"] = data  # type: ignore[assignment]
    proc = subprocess.Popen(
        ["openssl", "enc", "-pbkdf2", "-pass", "env:data"],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    if proc.stdin is None:
        raise RuntimeError("stdin is None")
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc


print(encrypt(b"Hello, World!").communicate()[0])


def hash(input_stdin: IO[bytes]) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        ["openssl", "dgst", "-whirlpool", "-binary"],
        stdin=input_stdin,
        stdout=subprocess.PIPE,
    )


en_procs: list[subprocess.Popen[bytes]] = []
hs_procs: list[subprocess.Popen[bytes]] = []
for _ in range(3):
    data = os.urandom(10)
    en_proc = encrypt(data)
    if en_proc.stdout is None:
        raise RuntimeError("stdout is None")

    en_procs.append(en_proc)
    hs_procs.append(hash(en_proc.stdout))

    en_proc.stdout.close()
    en_proc.stdout = None

for en_proc, hs_proc in zip(en_procs, hs_procs):
    try:
        en_proc.communicate(timeout=0.0001)
    except subprocess.TimeoutExpired:
        en_proc.terminate()
        en_proc.wait()

    try:
        out_bytes, __ = hs_proc.communicate(timeout=0.0001)
    except subprocess.TimeoutExpired:
        hs_proc.terminate()
        hs_proc.wait()
        out_bytes = b"<timeout>"
    print(out_bytes)
