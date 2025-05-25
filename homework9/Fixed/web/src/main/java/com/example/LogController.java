package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.*;

@RestController
public class LogController {
    private static final Logger logger = LogManager.getLogger(LogController.class);

    @GetMapping("/log")
    public String logInput(@RequestParam String input) {
        
        // Basic input validation to prevent JNDI exploit attempts
        if (input != null && input.toLowerCase().contains("jndi:")) {
            logger.warn("Blocked suspicious input: {}", input);
            return "Suspicious input was blocked";
        }

        //Regex-Based Hardening for stronger filtering (e.g., against ${, ${env, ${java:, etc.)
        if (input != null && input.matches("(?i).*\\$\\{.*\\}.*")) {
            logger.warn("Blocked potentially malicious input: {}", input);
            return "Suspicious input was blocked";
        }

        // Safe to log
        logger.error("User input: {}", input);

        // Print logger implementation class
        System.out.println("Logger class: " + logger.getClass().getName());

        // Check what logging backend is actually active at runtime
        try {
            org.slf4j.ILoggerFactory loggerFactory = org.slf4j.LoggerFactory.getILoggerFactory();
            System.out.println("LoggerFactory class: " + loggerFactory.getClass().getName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        return "Logged: " + input;
    }

}
