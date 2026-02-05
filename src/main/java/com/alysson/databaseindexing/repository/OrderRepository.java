package com.alysson.databaseindexing.repository;

import com.alysson.databaseindexing.model.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {

    // Query por user_id
    List<Order> findByUserId(Long userId);

    // Query por status
    List<Order> findByStatus(String status);

    // Query por user_id e intervalo de datas (composite index: user_id, order_date)
    @Query("SELECT o FROM Order o WHERE o.userId = :userId AND o.orderDate BETWEEN :startDate AND :endDate")
    List<Order> findByUserIdAndDateRange(
            @Param("userId") Long userId,
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate
    );

    // Query por user_id e status (composite index: user_id, status)
    List<Order> findByUserIdAndStatus(Long userId, String status);

    // Query por status e intervalo de datas (composite index: status, order_date)
    @Query("SELECT o FROM Order o WHERE o.status = :status AND o.orderDate BETWEEN :startDate AND :endDate")
    List<Order> findByStatusAndDateRange(
            @Param("status") String status,
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate
    );

    // Query com detalhes para covering index test
    @Query("SELECT o FROM Order o WHERE o.userId = :userId ORDER BY o.orderDate DESC")
    List<Order> findOrderDetailsByUserId(@Param("userId") Long userId);
}
