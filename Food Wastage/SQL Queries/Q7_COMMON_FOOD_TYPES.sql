
        SELECT 
            "Food_Type",
            COUNT("Food_ID") as Number_of_Listings,
            SUM("Quantity") as Total_Quantity,
            ROUND(AVG("Quantity"), 2) as Average_Quantity
        FROM Food_Listings
        GROUP BY "Food_Type"
        ORDER BY Number_of_Listings DESC;