package com.alysson.databaseindexing.repository;

import com.alysson.databaseindexing.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    // Query 1: Busca por email (sem índice será lenta)
    Optional<User> findByEmail(String email);

    // Query 2: Busca por país e cidade
    List<User> findByCountryAndCity(String country, String city);

    // Query 3: Busca por status e data
    @Query("SELECT u FROM User u WHERE u.status = :status AND u.createdAt >= :date")
    List<User> findByStatusAndCreatedAtAfter(
            @Param("status") String status,
            @Param("date") LocalDateTime date
    );

    // Query 4: Busca complexa com join
    @Query("""
        SELECT u FROM User u
        JOIN Order o ON u.id = o.userId
        WHERE u.country = :country
        AND o.orderDate >= :date
        """)
    List<User> findUsersWithOrdersByCountry(
            @Param("country") String country,
            @Param("date") LocalDateTime date
    );
}