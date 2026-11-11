# Docker containers

Read this for writing or reviewing a Dockerfile or a Compose file, making an image smaller, faster
to build or safer to run, running containers without root or extra privileges, pushing, signing
and scanning images, rootless Docker and Podman, and finding out why a container won't start or
stay healthy.

The host under the daemon, its packages, disks and journal, is `linux`; firewalls and
segmentation beyond a published port are `networking-security`. An entrypoint script follows
`coding`'s `bash-coding` and `bash-security`. Building and deploying from CI is `git-workflows`'
`ci-workflows` and `ci-cd`. The standard rules on where secrets live (dimension 7) and on keeping
dependencies current (dimension 8); this module covers how an image and a container honor them.

## Rules

1. **Pin every base image by digest, and let a bot move the pin** (fact `docker-pin-digest`).
2. **Build in stages and ship only the last,** on a small base: `-slim`, distroless or a
   hardened image.
3. **Keep secrets out of every layer:** a BuildKit secret mount at build time
   (fact `docker-build-secrets`) and a secret file at run time, never `ARG` or `ENV`.
4. **Run as a non-root user, on a read-only root filesystem, with every capability dropped and
   memory and process limits set** (fact `docker-no-limits`).
5. **Never use `--privileged`, and never mount the Docker socket into a container**
   (facts `docker-privileged`, `docker-daemon-trust`).
6. **Publish a port on `127.0.0.1` unless other hosts should reach it**
   (facts `docker-publish-default`, `docker-ufw`).
7. **Write Compose to the current specification:** `compose.yaml`, no `version:` key
   (fact `docker-compose-version`), health-gated `depends_on` (fact `docker-depends-healthy`),
   named volumes for data and an internal network for back ends.
8. **Deploy by digest, verify a signature before trusting an image, and scan it again on a
   schedule** (facts `docker-engine-29`, `docker-cosign-verify`).
9. **Debug from the outside in:** `ps`, `logs` and `inspect` change nothing; `exec` comes last.

### Dockerfiles

- A `.dockerignore` keeps `.git`, `.env`, virtual environments and build output out of the build.
- Order layers from least to most often changed: the dependency manifest and its install, then
  the source. A cache mount keeps the package cache out of the image.
- One process per container. Exec-form `CMD` makes it PID 1, so it gets `SIGTERM`; add `--init`
  (Compose `init: true`) when it starts children it doesn't reap.
- A `HEALTHCHECK` lets Compose and `docker ps` see "running but stuck". Lint with hadolint.

`docker buildx imagetools inspect python:3.14-slim` prints the `<digest>`. Build with
`docker build --secret id=netrc,src="$HOME/.netrc" .`

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.14-slim@sha256:<digest> AS build
WORKDIR /src
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=secret,id=netrc,target=/root/.netrc \
    pip install -r requirements.txt
COPY app/ app/

