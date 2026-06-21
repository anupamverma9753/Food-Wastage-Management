
        SELECT 
            "Location" as City,
            COUNT("Food_ID") as Total_Food_Listings,
            SUM("Quantity") as Total_Quantity,
            COUNT(DISTINCT "Provider_ID") as Number_of_Providers
        FROM Food_Listings
        GROUP BY "Location"
        ORDER BY Total_Food_Listings DESC;