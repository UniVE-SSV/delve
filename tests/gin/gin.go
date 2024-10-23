package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

func main() {
    // Create a Gin router
    router := gin.Default()

    // Define a simple GET route for the root path
    router.GET("/", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
            "message": "Welcome to Gin!",
        })
    })

    // Define a GET route with a dynamic parameter
    router.GET("/items/:id", func(c *gin.Context) {
        itemID := c.Param("id") // Get the dynamic item ID from the URL
        queryParam := c.DefaultQuery("q", "no query") // Get query parameter (if provided)

        c.JSON(http.StatusOK, gin.H{
            "item_id": itemID,
            "query":   queryParam,
        })
    })

    // Start the server on port 8080
    router.Run(":8080")
}