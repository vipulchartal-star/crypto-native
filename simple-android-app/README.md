# Simple Android App

Minimal Android sample app intended for building from Termux.

## What it does

- Shows a title and a message
- Updates the message when you tap the button

## Build from Termux

1. Install the Android SDK using the setup from `termux-build-apps`.
2. Make sure `platforms;android-35` and the matching build-tools are installed.
3. Create `local.properties` from `local.properties.example` and point `sdk.dir` at your SDK.
4. Run:

```sh
gradle assembleDebug
```

If you already generated a wrapper, you can use:

```sh
./gradlew assembleDebug
```
