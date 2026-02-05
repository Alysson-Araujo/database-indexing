package com.alysson.databaseindexing.repository;

import com.alysson.databaseindexing.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigDecimal;
import java.util.List;

public interface ProductRepository extends JpaRepository<Product, Long> {

    // Query por categoria
    List<Product> findByCategory(String category);

    // Query por categoria e range de preço (composite index: category, price)
    @Query("SELECT p FROM Product p WHERE p.category = :category AND p.price BETWEEN :minPrice AND :maxPrice")
    List<Product> findByCategoryAndPriceRange(
            @Param("category") String category,
            @Param("minPrice") BigDecimal minPrice,
            @Param("maxPrice") BigDecimal maxPrice
    );

    // Query com detalhes para covering index test
    @Query("SELECT p FROM Product p WHERE p.category = :category ORDER BY p.price ASC")
    List<Product> findProductDetailsByCategory(@Param("category") String category);
}
