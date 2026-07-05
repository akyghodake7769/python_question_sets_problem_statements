# JS_02_M: Spring Profile Configuration Extraction

## Objective
Read and extract specific configuration values from a multi-profile Spring Boot `application.yml` file.

## Problem Description
You are given a Spring Boot configuration file (`application.yml`) that contains multiple configuration profiles: `default`, `dev`, and `prod`. The production profile contains a sensitive database password that needs to be extracted for an automated deployment script.

Your task is to write a bash script named `extract.sh` that reads the `application.yml` file, extracts the `db.password` value specifically for the `prod` profile, and writes it to a file named `output.txt`.

## Tasks
1. Navigate to the `student_workspace` directory.
2. Review the `src/main/resources/application.yml` file to understand its structure.
3. Edit the provided `extract.sh` script.
4. Your script must parse the YAML file and extract the value of `db.password` under the `prod` profile (e.g., using `grep`, `awk`, `sed`, or `yq`).
5. Ensure the script writes the exact password string into a new file named `output.txt` in the `student_workspace` directory.
6. Make sure your script is executable (`chmod +x extract.sh`) and runs successfully.

## Evaluation Criteria
- **TC1:** `extract.sh` has execution permissions and runs successfully.
- **TC2:** The `output.txt` file is generated.
- **TC3:** `output.txt` is not empty.
- **TC4:** `output.txt` contains the correct `db.password` value for the `prod` profile.
- **TC5:** `output.txt` does NOT contain passwords from the `dev` or `default` profiles.
