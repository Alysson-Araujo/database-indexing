package com.alysson.databaseindexing.service;

import com.alysson.databaseindexing.model.OrderItem;
import com.alysson.databaseindexing.repository.OrderItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderItemService {

    @Autowired
    private OrderItemRepository orderItemRepository;

    public List<OrderItem> findByOrderId(Long orderId) {
        return orderItemRepository.findByOrderId(orderId);
    }

    public List<OrderItem> findByProductId(Long productId) {
        return orderItemRepository.findByProductId(productId);
    }

    public List<OrderItem> findOrderItemDetailsByOrderId(Long orderId) {
        return orderItemRepository.findOrderItemDetailsByOrderId(orderId);
    }
}
