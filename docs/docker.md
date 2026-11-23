# Docker

The `Dockerfile` ships everything needed to run the generator end-to-end: Python 3.13, the WeasyPrint native libraries and Node.js 22 for the Vite build.

## Build

```bash
docker build -t resume-creator .
```

## Usage

The image entrypoint is `python main.py`, so any subcommand works directly.

```bash
# default action: build pdf + web
docker run --rm \
  -v "$PWD/data:/app/data" \
  -v "$PWD/build:/app/build" \
  resume-creator

# pdf only
docker run --rm \
  -v "$PWD/data:/app/data" \
  -v "$PWD/build:/app/build" \
  resume-creator build pdf

# validate the configuration
docker run --rm -v "$PWD/data:/app/data" resume-creator validate
```

Bind-mount `./data` to keep your YAML and photo on the host, and `./build` to retrieve the generated PDFs and web bundle.
