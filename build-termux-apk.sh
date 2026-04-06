#!/data/data/com.termux/files/usr/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR="${PROJECT_DIR:-$ROOT_DIR/simple-android-app}"
SDK_ROOT="${ANDROID_SDK_ROOT:-$HOME/android-sdk}"
INSTALLER_URL="https://raw.githubusercontent.com/Sohil876/termux-sdk-installer/main/installer.sh"
INSTALLER_PATH="$HOME/install-android-sdk.sh"
APK_PATH="$PROJECT_DIR/app/build/outputs/apk/debug/app-debug.apk"
DOWNLOAD_APK_PATH="$HOME/storage/downloads/simple-android-app.apk"

log() {
    printf '\n[%s] %s\n' "$1" "$2"
}

require_path() {
    if [ ! -e "$1" ]; then
        printf 'Missing required path: %s\n' "$1" >&2
        exit 1
    fi
}

ensure_termux_storage() {
    if [ ! -d "$HOME/storage/downloads" ]; then
        log INFO "Requesting shared storage access for Termux"
        termux-setup-storage || true
    fi
}

install_packages() {
    log INFO "Installing Termux build dependencies"
    pkg update -y
    pkg install -y openjdk-21 wget curl jq tar xz-utils unzip termux-tools
}

install_sdk_base() {
    if [ -x "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" ] && [ -d "$SDK_ROOT/build-tools/34.0.4" ]; then
        log INFO "Android SDK base already present at $SDK_ROOT"
        return
    fi

    log INFO "Downloading Termux Android SDK installer"
    curl -L "$INSTALLER_URL" -o "$INSTALLER_PATH"
    chmod +x "$INSTALLER_PATH"

    log INFO "Installing Android SDK base files"
    yes y | bash "$INSTALLER_PATH" -i
}

install_sdk_components() {
    log INFO "Installing required Android SDK packages"
    yes | "$SDK_ROOT/cmdline-tools/latest/bin/sdkmanager" \
        --sdk_root="$SDK_ROOT" \
        "platforms;android-34" \
        "build-tools;34.0.0"
}

write_local_properties() {
    log INFO "Writing local.properties"
    cat > "$PROJECT_DIR/local.properties" <<EOF
sdk.dir=$SDK_ROOT
EOF
}

build_apk() {
    log INFO "Building debug APK"
    cd "$PROJECT_DIR"
    gradle assembleDebug --no-daemon
}

copy_apk() {
    require_path "$APK_PATH"
    ensure_termux_storage

    if [ -d "$HOME/storage/downloads" ]; then
        log INFO "Copying APK to shared Downloads"
        cp "$APK_PATH" "$DOWNLOAD_APK_PATH"
        printf 'Shared APK: %s\n' "$DOWNLOAD_APK_PATH"
    fi

    printf 'Build output: %s\n' "$APK_PATH"
}

main() {
    require_path "$PROJECT_DIR"
    install_packages
    install_sdk_base
    install_sdk_components
    write_local_properties
    build_apk
    copy_apk
    log DONE "APK build finished"
}

main "$@"
