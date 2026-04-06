FROM eclipse-temurin:17-jdk-jammy

ARG GRADLE_VERSION=9.4.1
ARG CMDLINE_TOOLS_ZIP=commandlinetools-linux-13114758_latest.zip
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_HOME=/opt/android-sdk
ENV GRADLE_HOME=/opt/gradle/gradle-9.4.1
ENV PATH=/opt/gradle/gradle-9.4.1/bin:/opt/android-sdk/cmdline-tools/latest/bin:/opt/android-sdk/platform-tools:$PATH
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    python3 \
    python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/gradle /opt/android-sdk/cmdline-tools /tmp/android

RUN curl -fsSL "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" -o /tmp/gradle.zip \
    && unzip -q /tmp/gradle.zip -d /opt/gradle \
    && rm /tmp/gradle.zip

RUN curl -fsSL "https://dl.google.com/android/repository/${CMDLINE_TOOLS_ZIP}" -o /tmp/android/cmdline-tools.zip \
    && unzip -q /tmp/android/cmdline-tools.zip -d /opt/android-sdk/cmdline-tools \
    && mv /opt/android-sdk/cmdline-tools/cmdline-tools /opt/android-sdk/cmdline-tools/latest \
    && rm -rf /tmp/android

RUN yes | sdkmanager --sdk_root="${ANDROID_SDK_ROOT}" --licenses >/dev/null
RUN sdkmanager --sdk_root="${ANDROID_SDK_ROOT}" \
    "platform-tools" \
    "platforms;android-34" \
    "build-tools;34.0.0"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY build_android.sh /app/build_android.sh
COPY server.py /app/server.py
COPY simple-android-app /app/simple-android-app

RUN chmod +x /app/build_android.sh

ENV PORT=10000
EXPOSE 10000

CMD ["python3", "/app/server.py"]
