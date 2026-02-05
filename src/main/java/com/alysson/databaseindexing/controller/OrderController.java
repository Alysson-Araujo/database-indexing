package com.alysson.databaseindexing.controller;

import com.alysson.databaseindexing.model.Order;
import com.alysson.databaseindexing.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    // GET /api/orders/user/{userId}
    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Order>> findByUserId(@PathVariable Long userId) {
        long start = System.currentTimeMillis();
        List<Order> orders = orderService.findByUserId(userId);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orders);
    }

    // GET /api/orders/status/{status}
    @GetMapping("/status/{status}")
    public ResponseEntity<List<Order>> findByStatus(@PathVariable String status) {
        long start = System.currentTimeMillis();
        List<Order> orders = orderService.findByStatus(status);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orders);
    }

    // GET /api/orders/user/{userId}/date-range?start=2024-01-01&end=2024-12-31
    @GetMapping("/user/{userId}/date-range")
    public ResponseEntity<List<Order>> findByUserIdAndDateRange(
            @PathVariable Long userId,
            @RequestParam String start,
            @RequestParam String end) {
        long startTime = System.currentTimeMillis();
        List<Order> orders = orderService.findByUserIdAndDateRange(userId, start, end);
        long duration = System.currentTimeMillis() - startTime;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orders);
    }

    // GET /api/orders/user/{userId}/status/{status}
    @GetMapping("/user/{userId}/status/{status}")
    public ResponseEntity<List<Order>> findByUserIdAndStatus(
            @PathVariable Long userId,
            @PathVariable String status) {
        long start = System.currentTimeMillis();
        List<Order> orders = orderService.findByUserIdAndStatus(userId, status);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orders);
    }

    // GET /api/orders/status/{status}/date-range?start=2024-01-01&end=2024-12-31
    @GetMapping("/status/{status}/date-range")
    public ResponseEntity<List<Order>> findByStatusAndDateRange(
            @PathVariable String status,
            @RequestParam String start,
            @RequestParam String end) {
        long startTime = System.currentTimeMillis();
        List<Order> orders = orderService.findByStatusAndDateRange(status, start, end);
        long duration = System.currentTimeMillis() - startTime;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orders);
    }

    // GET /api/orders/user/{userId}/details (for covering index test)
    @GetMapping("/user/{userId}/details")
    public ResponseEntity<List<Order>> findOrderDetailsByUserId(@PathVariable Long userId) {
        long start = System.currentTimeMillis();
        List<Order> orders = orderService.findOrderDetailsByUserId(userId);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orders);
    }
}
