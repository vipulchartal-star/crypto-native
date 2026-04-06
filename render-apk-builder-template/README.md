# Render APK Builder

This package deploys a Docker-based Render web service that builds the bundled Android app and exposes the resulting APK for download.

## Endpoints

- `GET /health` — service status
- `POST /build` — build the bundled `simple-android-app`
- `GET /latest` — fetch metadata for the newest APK
- `GET /artifacts/<name>` — download a built APK

## Deploy

1. Push this folder as its own repo, or deploy it from a subdirectory-aware workflow.
2. On Render, create a new Docker web service.
3. Point it at this package.
4. After deploy, call:

```sh
curl -X POST https://YOUR-RENDER-SERVICE.onrender.com/build
```

5. Download the returned `download_url`.

## Notes

- The build script strips the Termux-only `android.aapt2FromMavenOverride` line before building on Linux x86_64.
- Android SDK packages are installed into the Docker image at build time to keep request-time builds faster.
