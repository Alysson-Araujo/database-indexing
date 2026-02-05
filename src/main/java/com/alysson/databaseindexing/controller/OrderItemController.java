package com.alysson.databaseindexing.controller;

import com.alysson.databaseindexing.model.OrderItem;
import com.alysson.databaseindexing.service.OrderItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/order-items")
public class OrderItemController {

    @Autowired
    private OrderItemService orderItemService;

    @GetMapping("/order/{orderId}")
    public ResponseEntity<List<OrderItem>> findByOrderId(@PathVariable Long orderId) {
        long start = System.currentTimeMillis();
        List<OrderItem> orderItems = orderItemService.findByOrderId(orderId);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orderItems);
    }

    @GetMapping("/order/{orderId}/details")
    public ResponseEntity<List<OrderItem>> findOrderItemDetailsByOrderId(@PathVariable Long orderId) {
        long start = System.currentTimeMillis();
        List<OrderItem> orderItems = orderItemService.findOrderItemDetailsByOrderId(orderId);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(orderItems);
    }
}
