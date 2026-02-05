package com.alysson.databaseindexing.service;

import com.alysson.databaseindexing.model.Product;
import com.alysson.databaseindexing.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;

@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public List<Product> findByCategory(String category) {
        return productRepository.findByCategory(category);
    }

    public List<Product> findByCategoryAndPriceRange(String category, BigDecimal minPrice, BigDecimal maxPrice) {
        return productRepository.findByCategoryAndPriceRange(category, minPrice, maxPrice);
    }

    public List<Product> findProductDetailsByCategory(String category) {
        return productRepository.findProductDetailsByCategory(category);
    }
}
