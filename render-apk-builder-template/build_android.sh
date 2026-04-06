#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_SOURCE_DIR="$ROOT_DIR/simple-android-app"
WORK_ROOT="${WORK_ROOT:-/tmp/render-apk-builder}"
SDK_ROOT="${ANDROID_SDK_ROOT:-/opt/android-sdk}"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-$WORK_ROOT/.gradle}"
BUILD_DIR="$WORK_ROOT/build"
PROJECT_DIR="$BUILD_DIR/simple-android-app"
APK_OUT="$WORK_ROOT/artifacts/app-debug.apk"

log() {
    printf '\n[%s] %s\n' "$1" "$2"
}

prepare_workspace() {
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR" "$WORK_ROOT/artifacts" "$GRADLE_USER_HOME"
    cp -R "$PROJECT_SOURCE_DIR" "$PROJECT_DIR"

    if [ -f "$PROJECT_DIR/gradle.properties" ]; then
        grep -v '^android.aapt2FromMavenOverride=' "$PROJECT_DIR/gradle.properties" > "$PROJECT_DIR/gradle.properties.tmp" || true
        mv "$PROJECT_DIR/gradle.properties.tmp" "$PROJECT_DIR/gradle.properties"
    fi

    cat > "$PROJECT_DIR/local.properties" <<EOF
sdk.dir=$SDK_ROOT
EOF
}

build_apk() {
    log INFO "Building debug APK in $PROJECT_DIR"
    cd "$PROJECT_DIR"
    export GRADLE_USER_HOME
    gradle assembleDebug --no-daemon
}

collect_artifact() {
    src="$PROJECT_DIR/app/build/outputs/apk/debug/app-debug.apk"
    if [ ! -f "$src" ]; then
        printf 'APK not found: %s\n' "$src" >&2
        exit 1
    fi
    cp "$src" "$APK_OUT"
    printf '%s\n' "$APK_OUT"
}

prepare_workspace
build_apk
collect_artifact
