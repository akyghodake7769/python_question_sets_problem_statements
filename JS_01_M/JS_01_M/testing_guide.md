# Testing Guide: JS_01_M (Spring Boot Startup Failures - Local VM)

This guide provides instructions on how to solve and verify the problem statement successfully on your local VM.

## Prerequisites
Make sure Maven and Java 11+ are installed on the local Linux/VM:
```bash
sudo apt-get update
sudo apt-get install maven default-jdk -y
java -version
mvn -version
```

## Step 1: Open the Terminal
Open the terminal on your local machine. Navigate to the `student_workspace` directory inside the problem folder:
```bash
cd student_workspace
```

## Step 2: Fix the Bean Wiring Error (Passes TC2)
Open `src/main/java/com/kloudlabs/app/service/UserService.java` and add the `@Service` annotation:
```java
import org.springframework.stereotype.Service;

@Service
public class UserService {
    // ...
}
```

## Step 3: Change the Server Port (Passes TC3)
Open `src/main/resources/application.properties` and set:
```properties
server.port=8081
```

## Step 4: Compile the Application (Passes TC1)
```bash
mvn clean compile
```
If this exits with `BUILD SUCCESS`, TC1 passes.

## Step 5: Start the Application in the Background (Passes TC4 & TC5)
```bash
nohup mvn spring-boot:run > /tmp/springboot.log 2>&1 &
```
Wait ~30 seconds, then verify:
```bash
curl http://localhost:8081/actuator/health
```
Expected: `{"status":"UP"}`

## Step 6: Run the Verification Script
Run local evaluation from the root workspace directory:
```bash
python3 student_workspace/run.py
```
The script will check all 5 test cases and display your score out of 20.
