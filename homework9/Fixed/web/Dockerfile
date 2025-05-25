# ---- Build Stage ----
FROM maven:3.8.5-openjdk-11 AS build
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

# ---- Runtime Stage ----
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app

# Copy the built Spring Boot JAR
COPY --from=build /app/target/*.jar app.jar

# Expose the web app port
EXPOSE 8080

# Optional: print environment info at container start
CMD java -Djava.security.debug=properties -jar app.jar
