package com.mis_demo.app;

/**
 * Hello world!
 */
public class Sample
{

    private final String message = "Hello World!";

    public Sample() {}

    public static void main(String[] args) {
        System.out.println(new Sample().getMessage());
    }

    private final String getMessage() {
        return message;
    }

}
