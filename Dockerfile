FROM eclipse-temurin:17-jdk-jammy AS build
WORKDIR /source
COPY src ./src
COPY web ./web
COPY build.sh ./build.sh
RUN sh build.sh

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /source/campusloop.jar ./campusloop.jar
COPY lib ./lib
RUN mkdir -p /var/data
ENV BIND_ADDRESS=0.0.0.0 \
    DATA_DIR=/var/data \
    COOKIE_SECURE=true \
    REQUIRE_EXTERNAL_DB=true \
    PORT=8080 \
    JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=70 -Duser.timezone=Asia/Kolkata"
EXPOSE 8080
CMD ["java", "-cp", "campusloop.jar:lib/*", "campusloop.App"]
