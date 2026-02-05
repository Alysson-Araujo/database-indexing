package com.alysson.databaseindexing.service;

import com.alysson.databaseindexing.model.User;
import com.alysson.databaseindexing.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User findByEmail(String email) {
        return userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found with email: " + email));
    }

    public List<User> findByLocation(String country, String city) {
        return userRepository.findByCountryAndCity(country, city);
    }

    public List<User> findActiveRecent(int days) {
        LocalDateTime date = LocalDateTime.now().minusDays(days);
        return userRepository.findByStatusAndCreatedAtAfter("active", date);
    }
}
