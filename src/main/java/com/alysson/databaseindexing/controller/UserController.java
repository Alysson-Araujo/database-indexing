package com.alysson.databaseindexing.controller;

import com.alysson.databaseindexing.model.User;
import com.alysson.databaseindexing.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    // Endpoint para testes k6 - busca por email
    @GetMapping("/search")
    public ResponseEntity<User> searchByEmail(@RequestParam String email) {
        long start = System.currentTimeMillis();
        User user = userService.findByEmail(email);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(user);
    }

    // Endpoint 1: Buscar por email
    @GetMapping("/by-email")
    public ResponseEntity<User> findByEmail(@RequestParam String email) {
        long start = System.currentTimeMillis();
        User user = userService.findByEmail(email);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(user);
    }

    // Endpoint 2: Buscar por país e cidade
    @GetMapping("/by-location")
    public ResponseEntity<List<User>> findByLocation(
            @RequestParam String country,
            @RequestParam String city) {

        long start = System.currentTimeMillis();
        List<User> users = userService.findByLocation(country, city);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(users);
    }

    // Endpoint 3: Usuários ativos recentes
    @GetMapping("/active-recent")
    public ResponseEntity<List<User>> findActiveRecent(
            @RequestParam(defaultValue = "30") int days) {

        long start = System.currentTimeMillis();
        List<User> users = userService.findActiveRecent(days);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(users);
    }
}