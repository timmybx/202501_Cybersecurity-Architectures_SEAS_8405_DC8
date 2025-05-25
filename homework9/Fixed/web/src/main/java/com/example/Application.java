package com.example;

import org.apache.logging.log4j.util.PropertiesUtil;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);

        // Print Log4j version
        System.out.println("Java version: " + System.getProperty("java.version"));
        
        // Print Log4j version
        String version = PropertiesUtil.class.getPackage().getImplementationVersion();
        System.out.println("Log4j version: " + version);

        // Print potentially relevant JNDI security properties
        System.out.println("com.sun.jndi.ldap.object.trustURLCodebase = " +
            System.getProperty("com.sun.jndi.ldap.object.trustURLCodebase"));
        System.out.println("com.sun.jndi.ldap.object.factoriesFilter = " +
            System.getProperty("com.sun.jndi.ldap.object.factoriesFilter"));
    }
}