FROM python:3.14-slim@sha256:<digest>
RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /srv
COPY --from=build /venv /venv
COPY --from=build /src/app app/
ENV PATH="/venv/bin:$PATH"
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD ["python", "-c", "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"]
CMD ["python", "-m", "app"]
```

### Compose

```yaml
services:
  web:
    build: .
    ports: ["127.0.0.1:8000:8000"]
    read_only: true
    tmpfs: [/tmp]
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    mem_limit: 512m
    pids_limit: 200
    depends_on:
      db:
        condition: service_healthy
    networks: [front, back]
  db:
    image: postgres:18@sha256:<digest>
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets: [db_password]
    volumes: ["db-data:/var/lib/postgresql"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      retries: 5
    networks: [back]
networks:
  front: {}
  back:
    internal: true
volumes:
  db-data: {}
secrets:
  db_password:
    file: ./db_password.txt
```

A named volume holds data Docker owns; a bind mount, files the host edits, such as source in
development. Add a capability back with `cap_add` only where a process needs it.

### Registries

- Deploy the digest the push returned (`registry.example.com/web@sha256:…`): what CI tested.
- Sign in CI with Sigstore's cosign, and run `cosign verify` with the signer's identity and
  issuer before a deploy. Docker Content Trust is gone (fact `docker-engine-29`).
- Scan in CI and fail on fixable high and critical findings: `trivy image --exit-code 1
  --severity HIGH,CRITICAL --ignore-unfixed`, or `docker scout cves --exit-code --only-fixed`.
  Rescan published images weekly: new CVEs arrive after the build.

### Rootless Docker and Podman

Rootless mode runs the daemon and containers as an ordinary user, so an escape lands as that
user; read Docker's list of its limits first. Podman has no daemon and runs rootless for a
non-root user (fact `docker-podman-current`). Advice naming slirp4netns or cgroups v1 predates
Podman 6 (fact `docker-podman6`).

### Debugging

```bash
docker compose ps
docker compose logs --tail=100 web
id=$(docker compose ps -q web)
docker inspect --format '{{json .State.Health}}' "$id"
docker inspect --format 'exit={{.State.ExitCode}} oom={{.State.OOMKilled}}' "$id"
docker exec -it "$id" sh
```

Exit code 137 with `OOMKilled` true is the memory limit. For an image with no shell, join its
namespaces: `docker run --rm -it --pid=container:"$id" --network=container:"$id" busybox`.

## Mistakes

- **A tag with no digest, or `latest`.** The build changes under you. Pin the digest.
- **A token in `ARG` or `ENV`.** It stays in the image. Use a secret mount.
- **`version: "3.8"` atop a Compose file.** Assistants still write it; it earns a warning.
- **`depends_on: [db]` read as "wait until ready".** It orders start-up only. Add
  `condition: service_healthy`.
- **`DOCKER_CONTENT_TRUST=1` as image signing.** Engine 29 removed it. Use cosign.
- **`-p 5432:5432` on a host guarded by ufw.** Docker bypasses ufw, so the database is open to
  the network. Publish on `127.0.0.1`, or not at all.
- **The Docker socket mounted into a runner, proxy or dashboard.** That container is root on
  the host. Use a read-only socket proxy, or rootless mode.
- **A volume at a path the image doesn't declare.** Data lands in an anonymous volume, lost
  when the container is recreated; Postgres 18 moved its path (fact `docker-postgres-volume`).
  Check `docker image inspect --format '{{json .Config.Volumes}}'`.
- **`docker compose down -v` to reset.** It deletes the named volumes, the database with them.
  Take the database's own dump first, and run `down` without `-v`.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Base images pinned | `FROM` lines without `@sha256:` | `GAP` | Pin the digest; Dependabot's `docker` ecosystem moves it |
| Secrets in layers | A token in `ARG` or `ENV`; `docker history --no-trunc` | `BLOCKER` | Secret mount; rotate the secret |
| Runs as root | No `USER`, or `USER root` last | `GAP` | A non-root user |
| Privilege | `privileged: true`, or `/var/run/docker.sock` mounted | `BLOCKER` | Single capabilities; remove the socket |
| Hardening and limits | No `read_only`, `cap_drop: [ALL]`, `no-new-privileges`, `mem_limit` or `pids_limit` | `GAP` | Add them, with `tmpfs` where it writes |
| Published ports | `ports:` without a host address on a reachable host | `DRIFT` where a firewall is meant to cover it | Bind `127.0.0.1`, or drop the port |
| Compose spec | A `version:` key; short `depends_on` on a database | `DRIFT` | Remove the key; `service_healthy` |
| Supply chain | Production `image:` by tag; no scan or `cosign verify` | `GAP` | Deploy the digest; add both to CI |

## Why

### Digests, stages and small bases

- **The reason:** a tag can move to other content, and a digest names one image (fact
  `docker-pin-digest`). Every package left out of the final stage is a CVE that can't apply.
- **What others do:** Docker's guide pins digests, with Dependabot raising the bump. Many
  projects pin a minor tag, trading reproducibility for automatic patches.
- **What it costs:** without an update bot, a digest stops security fixes.
- **When to choose differently:** a throwaway local image can ride a tag.

### Secrets, users, capabilities and limits

- **The reason:** a build argument or variable persists in the image (fact
  `docker-build-secrets`). Root in a container plus a runtime flaw is root on the host; dropped
  capabilities and `no-new-privileges` shrink what a flaw reaches. A container without limits
  takes what the host allows (fact `docker-no-limits`), so one leak starves its neighbors.
- **What it costs:** an image that writes to its own tree or binds a low port needs a `tmpfs`
  or one `cap_add`.
- **When to choose differently:** a one-off tooling container may skip limits, never secrets.

### Privilege, the socket and published ports

- **The reason:** Docker says a privileged container can get a root shell on the host (fact
  `docker-privileged`). The socket is control of the daemon, for trusted users only (fact
  `docker-daemon-trust`). Published ports listen on every address (fact
  `docker-publish-default`) and skip ufw (fact `docker-ufw`).
- **When to choose differently:** a Docker-in-Docker runner needs privilege: give it its own
  host.

### Compose and registries

- **The reason:** Compose ignores `version:` (fact `docker-compose-version`), and short
  `depends_on` doesn't wait for health (fact `docker-depends-healthy`). A deployed digest is the
  image CI tested, and cosign checks the digest it signed (fact `docker-cosign-verify`).
- **What others do:** Kubernetes treats the digest as an image's identity. Since Engine 29,
  Docker leaves signing to cosign or Notation (fact `docker-engine-29`).

## Facts

Named elsewhere by ID. The newest Engine and Compose are facts `docker-engine-current` and
`docker-compose-current`.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `docker-engine-current` | Engine 29.9.3, 2026-11-03, is the newest | [Engine 29 release notes](https://docs.docker.com/engine/release-notes/29/) | "29.9.3" and "2026-11-03" | 2026-11-11 | 2027-02-11 |
| `docker-compose-current` | Compose's newest tag is v5.7.0 | `git ls-remote --tags https://github.com/docker/compose` | `refs/tags/v5.7.0` | 2026-11-11 | 2027-02-11 |
| `docker-podman-current` | Podman's newest tag is v6.2.0 | `git ls-remote --tags https://github.com/containers/podman` | `refs/tags/v6.2.0` | 2026-11-11 | 2027-02-11 |
| `docker-podman6` | Podman 6 removed slirp4netns, cgroups v1 and BoltDB | [Fedora: Podman 6](https://fedoraproject.org/wiki/Changes/Podman6) | "finalizes the removal of support for slirp4netns, cgroups v1, and the BoltDB database backend" | 2026-11-11 | 2027-05-11 |
| `docker-engine-29` | Engine 29.0.0 dropped Content Trust; the containerd store became the default | [Engine 29 release notes](https://docs.docker.com/engine/release-notes/29/) | "Docker Content Trust was removed from the Docker CLI." and "containerd image store is now the default for fresh installs." | 2026-11-11 | 2027-05-11 |
| `docker-pin-digest` | A digest pin holds when a tag moves; Dependabot updates it | [Build best practices](https://docs.docker.com/build/building/best-practices/) | "By pinning your images to a digest, you're guaranteed to always use the same image version" | 2026-11-11 | 2027-05-11 |
| `docker-build-secrets` | Build arguments and variables persist in the image | [Build secrets](https://docs.docker.com/build/building/secrets/) | "because they persist in the final image" | 2026-11-11 | 2027-05-11 |
| `docker-no-limits` | A container has no resource limits by default | [Resource constraints](https://docs.docker.com/engine/containers/resource_constraints/) | "By default, a container has no resource constraints" | 2026-11-11 | 2027-05-11 |
| `docker-privileged` | A privileged container can take over its host | [docker container run](https://docs.docker.com/reference/cli/docker/container/run/) | "Containers in this mode can get a root shell on the host" | 2026-11-11 | 2027-05-11 |
| `docker-daemon-trust` | Control of the daemon is for trusted users only | [Docker security](https://docs.docker.com/engine/security/) | "only trusted users should be allowed to control your Docker daemon" | 2026-11-11 | 2027-05-11 |
| `docker-publish-default` | Published ports listen on every host address | [Port publishing](https://docs.docker.com/engine/network/port-publishing/) | "Publishing container ports is insecure by default." | 2026-11-11 | 2027-05-11 |
| `docker-ufw` | Published ports bypass ufw | [Firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/) | "effectively ignoring your firewall configuration" | 2026-11-11 | 2027-05-11 |
| `docker-compose-version` | The top-level `version` key is obsolete | [Version and name](https://docs.docker.com/reference/compose-file/version-and-name/) | "you'll receive a warning message that it is obsolete if used" | 2026-11-11 | 2027-05-11 |
| `docker-depends-healthy` | `service_healthy` waits for the health check | [Services](https://docs.docker.com/reference/compose-file/services/) | "(as indicated by healthcheck) before starting a dependent" | 2026-11-11 | 2027-05-11 |
| `docker-cosign-verify` | `cosign verify` checks the signed digest | [Verifying signatures](https://docs.sigstore.dev/cosign/verifying/verify/) | "By default, cosign validates that this digest matches the container during cosign verify." | 2026-11-11 | 2027-05-11 |
| `docker-postgres-volume` | Postgres 18 moved its volume to `/var/lib/postgresql` | [postgres image docs](https://raw.githubusercontent.com/docker-library/docs/master/postgres/content.md) | "Mounts and volumes should be targeted at the updated location." | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Docker Docs](https://docs.docker.com/) | Versions, defaults and practice | Apache-2.0 in its repository, though pages say all rights reserved: facts in our own words, short quotes |
| [Sigstore cosign docs](https://docs.sigstore.dev/cosign/verifying/verify/) | Verifying signatures | Not stated on the page: short quotes only |
| [Fedora wiki: Podman 6](https://fedoraproject.org/wiki/Changes/Podman6) | Podman 6's removals | CC BY-SA 4.0: brief quotes with attribution, our own words otherwise |
| [docker-library/docs](https://github.com/docker-library/docs) | The postgres volume path | MIT: a fact with a short quote |
| GitHub tags of `docker/compose` and `containers/podman` | Current versions | Command output |
