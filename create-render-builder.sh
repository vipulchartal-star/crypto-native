#!/data/data/com.termux/files/usr/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET_DIR="${1:-$ROOT_DIR/render-apk-builder-deploy}"
SERVICE_NAME="${2:-termux-apk-builder}"
TEMPLATE_DIR="$ROOT_DIR/render-apk-builder-template"
PROJECT_DIR="$ROOT_DIR/simple-android-app"

log() {
    printf '\n[%s] %s\n' "$1" "$2"
}

require_path() {
    if [ ! -e "$1" ]; then
        printf 'Missing required path: %s\n' "$1" >&2
        exit 1
    fi
}

copy_tree() {
    src="$1"
    dst="$2"
    rm -rf "$dst"
    mkdir -p "$(dirname "$dst")"
    cp -R "$src" "$dst"
}

main() {
    require_path "$TEMPLATE_DIR"
    require_path "$PROJECT_DIR"

    log INFO "Creating Render APK builder package"
    mkdir -p "$TARGET_DIR"

    copy_tree "$PROJECT_DIR" "$TARGET_DIR/simple-android-app"

    cp "$TEMPLATE_DIR/Dockerfile" "$TARGET_DIR/Dockerfile"
    cp "$TEMPLATE_DIR/requirements.txt" "$TARGET_DIR/requirements.txt"
    cp "$TEMPLATE_DIR/server.py" "$TARGET_DIR/server.py"
    cp "$TEMPLATE_DIR/build_android.sh" "$TARGET_DIR/build_android.sh"
    cp "$TEMPLATE_DIR/README.md" "$TARGET_DIR/README.md"

    cat > "$TARGET_DIR/render.yaml" <<EOF
services:
  - type: web
    name: $SERVICE_NAME
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: starter
    autoDeploy: false
EOF

    chmod +x "$TARGET_DIR/build_android.sh"

    log DONE "Render builder package created at $TARGET_DIR"
    printf 'Render service name: %s\n' "$SERVICE_NAME"
    printf 'Next step: push %s to a repo or deploy it on Render as a Docker web service.\n' "$TARGET_DIR"
}

main "$@"
