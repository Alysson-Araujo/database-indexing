package com.alysson.databaseindexing.controller;

import com.alysson.databaseindexing.model.Product;
import com.alysson.databaseindexing.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping("/category/{category}")
    public ResponseEntity<List<Product>> findByCategory(@PathVariable String category) {
        long start = System.currentTimeMillis();
        List<Product> products = productService.findByCategory(category);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(products);
    }

    @GetMapping("/category/{category}/price-range")
    public ResponseEntity<List<Product>> findByCategoryAndPriceRange(
            @PathVariable String category,
            @RequestParam BigDecimal min,
            @RequestParam BigDecimal max) {
        long start = System.currentTimeMillis();
        List<Product> products = productService.findByCategoryAndPriceRange(category, min, max);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(products);
    }

    @GetMapping("/category/{category}/details")
    public ResponseEntity<List<Product>> findProductDetailsByCategory(@PathVariable String category) {
        long start = System.currentTimeMillis();
        List<Product> products = productService.findProductDetailsByCategory(category);
        long duration = System.currentTimeMillis() - start;

        return ResponseEntity.ok()
                .header("X-Query-Time", String.valueOf(duration))
                .body(products);
    }
}
