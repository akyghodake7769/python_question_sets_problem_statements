package com.kloudlabs.app.service;

// TODO: The application is failing to start because Spring cannot find this bean.
// Hint: This class needs a stereotype annotation so Spring can detect it during component scanning.

import org.springframework.stereotype.Service;

@Service
public class UserService {
    
    public String getUserGreeting() {
        return "Hello, User!";
    }
}
