package com.alysson.databaseindexing.repository;

import com.alysson.databaseindexing.model.OrderItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface OrderItemRepository extends JpaRepository<OrderItem, Long> {

    // Query por order_id
    List<OrderItem> findByOrderId(Long orderId);

    // Query por product_id
    List<OrderItem> findByProductId(Long productId);

    // Query com detalhes para covering index test
    @Query("SELECT oi FROM OrderItem oi WHERE oi.orderId = :orderId ORDER BY oi.id ASC")
    List<OrderItem> findOrderItemDetailsByOrderId(@Param("orderId") Long orderId);
}
